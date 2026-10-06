package client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"
)

type SceneObject struct {
	VariableName string `json:"variable_name"`
	WrapperType  string `json:"wrapper_type"`
}

type VarwinClient struct {
	BaseURL      string
	Endpoint     string
	AccessToken  string
	RefreshToken string
	WorkspaceID  int
	UserInfo     map[string]interface{}
	HTTPClient   *http.Client
	mu           sync.RWMutex
}

func NewVarwinClient(baseURL string) *VarwinClient {
	if baseURL == "" {
		baseURL = os.Getenv("VARWIN_URL")
		if baseURL == "" {
			baseURL = "http://127.0.0.1:1801"
		}
	}
	baseURL = strings.TrimRight(baseURL, "/")
	return &VarwinClient{
		BaseURL:  baseURL,
		Endpoint: baseURL + "/query",
		HTTPClient: &http.Client{
			Timeout: 15 * time.Second,
		},
	}
}

type graphQLRequest struct {
	Query     string                 `json:"query"`
	Variables map[string]interface{} `json:"variables,omitempty"`
}

type graphQLErrorExtension struct {
	Code string `json:"code"`
}

type graphQLError struct {
	Message    string                 `json:"message"`
	Extensions *graphQLErrorExtension `json:"extensions,omitempty"`
}

type graphQLResponse struct {
	Data   map[string]interface{} `json:"data"`
	Errors []graphQLError         `json:"errors,omitempty"`
}

func (c *VarwinClient) ExecuteRaw(query string, variables map[string]interface{}, auth bool) (map[string]interface{}, error) {
	if auth {
		if err := c.EnsureAuth(); err != nil {
			return nil, err
		}
	}

	payload := graphQLRequest{
		Query:     query,
		Variables: variables,
	}
	bodyBytes, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	req, err := http.NewRequest("POST", c.Endpoint, bytes.NewReader(bodyBytes))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "VarwinMCP-Go/1.0")

	c.mu.RLock()
	token := c.AccessToken
	c.mu.RUnlock()

	if auth && token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to Varwin Server at %s: %w", c.Endpoint, err)
	}
	defer resp.Body.Close()

	respBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	if resp.StatusCode >= 400 && len(respBytes) == 0 {
		return nil, fmt.Errorf("HTTP %d error from Varwin Server", resp.StatusCode)
	}

	var gqlResp graphQLResponse
	if err := json.Unmarshal(respBytes, &gqlResp); err != nil {
		return nil, fmt.Errorf("HTTP %d error: %s", resp.StatusCode, string(respBytes))
	}

	if len(gqlResp.Errors) > 0 {
		var expired bool
		var errMsgs []string
		for _, e := range gqlResp.Errors {
			errMsgs = append(errMsgs, e.Message)
			if e.Extensions != nil && e.Extensions.Code == "authorizationRequired" {
				expired = true
			}
		}

		if expired && auth {
			// Re-authenticate and retry once
			if _, err := c.Authenticate(); err == nil {
				return c.ExecuteRaw(query, variables, false)
			}
		}

		if gqlResp.Data == nil {
			return nil, fmt.Errorf("GraphQL Error: %s", strings.Join(errMsgs, "; "))
		}
	}

	return gqlResp.Data, nil
}

func (c *VarwinClient) Authenticate() (string, error) {
	c.mu.Lock()
	defer c.mu.Unlock()

	mutation := `
	mutation {
		loginAsDefaultUser(input: { clientInfo: "VarwinMCP-Go" }) {
			accessToken
			refreshToken
			user {
				id
				login
				fullName
				ownerWorkspaceId
			}
		}
	}
	`
	payload := graphQLRequest{Query: mutation}
	bodyBytes, _ := json.Marshal(payload)

	req, err := http.NewRequest("POST", c.Endpoint, bytes.NewReader(bodyBytes))
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "VarwinMCP-Go/1.0")

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return "", fmt.Errorf("auth request failed: %w", err)
	}
	defer resp.Body.Close()

	respBytes, _ := io.ReadAll(resp.Body)
	var gqlResp graphQLResponse
	if err := json.Unmarshal(respBytes, &gqlResp); err != nil {
		return "", fmt.Errorf("auth unmarshal failed: %w", err)
	}

	loginData, ok := gqlResp.Data["loginAsDefaultUser"].(map[string]interface{})
	if !ok || loginData == nil {
		return "", fmt.Errorf("loginAsDefaultUser returned empty response")
	}

	c.AccessToken, _ = loginData["accessToken"].(string)
	c.RefreshToken, _ = loginData["refreshToken"].(string)
	c.UserInfo, _ = loginData["user"].(map[string]interface{})

	// Resolve active workspace
	c.resolveWorkspaceUnlocked()

	return c.AccessToken, nil
}

func (c *VarwinClient) EnsureAuth() error {
	c.mu.RLock()
	hasToken := c.AccessToken != ""
	c.mu.RUnlock()

	if !hasToken {
		_, err := c.Authenticate()
		return err
	}
	return nil
}

func parseID(val interface{}) int {
	if val == nil {
		return 0
	}
	switch v := val.(type) {
	case float64:
		return int(v)
	case int:
		return v
	case string:
		if id, err := strconv.Atoi(v); err == nil {
			return id
		}
	}
	return 0
}

func (c *VarwinClient) resolveWorkspaceUnlocked() {
	query := `
	query {
		workspaceMembership {
			totalCount
			edges {
				node {
					id
					name
					state
				}
			}
		}
	}
	`
	payload := graphQLRequest{Query: query}
	bodyBytes, _ := json.Marshal(payload)

	req, err := http.NewRequest("POST", c.Endpoint, bytes.NewReader(bodyBytes))
	if err != nil {
		c.fallbackWorkspace()
		return
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+c.AccessToken)

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		c.fallbackWorkspace()
		return
	}
	defer resp.Body.Close()

	respBytes, _ := io.ReadAll(resp.Body)
	var gqlResp graphQLResponse
	if err := json.Unmarshal(respBytes, &gqlResp); err != nil {
		c.fallbackWorkspace()
		return
	}

	wsMem, ok := gqlResp.Data["workspaceMembership"].(map[string]interface{})
	if !ok || wsMem == nil {
		c.fallbackWorkspace()
		return
	}

	edges, ok := wsMem["edges"].([]interface{})
	if !ok || len(edges) == 0 {
		c.fallbackWorkspace()
		return
	}

	for _, e := range edges {
		edgeMap, ok := e.(map[string]interface{})
		if !ok {
			continue
		}
		node, ok := edgeMap["node"].(map[string]interface{})
		if !ok {
			continue
		}
		if node["state"] == "active" {
			if id := parseID(node["id"]); id > 0 {
				c.WorkspaceID = id
				return
			}
		}
	}

	// First edge fallback
	if firstEdge, ok := edges[0].(map[string]interface{}); ok {
		if node, ok := firstEdge["node"].(map[string]interface{}); ok {
			if id := parseID(node["id"]); id > 0 {
				c.WorkspaceID = id
				return
			}
		}
	}

	c.fallbackWorkspace()
}

func (c *VarwinClient) fallbackWorkspace() {
	if c.UserInfo != nil {
		if id := parseID(c.UserInfo["ownerWorkspaceId"]); id > 0 {
			c.WorkspaceID = id
			return
		}
	}
	if c.WorkspaceID == 0 {
		c.WorkspaceID = 3
	}
}

func (c *VarwinClient) GetServerInfo() (map[string]interface{}, error) {
	query := `
	query {
		serverInfo {
			appVersion
			defaultUserAuthorizationAllowed
		}
	}
	`
	data, err := c.ExecuteRaw(query, nil, false)
	if err != nil {
		return nil, err
	}

	info, _ := data["serverInfo"].(map[string]interface{})
	if info == nil {
		info = make(map[string]interface{})
	}

	_ = c.EnsureAuth()

	c.mu.RLock()
	info["url"] = c.BaseURL
	info["authenticated"] = c.AccessToken != ""
	info["activeWorkspaceId"] = c.WorkspaceID
	c.mu.RUnlock()

	return info, nil
}

func (c *VarwinClient) ListProjects(workspaceID int) ([]map[string]interface{}, error) {
	wsID := workspaceID
	if wsID == 0 {
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}
	if wsID == 0 {
		if err := c.EnsureAuth(); err != nil {
			return nil, err
		}
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}

	query := fmt.Sprintf(`
	query {
		projects(workspaceId: %d) {
			totalCount
			edges {
				node {
					id
					name
					guid
					mobileReady
					multiplayer
					author {
						name
					}
					scenes {
						id
						name
						sid
					}
				}
			}
		}
	}
	`, wsID)

	data, err := c.ExecuteRaw(query, nil, true)
	if err != nil {
		return nil, err
	}

	projectsData, ok := data["projects"].(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("unexpected projects response")
	}

	edges, ok := projectsData["edges"].([]interface{})
	if !ok {
		return []map[string]interface{}{}, nil
	}

	var results []map[string]interface{}
	for _, e := range edges {
		edgeMap, ok := e.(map[string]interface{})
		if !ok {
			continue
		}
		if node, ok := edgeMap["node"].(map[string]interface{}); ok {
			results = append(results, node)
		}
	}
	return results, nil
}

func (c *VarwinClient) GetProject(projectID int, workspaceID int) (map[string]interface{}, error) {
	projects, err := c.ListProjects(workspaceID)
	if err != nil {
		return nil, err
	}

	pIDStr := strconv.Itoa(projectID)
	for _, p := range projects {
		if fmt.Sprintf("%v", p["id"]) == pIDStr {
			return p, nil
		}
	}
	return nil, nil
}

func (c *VarwinClient) GetScene(sceneID int, workspaceID int) (map[string]interface{}, error) {
	wsID := workspaceID
	if wsID == 0 {
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}
	if wsID == 0 {
		if err := c.EnsureAuth(); err != nil {
			return nil, err
		}
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}

	query := fmt.Sprintf(`
	query {
		projects(workspaceId: %d) {
			edges {
				node {
					id
					name
					scenes {
						id
						name
						sid
						sceneObjects {
							id
							name
						}
						codeModules
						blocklyCodeModule
						autogeneratedCodeModules {
							sceneObjectsCodeModule
							sceneObjectTypesCodeModule
						}
					}
				}
			}
		}
	}
	`, wsID)

	data, err := c.ExecuteRaw(query, nil, true)
	if err != nil {
		return nil, err
	}

	projectsData, ok := data["projects"].(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("unexpected projects response")
	}

	edges, ok := projectsData["edges"].([]interface{})
	if !ok {
		return nil, nil
	}

	sIDStr := strconv.Itoa(sceneID)
	for _, e := range edges {
		edgeMap, ok := e.(map[string]interface{})
		if !ok {
			continue
		}
		node, ok := edgeMap["node"].(map[string]interface{})
		if !ok {
			continue
		}
		scenes, ok := node["scenes"].([]interface{})
		if !ok {
			continue
		}
		for _, s := range scenes {
			sceneMap, ok := s.(map[string]interface{})
			if !ok {
				continue
			}
			if parseID(sceneMap["id"]) == sceneID || fmt.Sprintf("%v", sceneMap["id"]) == sIDStr {
				sceneMap["projectId"] = node["id"]
				sceneMap["projectName"] = node["name"]
				return sceneMap, nil
			}
		}
	}
	return nil, nil
}

func (c *VarwinClient) ParseSceneObjects(sceneData map[string]interface{}) []SceneObject {
	auto, ok := sceneData["autogeneratedCodeModules"].(map[string]interface{})
	if !ok || auto == nil {
		return nil
	}
	code, ok := auto["sceneObjectsCodeModule"].(string)
	if !ok || code == "" {
		return nil
	}

	var objects []SceneObject
	lines := strings.Split(code, "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if strings.Contains(line, "=") && strings.Contains(line, "Wrapper(") {
			parts := strings.SplitN(line, "=", 2)
			if len(parts) == 2 {
				varName := strings.TrimSpace(parts[0])
				rightPart := strings.TrimSpace(parts[1])
				rightParts := strings.SplitN(rightPart, "(", 2)
				if len(rightParts) == 2 {
					objects = append(objects, SceneObject{
						VariableName: varName,
						WrapperType:  strings.TrimSpace(rightParts[0]),
					})
				}
			}
		}
	}
	return objects
}

func (c *VarwinClient) GetCodeModules(sceneID int) (map[string]string, error) {
	scene, err := c.GetScene(sceneID, 0)
	if err != nil {
		return nil, err
	}
	if scene == nil {
		return nil, fmt.Errorf("scene with ID %d not found", sceneID)
	}

	modules, ok := scene["codeModules"].(map[string]interface{})
	if !ok || modules == nil {
		return make(map[string]string), nil
	}

	res := make(map[string]string)
	for k, v := range modules {
		if s, ok := v.(string); ok {
			res[k] = s
		}
	}
	return res, nil
}

func (c *VarwinClient) UpdateCodeModules(sceneID int, codeModules map[string]string) (map[string]interface{}, error) {
	mutation := `
	mutation UpdateCode($input: UpdateCodeModulesInput!) {
		updateCodeModules(input: $input) {
			sceneId
			scene {
				id
				codeModules
			}
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"id":          sceneID,
			"codeModules": codeModules,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) CreateProject(name string, mobileReady bool, multiplayer bool, workspaceID int) (map[string]interface{}, error) {
	wsID := workspaceID
	if wsID == 0 {
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}
	if wsID == 0 {
		_ = c.EnsureAuth()
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}

	c.mu.RLock()
	authorName := "Varwin MCP Go"
	if c.UserInfo != nil {
		if fn, ok := c.UserInfo["fullName"].(string); ok && fn != "" {
			authorName = fn
		}
	}
	c.mu.RUnlock()

	mutation := `
	mutation CreateProj($input: CreateProjectInput!) {
		createProject(input: $input) {
			projectId
			project {
				id
				name
				guid
			}
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"workspaceId":                   strconv.Itoa(wsID),
			"name":                          name,
			"mobileReady":                   mobileReady,
			"multiplayer":                   multiplayer,
			"autoUpdateLibraryItemVersions": true,
			"author": map[string]interface{}{
				"name":    authorName,
				"company": "Varwin Community",
				"email":   "developer@varwin.local",
				"url":     "https://varwin.com",
			},
			"contentLicenseId": "1",
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) RenameProject(projectID int, newName string) (map[string]interface{}, error) {
	mutation := `
	mutation RenameProj($input: RenameProjectInput!) {
		renameProject(input: $input) {
			projectId
			project {
				id
				name
				guid
			}
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"id":   projectID,
			"name": newName,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) DuplicateProject(projectID int, newName string, workspaceID int) (map[string]interface{}, error) {
	wsID := workspaceID
	if wsID == 0 {
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}
	if wsID == 0 {
		_ = c.EnsureAuth()
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}

	mutation := `
	mutation DupProj($input: DuplicateProjectInput!) {
		duplicateProject(input: $input) {
			projectId
			project {
				id
				name
				guid
			}
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"workspaceId": strconv.Itoa(wsID),
			"id":          projectID,
			"name":        newName,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) DeleteProject(projectID int) (map[string]interface{}, error) {
	mutation := `
	mutation DelProj($input: DeleteProjectInput!) {
		deleteProject(input: $input) {
			projectId
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"id": projectID,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) CreateScene(projectID int, name string, sceneTemplateID int, lang string) (map[string]interface{}, error) {
	if lang == "" {
		lang = "ru"
	}
	mutation := `
	mutation CreateSc($input: CreateSceneInput!) {
		createScene(input: $input) {
			sceneId
			scene {
				id
				name
				sid
			}
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"projectId":       projectID,
			"name":            name,
			"sceneTemplateId": sceneTemplateID,
			"lang":            lang,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) RenameScene(sceneID int, newName string) (map[string]interface{}, error) {
	mutation := `
	mutation RenameSc($input: RenameSceneInput!) {
		renameScene(input: $input) {
			sceneId
			scene {
				id
				name
				sid
			}
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"id":   sceneID,
			"name": newName,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) DuplicateScene(sceneID int, targetProjectID int, newName string) (map[string]interface{}, error) {
	mutation := `
	mutation DupSc($input: DuplicateSceneInput!) {
		duplicateScene(input: $input) {
			sceneId
			scene {
				id
				name
				sid
			}
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"id":              sceneID,
			"targetProjectId": targetProjectID,
			"name":            newName,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) DeleteScene(sceneID int) (map[string]interface{}, error) {
	mutation := `
	mutation DelSc($input: DeleteSceneInput!) {
		deleteScene(input: $input) {
			sceneId
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"id": sceneID,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) ListSceneTemplates(workspaceID int) ([]map[string]interface{}, error) {
	wsID := workspaceID
	if wsID == 0 {
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}
	if wsID == 0 {
		_ = c.EnsureAuth()
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}

	query := fmt.Sprintf(`
	query {
		sceneTemplates(workspaceId: %d) {
			totalCount
			edges {
				node {
					id
					name {
						ru
						en
					}
					guid
					mobileReady
				}
			}
		}
	}
	`, wsID)

	data, err := c.ExecuteRaw(query, nil, true)
	if err != nil {
		return nil, err
	}

	st, _ := data["sceneTemplates"].(map[string]interface{})
	edges, _ := st["edges"].([]interface{})
	var results []map[string]interface{}
	for _, e := range edges {
		if em, ok := e.(map[string]interface{}); ok {
			if node, ok := em["node"].(map[string]interface{}); ok {
				results = append(results, node)
			}
		}
	}
	return results, nil
}

func (c *VarwinClient) ListLibraryObjects(workspaceID int, search string, limit int) ([]map[string]interface{}, int, error) {
	wsID := workspaceID
	if wsID == 0 {
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}
	if wsID == 0 {
		_ = c.EnsureAuth()
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}

	if limit <= 0 {
		limit = 50
	}

	searchClause := ""
	if search != "" {
		searchClause = fmt.Sprintf(`, search: "%s"`, strings.ReplaceAll(search, `"`, `\"`))
	}

	query := fmt.Sprintf(`
	query {
		objects(workspaceId: %d, first: %d%s) {
			totalCount
			edges {
				node {
					id
					name {
						ru
						en
					}
					guid
					mobileReady
				}
			}
		}
	}
	`, wsID, limit, searchClause)

	data, err := c.ExecuteRaw(query, nil, true)
	if err != nil {
		return nil, 0, err
	}

	objs, _ := data["objects"].(map[string]interface{})
	totalCount := parseID(objs["totalCount"])
	edges, _ := objs["edges"].([]interface{})
	var results []map[string]interface{}
	for _, e := range edges {
		if em, ok := e.(map[string]interface{}); ok {
			if node, ok := em["node"].(map[string]interface{}); ok {
				results = append(results, node)
			}
		}
	}
	return results, totalCount, nil
}

func (c *VarwinClient) ListResources(workspaceID int, limit int) ([]map[string]interface{}, int, error) {
	wsID := workspaceID
	if wsID == 0 {
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}
	if wsID == 0 {
		_ = c.EnsureAuth()
		c.mu.RLock()
		wsID = c.WorkspaceID
		c.mu.RUnlock()
	}

	if limit <= 0 {
		limit = 50
	}

	query := fmt.Sprintf(`
	query {
		resources(workspaceId: %d, first: %d) {
			totalCount
			edges {
				node {
					id
					name {
						ru
						en
					}
					guid
				}
			}
		}
	}
	`, wsID, limit)

	data, err := c.ExecuteRaw(query, nil, true)
	if err != nil {
		return nil, 0, err
	}

	resData, _ := data["resources"].(map[string]interface{})
	totalCount := parseID(resData["totalCount"])
	edges, _ := resData["edges"].([]interface{})
	var results []map[string]interface{}
	for _, e := range edges {
		if em, ok := e.(map[string]interface{}); ok {
			if node, ok := em["node"].(map[string]interface{}); ok {
				results = append(results, node)
			}
		}
	}
	return results, totalCount, nil
}

func (c *VarwinClient) GetBlockly(sceneID int) (map[string]interface{}, error) {
	scene, err := c.GetScene(sceneID, 0)
	if err != nil {
		return nil, err
	}
	if scene == nil {
		return nil, fmt.Errorf("scene %d not found", sceneID)
	}

	return map[string]interface{}{
		"sceneId":           sceneID,
		"blocklyCodeModule": scene["blocklyCodeModule"],
	}, nil
}

func (c *VarwinClient) UpdateBlockly(sceneID int, blocklyData interface{}, blocklyCodeModule string, usedObjectIDs []interface{}) (map[string]interface{}, error) {
	mutation := `
	mutation UpdateBlk($input: UpdateBlocklyInput!) {
		updateBlockly(input: $input) {
			sceneId
		}
	}
	`
	if usedObjectIDs == nil {
		usedObjectIDs = []interface{}{}
	}
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"id":                                sceneID,
			"blocklyData":                       blocklyData,
			"blocklyCodeModule":                 blocklyCodeModule,
			"sceneObjectInstanceIdsUsedInLogic": usedObjectIDs,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) UpdateSceneObjects(sceneID int, data interface{}, sceneObjects []interface{}, objectBehaviours []interface{}) (map[string]interface{}, error) {
	mutation := `
	mutation UpdateObjects($input: UpdateSceneObjectsInput!) {
		updateSceneObjects(input: $input) {
			sceneId
			scene {
				id
				name
			}
		}
	}
	`
	vars := map[string]interface{}{
		"input": map[string]interface{}{
			"id":               sceneID,
			"data":             data,
			"sceneObjects":     sceneObjects,
			"objectBehaviours": objectBehaviours,
		},
	}
	return c.ExecuteRaw(mutation, vars, true)
}

func (c *VarwinClient) GetSystemModule(locale string) (string, error) {
	if locale == "" {
		locale = "ru"
	}
	query := fmt.Sprintf(`
	query {
		varwinPythonModule(locale: "%s")
	}
	`, locale)
	data, err := c.ExecuteRaw(query, nil, true)
	if err != nil {
		return "", err
	}
	mod, _ := data["varwinPythonModule"].(string)
	return mod, nil
}

func (c *VarwinClient) AddSceneObject(sceneID int, objectID int, name string, varName string, x, y, z float64, rx, ry, rz float64, sx, sy, sz float64) (int, error) {
	homeDir, _ := os.UserHomeDir()
	dbPath := filepath.Join(homeDir, ".config", "VarwinData18", "SQLite3", "database.db")
	if _, err := os.Stat(dbPath); err != nil {
		return 0, fmt.Errorf("Varwin database not found at %s", dbPath)
	}

	if sx == 0 && sy == 0 && sz == 0 {
		sx, sy, sz = 1.0, 1.0, 1.0
	}

	script := `
import sqlite3, json, datetime, sys

db_path = sys.argv[1]
scene_id = int(sys.argv[2])
object_id = int(sys.argv[3])
name = sys.argv[4]
var_name = sys.argv[5]
x, y, z = float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8])
rx, ry, rz = float(sys.argv[9]), float(sys.argv[10]), float(sys.argv[11])
sx, sy, sz = float(sys.argv[12]), float(sys.argv[13]), float(sys.argv[14])

con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT MAX(instance_id), MAX(position) FROM scene_objects WHERE scene_id = ?", (scene_id,))
row = cur.fetchone()
max_inst = (row[0] or 0) + 1
max_pos = (row[1] or 0) + 1

data_json = json.dumps({
    "DisableSelectabilityInEditor": False,
    "Index": max_inst,
    "IsDisabled": False,
    "IsDisabledInHierarchy": False,
    "LocalTransform": {
        "PositionDT": {"x": x, "y": y, "z": z},
        "EulerAnglesDT": {"x": rx, "y": ry, "z": rz},
        "RotationDT": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0},
        "ScaleDT": {"x": sx, "y": sy, "z": sz}
    },
    "RootTransform": {
        "PositionDT": {"x": x, "y": y, "z": z},
        "EulerAnglesDT": {"x": rx, "y": ry, "z": rz},
        "RotationDT": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0},
        "ScaleDT": {"x": sx, "y": sy, "z": sz}
    },
    "InspectorPropertiesData": []
})

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

cur.execute("""
INSERT INTO scene_objects (
    scene_id, object_id, instance_id, position, name, variable_name,
    data, disable_scene_logic, used_in_scene_logic, created_at, updated_at,
    created_by, updated_by
) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?, 3, 3)
""", (scene_id, object_id, max_inst, max_pos, name, var_name, data_json, now, now))

con.commit()
print(cur.lastrowid)
`

	cmd := exec.Command("python3", "-c", script,
		dbPath,
		strconv.Itoa(sceneID),
		strconv.Itoa(objectID),
		name,
		varName,
		fmt.Sprintf("%f", x), fmt.Sprintf("%f", y), fmt.Sprintf("%f", z),
		fmt.Sprintf("%f", rx), fmt.Sprintf("%f", ry), fmt.Sprintf("%f", rz),
		fmt.Sprintf("%f", sx), fmt.Sprintf("%f", sy), fmt.Sprintf("%f", sz),
	)

	out, err := cmd.CombinedOutput()
	if err != nil {
		return 0, fmt.Errorf("failed to add scene object: %s (err: %w)", string(out), err)
	}

	newID, _ := strconv.Atoi(strings.TrimSpace(string(out)))
	return newID, nil
}

