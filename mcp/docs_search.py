"""
Fast search and lookup for Varwin 18 Python API documentation.
Parses and indexes docs/varwin18_python_api_full.md.
"""

import os
import re
from typing import Any, Dict, List, Optional


class VarwinDocsSearch:
    def __init__(self, docs_path: Optional[str] = None):
        if not docs_path:
            # Look relative to workspace or known path
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            docs_path = os.path.join(base_dir, "docs", "varwin18_python_api_full.md")
        self.docs_path = docs_path
        self.sections: List[Dict[str, Any]] = []
        self._load_and_index()

    def _load_and_index(self):
        if not os.path.isfile(self.docs_path):
            return

        with open(self.docs_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Split by section headers: "########## _generated_..."
        raw_sections = content.split("########## ")
        for sec in raw_sections:
            sec = sec.strip()
            if not sec:
                continue

            lines = sec.splitlines()
            header = lines[0].strip()
            body = "\n".join(lines[1:]).strip()

            # Extract clean class/topic name
            name = header
            m = re.search(r"_generated_(?:Varwin_)?([A-Za-z0-9_]+)", header)
            if m:
                name = m.group(1).replace(".html.md", "").replace(".md", "")

            # Look for class name in body
            class_match = re.search(r"_class_\s+([A-Za-z0-9_.]+)", body)
            class_name = class_match.group(1) if class_match else name

            self.sections.append({
                "id": header,
                "name": name,
                "class_name": class_name,
                "content": body,
            })

    def list_wrappers(self) -> List[str]:
        """List all wrapper and behaviour names in the API documentation."""
        names = []
        for s in self.sections:
            cn = s["class_name"]
            if cn and cn not in names and not cn.startswith("pages_") and not cn.startswith("genindex"):
                names.append(cn)
        return sorted(names)

    def get_wrapper_doc(self, name: str) -> Optional[str]:
        """Get full documentation for a specific wrapper or behaviour (e.g. PlayerWrapper, MotionBehaviour)."""
        name_lower = name.lower().replace("wrapper", "").strip()
        for s in self.sections:
            s_name = s["name"].lower().replace("wrapper", "").strip()
            s_class = s["class_name"].lower()
            if name_lower == s_name or name.lower() == s["class_name"].lower() or name_lower in s_class:
                return f"# {s['class_name']}\n\n{s['content']}"
        return None

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search the documentation for keywords (methods, events, parameters)."""
        query_terms = [t.lower() for t in query.split() if len(t) > 2]
        if not query_terms:
            query_terms = [query.lower()]

        results = []
        for s in self.sections:
            content_lower = s["content"].lower()
            name_lower = s["name"].lower()
            class_lower = s["class_name"].lower()

            score = 0
            for term in query_terms:
                if term in class_lower:
                    score += 50
                if term in name_lower:
                    score += 30
                # Count occurrences in body
                cnt = content_lower.count(term)
                score += min(cnt * 2, 20)

            if score > 0:
                # Find matching snippet
                snippet = ""
                for line in s["content"].splitlines():
                    if any(t in line.lower() for t in query_terms):
                        snippet += line.strip() + "\n"
                        if len(snippet) > 300:
                            break

                results.append({
                    "name": s["name"],
                    "class_name": s["class_name"],
                    "score": score,
                    "snippet": snippet.strip() or s["content"][:200],
                    "total_length": len(s["content"]),
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
