package docs

import (
	"fmt"
	"os"
	"regexp"
	"sort"
	"strings"
)

type Section struct {
	ID        string
	Name      string
	ClassName string
	Content   string
}

type SearchResult struct {
	Name        string `json:"name"`
	ClassName   string `json:"class_name"`
	Score       int    `json:"score"`
	Snippet     string `json:"snippet"`
	TotalLength int    `json:"total_length"`
}

type VarwinDocsSearch struct {
	DocsPath string
	Sections []Section
}

var (
	reHeaderName = regexp.MustCompile(`_generated_(?:Varwin_)?([A-Za-z0-9_]+)`)
	reClassName  = regexp.MustCompile(`_class_\s+([A-Za-z0-9_.]+)`)
)

func NewVarwinDocsSearch(docsPath string) *VarwinDocsSearch {
	if docsPath == "" {
		// Look in typical project location
		candidates := []string{
			"/home/reg/Projects/NOVAT.varwin/docs/varwin18_python_api_full.md",
			"docs/varwin18_python_api_full.md",
			"../docs/varwin18_python_api_full.md",
		}
		for _, cand := range candidates {
			if _, err := os.Stat(cand); err == nil {
				docsPath = cand
				break
			}
		}
	}

	ds := &VarwinDocsSearch{DocsPath: docsPath}
	ds.loadAndIndex()
	return ds
}

func (d *VarwinDocsSearch) loadAndIndex() {
	if d.DocsPath == "" {
		return
	}
	data, err := os.ReadFile(d.DocsPath)
	if err != nil {
		return
	}

	content := string(data)
	rawSections := strings.Split(content, "########## ")

	for _, sec := range rawSections {
		sec = strings.TrimSpace(sec)
		if sec == "" {
			continue
		}

		lines := strings.Split(sec, "\n")
		header := strings.TrimSpace(lines[0])
		body := ""
		if len(lines) > 1 {
			body = strings.TrimSpace(strings.Join(lines[1:], "\n"))
		}

		name := header
		if m := reHeaderName.FindStringSubmatch(header); len(m) > 1 {
			name = m[1]
			name = strings.ReplaceAll(name, ".html.md", "")
			name = strings.ReplaceAll(name, ".md", "")
		}

		className := name
		if m := reClassName.FindStringSubmatch(body); len(m) > 1 {
			className = m[1]
		}

		d.Sections = append(d.Sections, Section{
			ID:        header,
			Name:      name,
			ClassName: className,
			Content:   body,
		})
	}
}

func (d *VarwinDocsSearch) ListWrappers() []string {
	seen := make(map[string]bool)
	var names []string

	for _, s := range d.Sections {
		cn := s.ClassName
		if cn != "" && !seen[cn] && !strings.HasPrefix(cn, "pages_") && !strings.HasPrefix(cn, "genindex") {
			seen[cn] = true
			names = append(names, cn)
		}
	}
	sort.Strings(names)
	return names
}

func (d *VarwinDocsSearch) GetWrapperDoc(name string) (string, bool) {
	nameLower := strings.ToLower(strings.ReplaceAll(name, "wrapper", ""))
	nameLower = strings.TrimSpace(nameLower)
	fullLower := strings.ToLower(name)

	for _, s := range d.Sections {
		sName := strings.ToLower(strings.ReplaceAll(s.Name, "wrapper", ""))
		sName = strings.TrimSpace(sName)
		sClass := strings.ToLower(s.ClassName)

		if nameLower == sName || fullLower == sClass || strings.Contains(sClass, nameLower) {
			return fmt.Sprintf("# %s\n\n%s", s.ClassName, s.Content), true
		}
	}
	return "", false
}

func (d *VarwinDocsSearch) Search(query string, limit int) []SearchResult {
	if limit <= 0 {
		limit = 5
	}

	termsRaw := strings.Fields(strings.ToLower(query))
	var terms []string
	for _, t := range termsRaw {
		if len(t) > 2 {
			terms = append(terms, t)
		}
	}
	if len(terms) == 0 {
		terms = []string{strings.ToLower(query)}
	}

	var results []SearchResult
	for _, s := range d.Sections {
		contentLower := strings.ToLower(s.Content)
		nameLower := strings.ToLower(s.Name)
		classLower := strings.ToLower(s.ClassName)

		score := 0
		for _, term := range terms {
			if strings.Contains(classLower, term) {
				score += 50
			}
			if strings.Contains(nameLower, term) {
				score += 30
			}
			cnt := strings.Count(contentLower, term)
			if cnt > 10 {
				cnt = 10
			}
			score += cnt * 2
		}

		if score > 0 {
			var snippetLines []string
			lines := strings.Split(s.Content, "\n")
			snippetLen := 0
			for _, line := range lines {
				lineLower := strings.ToLower(line)
				matched := false
				for _, term := range terms {
					if strings.Contains(lineLower, term) {
						matched = true
						break
					}
				}
				if matched {
					trimmed := strings.TrimSpace(line)
					snippetLines = append(snippetLines, trimmed)
					snippetLen += len(trimmed)
					if snippetLen > 300 {
						break
					}
				}
			}

			snippet := strings.Join(snippetLines, "\n")
			if snippet == "" && len(s.Content) > 0 {
				if len(s.Content) > 200 {
					snippet = s.Content[:200]
				} else {
					snippet = s.Content
				}
			}

			results = append(results, SearchResult{
				Name:        s.Name,
				ClassName:   s.ClassName,
				Score:       score,
				Snippet:     snippet,
				TotalLength: len(s.Content),
			})
		}
	}

	sort.Slice(results, func(i, j int) bool {
		return results[i].Score > results[j].Score
	})

	if len(results) > limit {
		return results[:limit]
	}
	return results
}
