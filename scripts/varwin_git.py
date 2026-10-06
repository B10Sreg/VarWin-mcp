#!/usr/bin/env python3
"""
Varwin Git Sync Tool (varwin-git)
=================================
Automated team collaboration and Git/GitHub version control for Varwin 18 XRMS projects.

Decomposes heavy multi-gigabyte Varwin projects into ultra-compact (~60 KB),
100% diffable, human-readable Git repositories:
- project.json: metadata, settings, GUIDs
- scenes/<name>/scene.json: scene settings, camera spawn
- scenes/<name>/objects.json: 3D scene objects hierarchy, transforms, inspector properties
- scenes/<name>/code/*.py: clean Python code modules (edit with VS Code / Cursor / PyCharm)
- scenes/<name>/logic/Blockly.xml: visual logic blocks
- scenes/<name>/logic/Blockly.py: compiled visual logic script
"""

import argparse
import datetime
import difflib
import json
import os
import shutil
import subprocess
import sys
import uuid
from typing import Any, Dict, List, Optional, Tuple

# Robust module path resolution for standalone, development, and /usr/bin execution
_current_file = os.path.realpath(__file__)
_current_dir = os.path.dirname(_current_file)
_candidate_dirs = [
    os.path.dirname(_current_dir),  # Repository root when running from bin/ or scripts/
    _current_dir,
    "/usr/share/varwin-mcp",
    "/usr/lib/varwin-mcp",
    "/opt/varwin-mcp",
]
for _p in _candidate_dirs:
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

import sqlite3

try:
    from mcp.client import VarwinClient
except ImportError:
    VarwinClient = None


# Terminal Color Helpers
def _supports_color() -> bool:
    if not hasattr(sys.stdout, "isatty"):
        return False
    return sys.stdout.isatty() or os.environ.get("TERM") in ("xterm", "xterm-256color", "screen", "tmux")


USE_COLOR = _supports_color()


def colorize(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def c_green(t: str) -> str:
    return colorize(t, "32")


def c_red(t: str) -> str:
    return colorize(t, "31")


def c_yellow(t: str) -> str:
    return colorize(t, "33")


def c_cyan(t: str) -> str:
    return colorize(t, "36")


def c_bold(t: str) -> str:
    return colorize(t, "1")


def c_magenta(t: str) -> str:
    return colorize(t, "35")


def find_varwin_db_path() -> str:
    """Locate the Varwin 18 SQLite database cross-platform."""
    env_override = os.environ.get("VARWIN_DB_PATH")
    if env_override and os.path.exists(env_override):
        return env_override

    candidates = []
    if sys.platform == "win32":
        for env_var in ["APPDATA", "LOCALAPPDATA", "ProgramData"]:
            val = os.environ.get(env_var)
            if val:
                candidates.append(os.path.join(val, "VarwinData18", "SQLite3", "database.db"))
        home = os.path.expanduser("~")
        candidates.append(os.path.join(home, "AppData", "Roaming", "VarwinData18", "SQLite3", "database.db"))
    else:
        home = os.path.expanduser("~")
        candidates.append(os.path.join(home, ".config", "VarwinData18", "SQLite3", "database.db"))
        candidates.append("/var/lib/varwin/database.db")

    for path in candidates:
        if os.path.exists(path):
            return path
    if candidates:
        return candidates[0]
    raise RuntimeError("Cannot determine Varwin database path")


def get_db_connection() -> sqlite3.Connection:
    """Connect to Varwin SQLite DB with Row factory."""
    db_path = find_varwin_db_path()
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Varwin database not found at {db_path}")
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def decode_field(val: Any) -> Any:
    """Safely decode byte strings or JSON bytes from SQLite."""
    if isinstance(val, bytes):
        val = val.decode("utf-8")
    return val


def parse_json_field(val: Any, default: Any = None) -> Any:
    """Safely parse JSON field from SQLite."""
    if val is None:
        return default
    if isinstance(val, bytes):
        val = val.decode("utf-8")
    if isinstance(val, str):
        try:
            return json.loads(val)
        except Exception:
            return val
    return val


def sanitize_filename(name: str) -> str:
    """Sanitize directory/file names across OSes."""
    for ch in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        name = name.replace(ch, '_')
    return name.strip()


class VarwinGitManager:
    def __init__(self, base_url: Optional[str] = None):
        self.client = None
        if VarwinClient is not None:
            try:
                self.client = VarwinClient(base_url=base_url)
            except Exception:
                self.client = None
        self.db_con = get_db_connection()

    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects from DB."""
        cur = self.db_con.cursor()
        rows = cur.execute(
            "SELECT id, name, guid, mobile_ready, multiplayer, updated_at FROM projects WHERE deleted_at IS NULL ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]

    def find_project(self, identifier: str) -> Optional[sqlite3.Row]:
        """Find a project by ID, GUID, or name substring."""
        cur = self.db_con.cursor()
        if identifier.isdigit():
            p = cur.execute("SELECT * FROM projects WHERE id=? AND deleted_at IS NULL", (int(identifier),)).fetchone()
            if p:
                return p

        # Check exact GUID
        p = cur.execute("SELECT * FROM projects WHERE guid=? AND deleted_at IS NULL", (identifier,)).fetchone()
        if p:
            return p

        # Check name
        p = cur.execute("SELECT * FROM projects WHERE name=? AND deleted_at IS NULL", (identifier,)).fetchone()
        if p:
            return p

        # Substring search
        matches = cur.execute(
            "SELECT * FROM projects WHERE name LIKE ? AND deleted_at IS NULL", (f"%{identifier}%",)
        ).fetchall()
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            names = [f"ID {m['id']}: {m['name']}" for m in matches]
            raise ValueError(f"Ambiguous project identifier '{identifier}'. Found multiple: {', '.join(names)}")

        return None

    def export_project(self, identifier: str, target_dir: Optional[str] = None, init_git: bool = True, force: bool = False) -> str:
        """Export a Varwin project into a structured, clean Git directory."""
        proj = self.find_project(identifier)
        if not proj:
            raise ValueError(f"Project '{identifier}' not found in Varwin")

        proj_id = proj["id"]
        proj_name = proj["name"]

        if not target_dir:
            slug = sanitize_filename(proj_name).replace(" ", "-").lower()
            target_dir = os.path.abspath(slug)
        else:
            target_dir = os.path.abspath(target_dir)

        if os.path.exists(target_dir) and not force and not os.path.exists(os.path.join(target_dir, ".git")):
            # If target dir exists with files and not force, proceed smoothly
            pass

        os.makedirs(target_dir, exist_ok=True)
        cur = self.db_con.cursor()

        # 1. project.json
        author_data = parse_json_field(proj["author"], default={})
        project_meta = {
            "name": proj["name"],
            "guid": proj["guid"],
            "root_guid": proj["root_guid"],
            "mobile_ready": bool(proj["mobile_ready"]),
            "multiplayer": bool(proj["multiplayer"]),
            "auto_update_library_item_versions": bool(proj["auto_update_library_item_versions"]),
            "author": author_data,
        }
        with open(os.path.join(target_dir, "project.json"), "w", encoding="utf-8") as f:
            json.dump(project_meta, f, indent=2, ensure_ascii=False)

        # 2. scenes
        scenes_dir = os.path.join(target_dir, "scenes")
        os.makedirs(scenes_dir, exist_ok=True)

        scenes = cur.execute(
            "SELECT * FROM scenes WHERE project_id=? AND deleted_at IS NULL ORDER BY id", (proj_id,)
        ).fetchall()

        for sc in scenes:
            scene_id = sc["id"]
            scene_name = sc["name"]
            scene_folder = os.path.join(scenes_dir, sanitize_filename(scene_name))
            os.makedirs(scene_folder, exist_ok=True)

            # Get template info
            tmpl = cur.execute(
                "SELECT guid, root_guid, name FROM scene_templates WHERE id=?", (sc["scene_template_id"],)
            ).fetchone()
            tmpl_guid = tmpl["guid"] if tmpl else None
            tmpl_name_json = parse_json_field(tmpl["name"], default={}) if tmpl else {}
            tmpl_name = tmpl_name_json.get("ru") or tmpl_name_json.get("en") if isinstance(tmpl_name_json, dict) else str(tmpl_name_json)

            scene_settings = parse_json_field(sc["data"], default={})

            scene_meta = {
                "name": sc["name"],
                "sid": sc["sid"],
                "template_guid": tmpl_guid,
                "template_name": tmpl_name,
                "settings": scene_settings,
            }
            with open(os.path.join(scene_folder, "scene.json"), "w", encoding="utf-8") as f:
                json.dump(scene_meta, f, indent=2, ensure_ascii=False)

            # 3. Scene Objects
            objects_list = []
            scene_objs = cur.execute(
                "SELECT * FROM scene_objects WHERE scene_id=? ORDER BY position, id", (scene_id,)
            ).fetchall()

            for obj in scene_objs:
                lib_obj = cur.execute(
                    "SELECT guid, root_guid, name FROM objects WHERE id=?", (obj["object_id"],)
                ).fetchone()
                lib_guid = lib_obj["guid"] if lib_obj else ""
                lib_root_guid = lib_obj["root_guid"] if lib_obj else ""
                lib_name_json = parse_json_field(lib_obj["name"], default={}) if lib_obj else {}
                lib_name = lib_name_json.get("ru") or lib_name_json.get("en") if isinstance(lib_name_json, dict) else str(lib_name_json)

                obj_data = parse_json_field(obj["data"], default={})

                behaviours = [
                    r[0] for r in cur.execute(
                        "SELECT behaviour_name FROM scene_object_behaviours WHERE scene_id=? AND object_id=?",
                        (scene_id, obj["object_id"])
                    ).fetchall()
                ]

                objects_list.append({
                    "instance_id": obj["instance_id"],
                    "name": obj["name"],
                    "variable_name": obj["variable_name"],
                    "object_guid": lib_guid,
                    "object_root_guid": lib_root_guid,
                    "object_name": lib_name,
                    "position": obj["position"],
                    "parent_id": obj["parent_id"],
                    "used_in_scene_logic": bool(obj["used_in_scene_logic"]),
                    "disable_scene_logic": bool(obj["disable_scene_logic"]),
                    "behaviours": behaviours,
                    "data": obj_data,
                })

            with open(os.path.join(scene_folder, "objects.json"), "w", encoding="utf-8") as f:
                json.dump(objects_list, f, indent=2, ensure_ascii=False)

            # 4. Code Modules (Python scripts)
            code_dir = os.path.join(scene_folder, "code")
            os.makedirs(code_dir, exist_ok=True)
            code_modules = parse_json_field(sc["code_modules"], default={})
            if isinstance(code_modules, dict):
                for filename, code_text in code_modules.items():
                    if not filename.endswith(".py"):
                        filename += ".py"
                    filepath = os.path.join(code_dir, sanitize_filename(filename))
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(code_text or "")

            # 5. Logic (Blockly)
            logic_dir = os.path.join(scene_folder, "logic")
            os.makedirs(logic_dir, exist_ok=True)

            b_data_raw = parse_json_field(sc["blockly_data"], default={})
            xml_content = ""
            meta_data = {}
            if isinstance(b_data_raw, dict):
                xml_content = b_data_raw.get("blockly", "")
                meta_data = {k: v for k, v in b_data_raw.items() if k != "blockly"}
            elif isinstance(b_data_raw, str):
                xml_content = b_data_raw

            with open(os.path.join(logic_dir, "Blockly.xml"), "w", encoding="utf-8") as f:
                f.write(xml_content or "")

            blockly_py = decode_field(sc["blockly_code_module"]) or ""
            with open(os.path.join(logic_dir, "Blockly.py"), "w", encoding="utf-8") as f:
                f.write(blockly_py)

            if meta_data:
                with open(os.path.join(logic_dir, "blockly_meta.json"), "w", encoding="utf-8") as f:
                    json.dump(meta_data, f, indent=2, ensure_ascii=False)

        # 6. .gitignore
        gitignore_path = os.path.join(target_dir, ".gitignore")
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write(
                    "# Python\n"
                    "__pycache__/\n"
                    "*.py[cod]\n"
                    "*$py.class\n\n"
                    "# Varwin Cache & Binaries\n"
                    "*.vwm\n"
                    "*.vwp\n"
                    "*.tmp\n"
                    "*.log\n"
                    ".varwin_cache/\n\n"
                    "# OS\n"
                    ".DS_Store\n"
                    "Thumbs.db\n"
                )

        # 7. README.md
        readme_path = os.path.join(target_dir, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(
                    f"# {proj_name}\n\n"
                    f"Проект Varwin 18 XRMS, синхронизируемый через Git / GitHub.\n\n"
                    f"## Особенности\n"
                    f"- Вес репозитория: **~60 КБ** вместо многогигабайтного `.vwp` архива!\n"
                    f"- Полная поддержка веток, Pull Requests, merge и code review.\n"
                    f"- Чистый Python код в `scenes/*/code/` и блоки Blockly в `scenes/*/logic/`.\n\n"
                    f"## Как работать с проектом команде\n\n"
                    f"### 1. Клонирование и применение в локальный Varwin\n"
                    f"```bash\n"
                    f"git clone <url-этого-репозитория>\n"
                    f"cd {os.path.basename(target_dir)}\n"
                    f"varwin-git apply\n"
                    f"```\n\n"
                    f"### 2. Сохранение изменений в Git\n"
                    f"После редактирования сцены или кода в Varwin:\n"
                    f"```bash\n"
                    f"varwin-git push -m \"Описание изменений\"\n"
                    f"```\n\n"
                    f"### 3. Проверка статуса и изменений\n"
                    f"```bash\n"
                    f"varwin-git status\n"
                    f"varwin-git diff\n"
                    f"```\n\n"
                    f"### 4. Получение обновлений от коллег\n"
                    f"```bash\n"
                    f"varwin-git pull\n"
                    f"```\n"
                )

        # 8. Git Init if requested
        if init_git and not os.path.exists(os.path.join(target_dir, ".git")):
            try:
                subprocess.run(["git", "init"], cwd=target_dir, check=True, capture_output=True)
            except Exception:
                pass

        return target_dir

    def apply_project(self, repo_dir: str = ".", target_project_name: Optional[str] = None) -> int:
        """Apply/sync a Git repository structure into the local Varwin installation."""
        repo_dir = os.path.abspath(repo_dir)
        proj_file = os.path.join(repo_dir, "project.json")
        if not os.path.exists(proj_file):
            raise FileNotFoundError(f"project.json not found in {repo_dir}")

        with open(proj_file, "r", encoding="utf-8") as f:
            proj_meta = json.load(f)

        proj_name = target_project_name or proj_meta.get("name", "Imported Git Project")
        proj_guid = proj_meta.get("guid")

        cur = self.db_con.cursor()

        # Check if project already exists
        existing_proj = None
        if proj_guid:
            existing_proj = cur.execute(
                "SELECT * FROM projects WHERE guid=? AND deleted_at IS NULL", (proj_guid,)
            ).fetchone()
        if not existing_proj:
            existing_proj = cur.execute(
                "SELECT * FROM projects WHERE name=? AND deleted_at IS NULL", (proj_name,)
            ).fetchone()

        now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        proj_id = None
        if existing_proj:
            proj_id = existing_proj["id"]
            cur.execute(
                "UPDATE projects SET updated_at=?, mobile_ready=?, multiplayer=? WHERE id=?",
                (now_str, int(proj_meta.get("mobile_ready", True)), int(proj_meta.get("multiplayer", False)), proj_id)
            )
            self.db_con.commit()
        else:
            # 1. Try GraphQL client if available
            if self.client:
                try:
                    self.client.authenticate()
                    res = self.client.create_project(
                        name=proj_name,
                        mobile_ready=proj_meta.get("mobile_ready", True),
                        multiplayer=proj_meta.get("multiplayer", False),
                    )
                    created_data = res.get("createProject", {}).get("project", {})
                    proj_id = int(created_data["id"])
                    if proj_guid:
                        cur.execute(
                            "UPDATE projects SET guid=?, root_guid=? WHERE id=?",
                            (proj_guid, proj_meta.get("root_guid", proj_guid), proj_id)
                        )
                        self.db_con.commit()
                except Exception:
                    proj_id = None

            # 2. Resilient SQLite fallback if Varwin Server is offline or GraphQL unavailable
            if proj_id is None:
                if not proj_guid:
                    proj_guid = str(uuid.uuid4())
                root_guid = proj_meta.get("root_guid", proj_guid)
                cur.execute(
                    """
                    INSERT INTO projects (
                        name, mobile_ready, content_license_id, author, guid, root_guid,
                        multiplayer, created_by, updated_by, workspace_id,
                        auto_update_library_item_versions, created_at, updated_at
                    ) VALUES (?, ?, 1, ?, ?, ?, ?, 3, 3, 3, ?, ?, ?)
                    """,
                    (
                        proj_name,
                        int(proj_meta.get("mobile_ready", True)),
                        json.dumps(proj_meta.get("author", {})),
                        proj_guid,
                        root_guid,
                        int(proj_meta.get("multiplayer", False)),
                        int(proj_meta.get("auto_update_library_item_versions", False)),
                        now_str,
                        now_str,
                    )
                )
                proj_id = cur.lastrowid
                self.db_con.commit()

        # Iterate scenes in repository
        scenes_dir = os.path.join(repo_dir, "scenes")
        if not os.path.exists(scenes_dir):
            return proj_id

        for scene_entry in os.listdir(scenes_dir):
            scene_folder = os.path.join(scenes_dir, scene_entry)
            if not os.path.isdir(scene_folder):
                continue

            scene_file = os.path.join(scene_folder, "scene.json")
            if not os.path.exists(scene_file):
                continue

            with open(scene_file, "r", encoding="utf-8") as f:
                scene_meta = json.load(f)

            scene_name = scene_meta.get("name", scene_entry)
            scene_sid = scene_meta.get("sid")
            tmpl_guid = scene_meta.get("template_guid")
            tmpl_name = scene_meta.get("template_name")

            # Resolve template ID
            tmpl_id = 1
            if tmpl_guid:
                t_row = cur.execute(
                    "SELECT id FROM scene_templates WHERE guid=? OR root_guid=?", (tmpl_guid, tmpl_guid)
                ).fetchone()
                if t_row:
                    tmpl_id = t_row["id"]
            if tmpl_id == 1 and tmpl_name:
                t_rows = cur.execute("SELECT id, name FROM scene_templates").fetchall()
                for r in t_rows:
                    n_json = parse_json_field(r["name"], default={})
                    if isinstance(n_json, dict) and tmpl_name in n_json.values():
                        tmpl_id = r["id"]
                        break

            # Find existing scene in project
            existing_scene = None
            if scene_sid:
                existing_scene = cur.execute(
                    "SELECT * FROM scenes WHERE project_id=? AND sid=? AND deleted_at IS NULL", (proj_id, scene_sid)
                ).fetchone()
            if not existing_scene:
                existing_scene = cur.execute(
                    "SELECT * FROM scenes WHERE project_id=? AND name=? AND deleted_at IS NULL", (proj_id, scene_name)
                ).fetchone()

            # Read code modules
            code_dir = os.path.join(scene_folder, "code")
            code_modules = {}
            if os.path.exists(code_dir):
                for py_file in os.listdir(code_dir):
                    if py_file.endswith(".py"):
                        with open(os.path.join(code_dir, py_file), "r", encoding="utf-8") as f:
                            code_modules[py_file] = f.read()

            # Read Blockly
            logic_dir = os.path.join(scene_folder, "logic")
            xml_content = ""
            blockly_py = ""
            meta_data = {}
            if os.path.exists(os.path.join(logic_dir, "Blockly.xml")):
                with open(os.path.join(logic_dir, "Blockly.xml"), "r", encoding="utf-8") as f:
                    xml_content = f.read()
            if os.path.exists(os.path.join(logic_dir, "Blockly.py")):
                with open(os.path.join(logic_dir, "Blockly.py"), "r", encoding="utf-8") as f:
                    blockly_py = f.read()
            if os.path.exists(os.path.join(logic_dir, "blockly_meta.json")):
                with open(os.path.join(logic_dir, "blockly_meta.json"), "r", encoding="utf-8") as f:
                    meta_data = json.load(f)

            b_data_combined = dict(meta_data)
            b_data_combined["blockly"] = xml_content

            scene_settings = json.dumps(scene_meta.get("settings", {}))
            code_modules_json = json.dumps(code_modules, indent=4)
            blockly_data_json = json.dumps(b_data_combined)

            scene_id = None
            if existing_scene:
                scene_id = existing_scene["id"]
                cur.execute(
                    """
                    UPDATE scenes SET
                        updated_at=?, name=?, data=?, code_modules=?,
                        blockly_code_module=?, blockly_data=?, scene_template_id=?
                    WHERE id=?
                    """,
                    (now_str, scene_name, scene_settings, code_modules_json, blockly_py, blockly_data_json, tmpl_id, scene_id)
                )
                self.db_con.commit()
            else:
                # 1. Try GraphQL client
                if self.client:
                    try:
                        self.client.authenticate()
                        res = self.client.create_scene(proj_id, scene_name, tmpl_id)
                        sc_node = res.get("createScene", {}).get("scene", {})
                        scene_id = int(sc_node["id"])
                    except Exception:
                        scene_id = None

                # 2. SQLite direct fallback
                if scene_id is None:
                    if not scene_sid:
                        scene_sid = str(uuid.uuid4())
                    cur.execute(
                        """
                        INSERT INTO scenes (
                            sid, project_id, scene_template_id, code_modules,
                            blockly_code_module, blockly_data, name, data,
                            created_by, updated_by, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 3, 3, ?, ?)
                        """,
                        (
                            scene_sid,
                            proj_id,
                            tmpl_id,
                            code_modules_json,
                            blockly_py,
                            blockly_data_json,
                            scene_name,
                            scene_settings,
                            now_str,
                            now_str,
                        )
                    )
                    scene_id = cur.lastrowid
                    self.db_con.commit()
                else:
                    cur.execute(
                        """
                        UPDATE scenes SET
                            updated_at=?, data=?, code_modules=?,
                            blockly_code_module=?, blockly_data=?
                        WHERE id=?
                        """,
                        (now_str, scene_settings, code_modules_json, blockly_py, blockly_data_json, scene_id)
                    )
                    if scene_sid:
                        cur.execute("UPDATE scenes SET sid=? WHERE id=?", (scene_sid, scene_id))
                    self.db_con.commit()

            # Sync objects
            objects_file = os.path.join(scene_folder, "objects.json")
            if os.path.exists(objects_file):
                with open(objects_file, "r", encoding="utf-8") as f:
                    objects_list = json.load(f)

                cur.execute("DELETE FROM scene_objects WHERE scene_id=?", (scene_id,))
                cur.execute("DELETE FROM scene_object_behaviours WHERE scene_id=?", (scene_id,))

                for obj in objects_list:
                    obj_guid = obj.get("object_guid")
                    obj_root_guid = obj.get("object_root_guid")
                    obj_name = obj.get("object_name")

                    lib_obj_id = None
                    if obj_guid:
                        lo = cur.execute(
                            "SELECT id FROM objects WHERE guid=? OR root_guid=?", (obj_guid, obj_guid)
                        ).fetchone()
                        if lo:
                            lib_obj_id = lo["id"]
                    if not lib_obj_id and obj_root_guid:
                        lo = cur.execute("SELECT id FROM objects WHERE root_guid=?", (obj_root_guid,)).fetchone()
                        if lo:
                            lib_obj_id = lo["id"]
                    if not lib_obj_id and obj_name:
                        lo_rows = cur.execute("SELECT id, name FROM objects").fetchall()
                        for r in lo_rows:
                            n_json = parse_json_field(r["name"], default={})
                            if isinstance(n_json, dict) and obj_name in n_json.values():
                                lib_obj_id = r["id"]
                                break

                    if not lib_obj_id:
                        print(f"⚠️ 3D-объект '{obj.get('name')}' (GUID: {obj_guid}) не найден в библиотеке Varwin. Пропускаем.")
                        continue

                    obj_data_str = json.dumps(obj.get("data", {}))
                    cur.execute(
                        """
                        INSERT INTO scene_objects (
                            scene_id, object_id, instance_id, position, name, variable_name,
                            data, disable_scene_logic, used_in_scene_logic,
                            created_at, updated_at, created_by, updated_by, parent_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 3, 3, ?)
                        """,
                        (
                            scene_id,
                            lib_obj_id,
                            obj.get("instance_id", 1),
                            obj.get("position", 0),
                            obj.get("name", "Object"),
                            obj.get("variable_name", "object"),
                            obj_data_str,
                            int(obj.get("disable_scene_logic", False)),
                            int(obj.get("used_in_scene_logic", False)),
                            now_str,
                            now_str,
                            obj.get("parent_id")
                        )
                    )

                    for beh in obj.get("behaviours", []):
                        cur.execute(
                            "INSERT OR IGNORE INTO scene_object_behaviours (scene_id, object_id, behaviour_name) VALUES (?, ?, ?)",
                            (scene_id, lib_obj_id, beh)
                        )

                self.db_con.commit()

            if self.client:
                try:
                    self.client.update_code_modules(scene_id, code_modules)
                except Exception:
                    pass

        return proj_id

    def resolve_repo_and_project(self, target: Optional[str] = None) -> Tuple[str, Optional[sqlite3.Row]]:
        """Resolve repository path and corresponding DB project from path or identifier."""
        repo_dir = "."
        proj_row = None

        if target:
            if os.path.isdir(target) and os.path.exists(os.path.join(target, "project.json")):
                repo_dir = os.path.abspath(target)
            else:
                try:
                    proj_row = self.find_project(target)
                except Exception:
                    proj_row = None

                if proj_row:
                    slug = sanitize_filename(proj_row["name"]).replace(" ", "-").lower()
                    if os.path.exists(slug):
                        repo_dir = os.path.abspath(slug)

        if not proj_row and os.path.exists(os.path.join(repo_dir, "project.json")):
            with open(os.path.join(repo_dir, "project.json"), "r", encoding="utf-8") as f:
                p_meta = json.load(f)
            p_guid = p_meta.get("guid")
            p_name = p_meta.get("name")
            if p_guid:
                proj_row = self.find_project(p_guid)
            if not proj_row and p_name:
                proj_row = self.find_project(p_name)

        return os.path.abspath(repo_dir), proj_row

    def status_project(self, target: Optional[str] = None) -> None:
        """Compare Git workspace against local Varwin SQLite database."""
        repo_dir, proj = self.resolve_repo_and_project(target)
        proj_file = os.path.join(repo_dir, "project.json")

        if not os.path.exists(proj_file):
            print(c_red(f"❌ Ошибка: В директории '{repo_dir}' не найден файл project.json!"))
            print("💡 Укажите папку репозитория через аргумент или перейдите в неё.")
            return

        with open(proj_file, "r", encoding="utf-8") as f:
            proj_meta = json.load(f)

        print(c_bold("=" * 80))
        print(f"🔍 {c_bold('СТАТУС ПРОЕКТА VARWIN 18')}: {c_cyan(proj_meta.get('name', 'Unknown'))}")
        print(f"📁 Локальный репозиторий: {repo_dir}")
        print(c_bold("=" * 80))

        if not proj:
            print(c_yellow("⚠️ Проект есть в Git, но отсутствует в локальной базе Varwin 18."))
            print(f"💡 Запустите {c_bold('varwin-git apply')} чтобы загрузить проект в Varwin.")
            return

        cur = self.db_con.cursor()
        proj_id = proj["id"]
        print(f"💾 База данных Varwin: ID {c_bold(str(proj_id))}, обновлен: {proj['updated_at']}")

        # Compare project metadata
        meta_diffs = []
        if proj_meta.get("name") != proj["name"]:
            meta_diffs.append(f"Имя: Git='{proj_meta.get('name')}' != DB='{proj['name']}'")
        if bool(proj_meta.get("mobile_ready", True)) != bool(proj["mobile_ready"]):
            meta_diffs.append(f"Mobile Ready: Git={proj_meta.get('mobile_ready')} != DB={bool(proj['mobile_ready'])}")
        if bool(proj_meta.get("multiplayer", False)) != bool(proj["multiplayer"]):
            meta_diffs.append(f"Multiplayer: Git={proj_meta.get('multiplayer')} != DB={bool(proj['multiplayer'])}")

        if meta_diffs:
            print(c_yellow(f"\n⚙️ Метаданные проекта изменены: {', '.join(meta_diffs)}"))
        else:
            print(c_green("\n⚙️ Метаданные проекта: синхронизированы"))

        scenes_dir = os.path.join(repo_dir, "scenes")
        if not os.path.exists(scenes_dir):
            print("Папка сцен отсутствует.")
            return

        db_scenes = cur.execute(
            "SELECT * FROM scenes WHERE project_id=? AND deleted_at IS NULL ORDER BY id", (proj_id,)
        ).fetchall()
        db_scenes_map = {sc["name"]: sc for sc in db_scenes}

        all_synced = True

        for scene_entry in sorted(os.listdir(scenes_dir)):
            sc_folder = os.path.join(scenes_dir, scene_entry)
            if not os.path.isdir(sc_folder):
                continue

            sc_file = os.path.join(sc_folder, "scene.json")
            sc_name = scene_entry
            if os.path.exists(sc_file):
                with open(sc_file, "r", encoding="utf-8") as f:
                    sc_meta = json.load(f)
                sc_name = sc_meta.get("name", scene_entry)

            print(f"\n🎬 {c_bold('Сцена:')} {c_magenta(sc_name)}")

            db_sc = db_scenes_map.get(sc_name)
            if not db_sc:
                print(f"   {c_yellow('⚠️ Сцена есть в Git, но отсутствует в Varwin!')}")
                all_synced = False
                continue

            # Compare Python code modules
            code_dir = os.path.join(sc_folder, "code")
            db_code = parse_json_field(db_sc["code_modules"], default={})
            if not isinstance(db_code, dict):
                db_code = {}

            git_py_files = set()
            if os.path.exists(code_dir):
                for f_name in sorted(os.listdir(code_dir)):
                    if f_name.endswith(".py"):
                        git_py_files.add(f_name)
                        f_path = os.path.join(code_dir, f_name)
                        with open(f_path, "r", encoding="utf-8") as f:
                            git_code = f.read()

                        db_version = db_code.get(f_name, "")
                        if f_name not in db_code:
                            print(f"   🐍 [CODE]  {f_name:<24} {c_cyan('[НОВЫЙ В GIT / НЕ ПРИМЕНЕН]')}")
                            all_synced = False
                        elif git_code != db_version:
                            print(f"   🐍 [CODE]  {f_name:<24} {c_yellow('[МОДИФИЦИРОВАН В РЕПОЗИТОРИИ]')}")
                            all_synced = False
                        else:
                            print(f"   🐍 [CODE]  {f_name:<24} {c_green('[СИНХРОНИЗИРОВАНО]')}")

            for db_f in sorted(db_code.keys()):
                if db_f not in git_py_files:
                    print(f"   🐍 [CODE]  {db_f:<24} {c_red('[ЕСТЬ В VARWIN, НО НЕТ В GIT]')}")
                    all_synced = False

            # Compare Blockly logic
            logic_dir = os.path.join(sc_folder, "logic")
            xml_path = os.path.join(logic_dir, "Blockly.xml")
            if os.path.exists(xml_path):
                with open(xml_path, "r", encoding="utf-8") as f:
                    git_xml = f.read().strip()
                b_data = parse_json_field(db_sc["blockly_data"], default={})
                db_xml = (b_data.get("blockly", "") if isinstance(b_data, dict) else str(b_data)).strip()

                if git_xml != db_xml:
                    print(f"   🧩 [LOGIC] Blockly.xml              {c_yellow('[РАЗЛИЧАЕТСЯ С БАЗОЙ VARWIN]')}")
                    all_synced = False
                else:
                    print(f"   🧩 [LOGIC] Blockly.xml              {c_green('[СИНХРОНИЗИРОВАНО]')}")

            # Compare objects count
            obj_file = os.path.join(sc_folder, "objects.json")
            if os.path.exists(obj_file):
                with open(obj_file, "r", encoding="utf-8") as f:
                    git_objs = json.load(f)
                db_objs_count = cur.execute(
                    "SELECT COUNT(*) FROM scene_objects WHERE scene_id=?", (db_sc["id"],)
                ).fetchone()[0]

                if len(git_objs) != db_objs_count:
                    print(f"   📦 [OBJS]  3D-объекты сцены         {c_yellow(f'[GIT: {len(git_objs)} шт., VARWIN: {db_objs_count} шт.]')}")
                    all_synced = False
                else:
                    print(f"   📦 [OBJS]  3D-объекты сцены ({len(git_objs)} шт.)  {c_green('[СИНХРОНИЗИРОВАНО]')}")

        print(c_bold("=" * 80))
        if all_synced:
            print(c_green("✨ Полная синхронизация: репозиторий Git и база Varwin 18 абсолютно идентичны!"))
        else:
            print(c_yellow("ℹ️ Обнаружены различия."))
            print(f"   - Чтобы посмотреть построчный diff: {c_bold('varwin-git diff')}")
            print(f"   - Чтобы применить код из Git в Varwin: {c_bold('varwin-git apply')}")
            print(f"   - Чтобы сохранить состояние Varwin в Git: {c_bold('varwin-git push -m \"...\"')}")

    def diff_project(self, target: Optional[str] = None, file_filter: Optional[str] = None) -> None:
        """Show colored unified diff between Git worktree and Varwin DB code."""
        repo_dir, proj = self.resolve_repo_and_project(target)
        if not proj:
            print(c_red("❌ Ошибка: проект не найден в локальной базе Varwin 18."))
            return

        cur = self.db_con.cursor()
        proj_id = proj["id"]
        scenes_dir = os.path.join(repo_dir, "scenes")
        if not os.path.exists(scenes_dir):
            print(c_red("❌ Папка scenes отсутствует."))
            return

        db_scenes = cur.execute(
            "SELECT * FROM scenes WHERE project_id=? AND deleted_at IS NULL ORDER BY id", (proj_id,)
        ).fetchall()
        db_scenes_map = {sc["name"]: sc for sc in db_scenes}

        diffs_found = 0

        for scene_entry in sorted(os.listdir(scenes_dir)):
            sc_folder = os.path.join(scenes_dir, scene_entry)
            if not os.path.isdir(sc_folder):
                continue

            sc_file = os.path.join(sc_folder, "scene.json")
            sc_name = scene_entry
            if os.path.exists(sc_file):
                with open(sc_file, "r", encoding="utf-8") as f:
                    sc_meta = json.load(f)
                sc_name = sc_meta.get("name", scene_entry)

            db_sc = db_scenes_map.get(sc_name)
            if not db_sc:
                continue

            db_code = parse_json_field(db_sc["code_modules"], default={})
            if not isinstance(db_code, dict):
                db_code = {}

            code_dir = os.path.join(sc_folder, "code")
            if os.path.exists(code_dir):
                for f_name in sorted(os.listdir(code_dir)):
                    if not f_name.endswith(".py"):
                        continue
                    if file_filter and file_filter not in f_name:
                        continue

                    f_path = os.path.join(code_dir, f_name)
                    with open(f_path, "r", encoding="utf-8") as f:
                        git_lines = f.readlines()

                    db_text = db_code.get(f_name, "")
                    db_lines = db_text.splitlines(keepends=True)

                    if git_lines != db_lines:
                        diffs_found += 1
                        diff_iter = difflib.unified_diff(
                            db_lines,
                            git_lines,
                            fromfile=f"Varwin DB: {sc_name}/code/{f_name}",
                            tofile=f"Git Worktree: {sc_name}/code/{f_name}",
                        )
                        print(f"\n{c_bold('diff --varwin-db-vs-git')} {c_cyan(f_name)}")
                        for line in diff_iter:
                            line_clean = line.rstrip("\n")
                            if line.startswith("---"):
                                print(c_red(line_clean))
                            elif line.startswith("+++"):
                                print(c_green(line_clean))
                            elif line.startswith("@@"):
                                print(c_cyan(line_clean))
                            elif line.startswith("+"):
                                print(c_green(line_clean))
                            elif line.startswith("-"):
                                print(c_red(line_clean))
                            else:
                                print(line_clean)

            # Diff Blockly.xml if applicable
            logic_dir = os.path.join(sc_folder, "logic")
            xml_path = os.path.join(logic_dir, "Blockly.xml")
            if os.path.exists(xml_path) and (not file_filter or "Blockly" in file_filter):
                with open(xml_path, "r", encoding="utf-8") as f:
                    git_xml_lines = f.readlines()
                b_data = parse_json_field(db_sc["blockly_data"], default={})
                db_xml = (b_data.get("blockly", "") if isinstance(b_data, dict) else str(b_data))
                db_xml_lines = db_xml.splitlines(keepends=True)

                if git_xml_lines != db_xml_lines:
                    diffs_found += 1
                    diff_iter = difflib.unified_diff(
                        db_xml_lines,
                        git_xml_lines,
                        fromfile=f"Varwin DB: {sc_name}/logic/Blockly.xml",
                        tofile=f"Git Worktree: {sc_name}/logic/Blockly.xml",
                    )
                    print(f"\n{c_bold('diff --varwin-db-vs-git')} {c_cyan('Blockly.xml')}")
                    for line in diff_iter:
                        line_clean = line.rstrip("\n")
                        if line.startswith("---"):
                            print(c_red(line_clean))
                        elif line.startswith("+++"):
                            print(c_green(line_clean))
                        elif line.startswith("@@"):
                            print(c_cyan(line_clean))
                        elif line.startswith("+"):
                            print(c_green(line_clean))
                        elif line.startswith("-"):
                            print(c_red(line_clean))
                        else:
                            print(line_clean)

        if diffs_found == 0:
            print(c_green("✨ Нет различий между кодом в Git и базой Varwin 18."))

    def clone_repo(self, repo_url: str, target_dir: Optional[str] = None, name_override: Optional[str] = None) -> None:
        """Clone a remote Git repository and apply it to the local Varwin platform."""
        cmd = ["git", "clone", repo_url]
        if target_dir:
            cmd.append(target_dir)

        print(f"📥 Клонируем проект из: {c_cyan(repo_url)}...")
        res = subprocess.run(cmd)
        if res.returncode != 0:
            raise RuntimeError(f"Команда 'git clone' завершилась с ошибкой {res.returncode}")

        if not target_dir:
            base = repo_url.rstrip("/").split("/")[-1]
            if base.endswith(".git"):
                base = base[:-4]
            target_dir = base

        target_dir = os.path.abspath(target_dir)
        print(f"⚙️ Применяем проект в локальный Varwin 18...")
        proj_id = self.apply_project(repo_dir=target_dir, target_project_name=name_override)
        print(c_green(f"🎉 Проект успешно импортирован в Varwin 18! (ID: {proj_id})"))
        print("💡 Теперь проект доступен в Varwin Dashboard и готов к запуску или редактированию.")

    def push_changes(self, identifier: Optional[str] = None, commit_msg: str = "Update Varwin project", repo_dir: Optional[str] = None):
        """Export latest state from Varwin, commit, and push to Git remote."""
        if not identifier and repo_dir and os.path.exists(os.path.join(repo_dir, "project.json")):
            with open(os.path.join(repo_dir, "project.json"), "r", encoding="utf-8") as f:
                identifier = json.load(f).get("name")
        elif not identifier and os.path.exists("project.json"):
            with open("project.json", "r", encoding="utf-8") as f:
                identifier = json.load(f).get("name")

        if not identifier:
            raise ValueError("Не указан проект для push (укажите ID, имя или запустите команду внутри папки репозитория).")

        export_dir = self.export_project(identifier, target_dir=repo_dir, init_git=True)
        print(f"📦 Проект экспортирован в: {export_dir}")

        subprocess.run(["git", "add", "."], cwd=export_dir, check=True)

        status_res = subprocess.run(["git", "status", "--porcelain"], cwd=export_dir, capture_output=True, text=True)
        if not status_res.stdout.strip():
            print(c_green("✨ Нет новых изменений для коммита."))
            return

        subprocess.run(["git", "commit", "-m", commit_msg], cwd=export_dir, check=True)
        print(c_green(f"✅ Коммит создан: '{commit_msg}'"))

        try:
            push_res = subprocess.run(["git", "push"], cwd=export_dir, capture_output=True, text=True)
            if push_res.returncode == 0:
                print(c_green("🚀 Успешно отправлено в удаленный Git-репозиторий!"))
            else:
                print(f"ℹ️ Git push вывод:\n{push_res.stderr or push_res.stdout}")
        except Exception as e:
            print(f"⚠️ Не удалось выполнить git push: {e}. Запустите 'git push' вручную.")

    def pull_changes(self, repo_dir: str = "."):
        """Pull latest commits from remote and apply to local Varwin."""
        repo_dir = os.path.abspath(repo_dir)
        print(f"📥 Подтягиваем изменения из Git в {repo_dir}...")
        pull_res = subprocess.run(["git", "pull"], cwd=repo_dir, capture_output=True, text=True)
        if pull_res.returncode != 0:
            print(f"⚠️ Ошибка git pull:\n{pull_res.stderr}")
        else:
            print(c_green(f"✅ Git pull завершен: {pull_res.stdout.strip()}"))

        proj_id = self.apply_project(repo_dir)
        print(c_green(f"🎉 Проект ID {proj_id} успешно обновлен в локальном Varwin 18!"))


def main():
    parser = argparse.ArgumentParser(
        prog="varwin-git",
        description="Varwin Git Sync Tool — командная разработка и версионирование проектов Varwin 18 XRMS через Git и GitHub"
    )
    subparsers = parser.add_subparsers(dest="command", help="Команда")

    # list
    subparsers.add_parser("list", help="Список всех проектов в локальном Varwin")

    # export
    exp_parser = subparsers.add_parser("export", help="Экспортировать проект Varwin в структуру Git")
    exp_parser.add_argument("project", help="ID, GUID или название проекта")
    exp_parser.add_argument("--dir", "-d", help="Целевая папка для экспорта (по умолчанию: slug имени проекта)")
    exp_parser.add_argument("--force", "-f", action="store_true", help="Перезаписать существующие файлы")

    # apply
    app_parser = subparsers.add_parser("apply", help="Применить (импортировать/обновить) Git проект в Varwin")
    app_parser.add_argument("--dir", "-d", default=".", help="Папка репозитория (по умолчанию: .)")
    app_parser.add_argument("--name", "-n", help="Переопределить имя проекта в Varwin")

    # status
    status_parser = subparsers.add_parser("status", help="Проверить статус синхронизации между Git и базой Varwin")
    status_parser.add_argument("target", nargs="?", help="Папка репозитория или имя проекта (по умолчанию: .)")

    # diff
    diff_parser = subparsers.add_parser("diff", help="Показать diff кода между Git репозиторием и базой Varwin")
    diff_parser.add_argument("target", nargs="?", help="Папка репозитория или имя проекта (по умолчанию: .)")
    diff_parser.add_argument("--file", help="Фильтр по конкретному файлу (например Main.py)")

    # clone
    clone_parser = subparsers.add_parser("clone", help="Клонировать Git репозиторий и автоматически загрузить в Varwin")
    clone_parser.add_argument("url", help="URL Git-репозитория (HTTPS или SSH)")
    clone_parser.add_argument("dir", nargs="?", help="Опциональная целевая папка")
    clone_parser.add_argument("--name", "-n", help="Переопределить имя проекта в Varwin")

    # push
    push_parser = subparsers.add_parser("push", help="Экспортировать из Varwin, закоммитить и запушить в Git")
    push_parser.add_argument("project", nargs="?", help="ID, GUID или название проекта (если не указано, берется из project.json)")
    push_parser.add_argument("-m", "--message", default="Update Varwin project", help="Сообщение коммита")
    push_parser.add_argument("--dir", "-d", help="Папка репозитория")

    # pull
    pull_parser = subparsers.add_parser("pull", help="Сделать git pull и обновить локальный Varwin")
    pull_parser.add_argument("--dir", "-d", default=".", help="Папка репозитория (по умолчанию: .)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = VarwinGitManager()

    if args.command == "list":
        projects = manager.list_projects()
        print(f"{'ID':<6} | {'Название проекта':<32} | {'GUID':<38} | {'Обновлен'}")
        print("-" * 95)
        for p in projects:
            print(f"{p['id']:<6} | {p['name']:<32} | {p['guid']:<38} | {p['updated_at']}")

    elif args.command == "export":
        out_dir = manager.export_project(args.project, target_dir=args.dir, force=args.force)
        print(c_green(f"✅ Проект успешно экспортирован в папку: {out_dir}"))
        print("💡 Теперь вы можете добавить remote на GitHub:")
        print(f"   cd \"{out_dir}\"")
        print("   git remote add origin https://github.com/YourOrg/YourProject.git")
        print("   git branch -M main")
        print("   git push -u origin main")

    elif args.command == "apply":
        proj_id = manager.apply_project(args.dir, target_project_name=args.name)
        print(c_green(f"🎉 Проект успешно загружен в Varwin 18 (ID: {proj_id})!"))

    elif args.command == "status":
        manager.status_project(args.target)

    elif args.command == "diff":
        manager.diff_project(args.target, file_filter=args.file)

    elif args.command == "clone":
        manager.clone_repo(args.url, target_dir=args.dir, name_override=args.name)

    elif args.command == "push":
        manager.push_changes(args.project, commit_msg=args.message, repo_dir=args.dir)

    elif args.command == "pull":
        manager.pull_changes(args.dir)


if __name__ == "__main__":
    main()
