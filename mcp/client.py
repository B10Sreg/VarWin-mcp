"""
Varwin 18 GraphQL API Client for Python & MCP.
Handles authentication, workspace resolution, queries, and mutations.
"""

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

logger = logging.getLogger("varwin-mcp.client")


class VarwinClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or os.environ.get("VARWIN_URL", "http://127.0.0.1:1801")).rstrip("/")
        self.endpoint = f"{self.base_url}/query"
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.workspace_id: Optional[int] = None
        self.user_info: Optional[Dict[str, Any]] = None

    def execute_raw(self, query: str, variables: Optional[Dict[str, Any]] = None, auth: bool = True) -> Dict[str, Any]:
        """Execute a GraphQL query or mutation."""
        if auth and not self.access_token:
            self.authenticate()

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "VarwinMCP/1.0",
        }
        if auth and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=data, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                result = json.loads(body)
            except Exception:
                raise RuntimeError(f"HTTP {e.code} error from Varwin Server: {body}")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Varwin Server at {self.endpoint}: {e}")

        if "errors" in result and result["errors"]:
            # Check for expired token
            error_codes = [err.get("extensions", {}).get("code") for err in result["errors"]]
            if "authorizationRequired" in error_codes and auth:
                # Retry authentication once
                self.authenticate()
                headers["Authorization"] = f"Bearer {self.access_token}"
                req = urllib.request.Request(self.endpoint, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
            elif result.get("data") is None:
                err_msg = "; ".join(e.get("message", "") for e in result["errors"])
                raise RuntimeError(f"GraphQL Error: {err_msg}")

        return result.get("data", {})

    def authenticate(self) -> str:
        """Login as default user and resolve the active workspace ID."""
        mutation = """
        mutation {
            loginAsDefaultUser(input: { clientInfo: "VarwinMCP" }) {
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
        """
        data = self.execute_raw(mutation, auth=False)
        auth_data = data.get("loginAsDefaultUser")
        if not auth_data:
            raise RuntimeError("Authentication failed: no loginAsDefaultUser response")

        self.access_token = auth_data["accessToken"]
        self.refresh_token = auth_data.get("refreshToken")
        self.user_info = auth_data.get("user")

        # Resolve active workspace
        self._resolve_workspace()
        return self.access_token

    def _resolve_workspace(self):
        """Query workspaceMembership to find the user's active workspace ID."""
        query = """
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
        """
        try:
            data = self.execute_raw(query, auth=True)
            edges = data.get("workspaceMembership", {}).get("edges", [])
            for edge in edges:
                node = edge.get("node", {})
                if node.get("state") == "active":
                    self.workspace_id = int(node["id"])
                    break
            if not self.workspace_id and edges:
                self.workspace_id = int(edges[0]["node"]["id"])
        except Exception:
            # Fallback to ownerWorkspaceId from user info
            if self.user_info and self.user_info.get("ownerWorkspaceId"):
                self.workspace_id = int(self.user_info["ownerWorkspaceId"])
            else:
                self.workspace_id = 1

    def get_server_info(self) -> Dict[str, Any]:
        """Get Varwin server info and status."""
        query = """
        query {
            serverInfo {
                appVersion
                defaultUserAuthorizationAllowed
            }
        }
        """
        data = self.execute_raw(query, auth=False)
        info = data.get("serverInfo", {})
        try:
            self.ensure_auth()
        except Exception:
            pass
        info["url"] = self.base_url
        info["authenticated"] = bool(self.access_token)
        info["activeWorkspaceId"] = self.workspace_id
        return info

    def list_projects(self, workspace_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all projects in the workspace."""
        ws_id = workspace_id or self.workspace_id
        if not ws_id:
            self.authenticate()
            ws_id = self.workspace_id

        query = f"""
        query {{
            projects(workspaceId: {ws_id}) {{
                totalCount
                edges {{
                    node {{
                        id
                        name
                        guid
                        mobileReady
                        multiplayer
                        author {{
                            name
                        }}
                        scenes {{
                            id
                            name
                            sid
                        }}
                    }}
                }}
            }}
        }}
        """
        data = self.execute_raw(query, auth=True)
        edges = data.get("projects", {}).get("edges", [])
        return [edge["node"] for edge in edges]

    def get_project(self, project_id: int, workspace_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Get detailed info about a project by its numeric ID."""
        projects = self.list_projects(workspace_id=workspace_id)
        for p in projects:
            if p["id"] == project_id or str(p["id"]) == str(project_id):
                return p
        return None

    def get_scene(self, scene_id: int, workspace_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Fetch full details for a specific scene including objects and code modules."""
        ws_id = workspace_id or self.workspace_id
        query = f"""
        query {{
            projects(workspaceId: {ws_id}) {{
                edges {{
                    node {{
                        id
                        name
                        scenes {{
                            id
                            name
                            sid
                            sceneObjects {{
                                id
                                name
                            }}
                            codeModules
                            blocklyCodeModule
                            autogeneratedCodeModules {{
                                sceneObjectsCodeModule
                                sceneObjectTypesCodeModule
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
        data = self.execute_raw(query, auth=True)
        edges = data.get("projects", {}).get("edges", [])
        for edge in edges:
            project = edge["node"]
            for scene in project.get("scenes", []):
                if scene["id"] == scene_id or str(scene["id"]) == str(scene_id):
                    scene["projectId"] = project["id"]
                    scene["projectName"] = project["name"]
                    return scene
        return None

    def parse_scene_objects(self, scene_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Parse autogeneratedCodeModules to extract variable names and wrapper types."""
        auto = scene_data.get("autogeneratedCodeModules", {}) or {}
        code = auto.get("sceneObjectsCodeModule", "")
        objects = []
        for line in code.splitlines():
            line = line.strip()
            # Format: varName = TypeWrapper(Varwin.Objects.GetObjectByVarName("varName"))
            if "=" in line and "Wrapper(" in line:
                try:
                    left, right = line.split("=", 1)
                    var_name = left.strip()
                    type_part = right.split("(", 1)[0].strip()
                    objects.append({
                        "variable_name": var_name,
                        "wrapper_type": type_part,
                    })
                except Exception:
                    pass
        return objects

    def get_code_modules(self, scene_id: int) -> Dict[str, str]:
        """Return the dictionary of Python code modules (e.g. {'Main.py': '...'}) for a scene."""
        scene = self.get_scene(scene_id)
        if not scene:
            raise ValueError(f"Scene with ID {scene_id} not found")
        modules = scene.get("codeModules")
        if isinstance(modules, dict):
            return modules
        return {}

    def update_code_modules(self, scene_id: int, code_modules: Dict[str, str]) -> Dict[str, Any]:
        """Update or create Python code modules for a scene."""
        mutation = """
        mutation UpdateCode($input: UpdateCodeModulesInput!) {
            updateCodeModules(input: $input) {
                sceneId
                scene {
                    id
                    codeModules
                }
            }
        }
        """
        variables = {
            "input": {
                "id": int(scene_id),
                "codeModules": code_modules,
            }
        }
        return self.execute_raw(mutation, variables=variables, auth=True)

    def create_project(self, name: str, mobile_ready: bool = True, multiplayer: bool = False, workspace_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a new project in the workspace."""
        ws_id = workspace_id or self.workspace_id
        mutation = """
        mutation CreateProj($input: CreateProjectInput!) {
            createProject(input: $input) {
                id
                name
                guid
            }
        }
        """
        variables = {
            "input": {
                "workspaceId": str(ws_id),
                "name": name,
                "mobileReady": mobile_ready,
                "multiplayer": multiplayer,
                "autoUpdateLibraryItemVersions": True,
                "author": {
                    "name": self.user_info.get("fullName", "Varwin MCP") if self.user_info else "Varwin MCP"
                },
                "contentLicenseId": "1",
            }
        }
        return self.execute_raw(mutation, variables=variables, auth=True)
