#!/usr/bin/env python3
"""
Varwin 18 MCP (Model Context Protocol) Server.
Implements standard JSON-RPC 2.0 over Stdio.
Connects AI agents directly to Varwin 18 XRMS runtime, GraphQL API,
scene objects, and Python code modules.
"""

import json
import logging
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

# Ensure parent directory is in sys.path so server works both as module and standalone script
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from mcp.client import VarwinClient
from mcp.docs_search import VarwinDocsSearch
from mcp.validator import VarwinCodeValidator

log_dir = os.path.expanduser("~/.config/VarwinData18/Logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "mcp_server.log")),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("varwin-mcp")


class VarwinMCPServer:
    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self):
        self.client = VarwinClient()
        self.validator = VarwinCodeValidator()
        self.docs = VarwinDocsSearch()
        self.tools = self._build_tools_registry()

    def _build_tools_registry(self) -> Dict[str, Dict[str, Any]]:
        return {
            "varwin_status": {
                "description": "Проверить статус подключения к серверу Varwin 18, версию платформы и активный воркспейс.",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
                "handler": self._tool_status,
            },
            "varwin_list_projects": {
                "description": "Получить список всех проектов в рабочем пространстве Varwin (имена, ID, GUID, статус мобильной готовности).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "workspace_id": {
                            "type": "integer",
                            "description": "Необязательный ID воркспейса (по умолчанию используется активный)",
                        }
                    },
                },
                "handler": self._tool_list_projects,
            },
            "varwin_get_project": {
                "description": "Получить подробную информацию о проекте Varwin (список сцен, конфигураций, шаблонов) по ID.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "integer",
                            "description": "ID проекта",
                        }
                    },
                    "required": ["project_id"],
                },
                "handler": self._tool_get_project,
            },
            "varwin_get_scene": {
                "description": "Получить детальную информацию о сцене: имя, SID, список объектов и модули кода.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "scene_id": {
                            "type": "integer",
                            "description": "ID сцены",
                        }
                    },
                    "required": ["scene_id"],
                },
                "handler": self._tool_get_scene,
            },
            "varwin_list_scene_objects": {
                "description": "Получить список всех объектов на сцене с их именами переменных в Python (SceneObjects) и типами обёрток (SceneObjectTypes).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "scene_id": {
                            "type": "integer",
                            "description": "ID сцены",
                        }
                    },
                    "required": ["scene_id"],
                },
                "handler": self._tool_list_scene_objects,
            },
            "varwin_get_code_modules": {
                "description": "Получить исходный код Python-скриптов (Main.py, пользовательские модули) выбранной сцены.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "scene_id": {
                            "type": "integer",
                            "description": "ID сцены",
                        }
                    },
                    "required": ["scene_id"],
                },
                "handler": self._tool_get_code_modules,
            },
            "varwin_update_code_modules": {
                "description": "Записать и применить Python-скрипты к сцене Varwin с автоматической проверкой на запрещённые модули (asyncio, sleep) и корректность сигнатур.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "scene_id": {
                            "type": "integer",
                            "description": "ID сцены",
                        },
                        "code_modules": {
                            "type": "object",
                            "description": "Словарь модулей: {'Main.py': 'код...', 'my_module.py': 'код...'}",
                        },
                        "skip_validation": {
                            "type": "boolean",
                            "description": "Пропустить предварительную проверку кода (по умолчанию false)",
                        }
                    },
                    "required": ["scene_id", "code_modules"],
                },
                "handler": self._tool_update_code_modules,
            },
            "varwin_validate_python": {
                "description": "Проверить Python-код на совместимость с движком Varwin 18 (поиск time.sleep, asyncio, некорректных Add*Handler и Enums).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Исходный код скрипта",
                        },
                        "filename": {
                            "type": "string",
                            "description": "Имя файла (по умолчанию Main.py)",
                        }
                    },
                    "required": ["code"],
                },
                "handler": self._tool_validate_python,
            },
            "varwin_search_api": {
                "description": "Поиск по официальной документации Python API Varwin 18: методы, поведения (Motion, Rotate, Physics, Interaction), события, свойства.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Поисковый запрос (например: 'MoveToObject', 'AddGrabStartedHandler', 'ChangeColorOverTime')",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Максимальное количество результатов (по умолчанию 5)",
                        }
                    },
                    "required": ["query"],
                },
                "handler": self._tool_search_api,
            },
            "varwin_get_wrapper_doc": {
                "description": "Получить полную документацию с примерами для конкретной обёртки или поведения (PlayerWrapper, VBotBoyWrapper, MotionBehaviour, PhysicsBehaviour, etc.).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "wrapper_name": {
                            "type": "string",
                            "description": "Имя обёртки или поведения (например, 'PlayerWrapper' или 'MotionBehaviour')",
                        }
                    },
                    "required": ["wrapper_name"],
                },
                "handler": self._tool_get_wrapper_doc,
            },
            "varwin_create_project": {
                "description": "Создать новый проект в Varwin 18.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Название нового проекта",
                        },
                        "mobile_ready": {
                            "type": "boolean",
                            "description": "Поддержка мобильных гарнитур / standalone (по умолчанию true)",
                        },
                        "multiplayer": {
                            "type": "boolean",
                            "description": "Сетевой многопользовательский режим (по умолчанию false)",
                        }
                    },
                    "required": ["name"],
                },
                "handler": self._tool_create_project,
            },
            "varwin_launch_client": {
                "description": "Запустить 3D Unity-клиент Varwin для сцены или проекта через системный URL-лаунчер.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "scene_sid": {
                            "type": "string",
                            "description": "SID сцены (например из varwin_get_scene)",
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["desktop", "vr"],
                            "description": "Режим запуска: desktop или vr (по умолчанию desktop)",
                        }
                    },
                },
                "handler": self._tool_launch_client,
            },
        }

    # Tool Handlers
    def _tool_status(self, args: Dict[str, Any]) -> str:
        try:
            info = self.client.get_server_info()
            return (
                f"✅ **Varwin Server 18 активен**\n"
                f"- **URL:** `{info.get('url')}`\n"
                f"- **Версия приложения:** `{info.get('appVersion')}`\n"
                f"- **Активный Workspace ID:** `{info.get('activeWorkspaceId')}`\n"
                f"- **Авторизация:** {'Успешна (Bearer токен получен)' if info.get('authenticated') else 'Готов к подключению'}"
            )
        except Exception as e:
            return f"❌ Ошибка подключения к Varwin Server: {e}\nУбедитесь, что Varwin 18 запущен."

    def _tool_list_projects(self, args: Dict[str, Any]) -> str:
        try:
            projects = self.client.list_projects(workspace_id=args.get("workspace_id"))
            if not projects:
                return "В рабочем пространстве пока нет проектов."

            out = [f"### Найдено проектов: {len(projects)}\n"]
            for p in projects:
                scenes_list = ", ".join(f"'{s['name']}' (ID: {s['id']})" for s in p.get("scenes", []))
                out.append(
                    f"- **{p['name']}** (ID: `{p['id']}`, GUID: `{p['guid']}`)\n"
                    f"  - Сцены: {scenes_list or 'нет сцен'}\n"
                    f"  - Mobile: `{p.get('mobileReady')}`, Multiplayer: `{p.get('multiplayer')}`"
                )
            return "\n".join(out)
        except Exception as e:
            return f"Ошибка получения списка проектов: {e}"

    def _tool_get_project(self, args: Dict[str, Any]) -> str:
        try:
            p = self.client.get_project(args["project_id"])
            if not p:
                return f"Проект с ID {args['project_id']} не найден."
            return (
                f"## Проект: {p['name']}\n"
                f"- **ID:** `{p['id']}`\n"
                f"- **GUID:** `{p['guid']}`\n"
                f"- **Автор:** {p.get('author', {}).get('name', 'Не указан')}\n"
                f"- **Сцены:**\n" +
                "\n".join(f"  - {s['name']} (ID: `{s['id']}`, SID: `{s['sid']}`)" for s in p.get("scenes", []))
            )
        except Exception as e:
            return f"Ошибка: {e}"

    def _tool_get_scene(self, args: Dict[str, Any]) -> str:
        try:
            scene = self.client.get_scene(args["scene_id"])
            if not scene:
                return f"Сцена с ID {args['scene_id']} не найдена."

            objects = self.client.parse_scene_objects(scene)
            code_modules = scene.get("codeModules") or {}

            out = [
                f"## Сцена: {scene['name']} (ID: `{scene['id']}`)\n",
                f"- **Проект:** {scene.get('projectName')} (ID: `{scene.get('projectId')}`)",
                f"- **SID:** `{scene.get('sid')}`",
                f"- **Всего объектов:** {len(objects)}",
                f"- **Модули кода:** {', '.join(code_modules.keys()) or 'нет'}\n",
                "### Ключевые объекты на сцене:",
            ]
            for obj in objects[:15]:
                out.append(f"- `{obj['variable_name']}`: type `{obj['wrapper_type']}`")
            if len(objects) > 15:
                out.append(f"*(ещё {len(objects) - 15} объектов, вызовите varwin_list_scene_objects для полного списка)*")

            return "\n".join(out)
        except Exception as e:
            return f"Ошибка получения сцены: {e}"

    def _tool_list_scene_objects(self, args: Dict[str, Any]) -> str:
        try:
            scene = self.client.get_scene(args["scene_id"])
            if not scene:
                return f"Сцена с ID {args['scene_id']} не найдена."

            objects = self.client.parse_scene_objects(scene)
            if not objects:
                return f"На сцене '{scene['name']}' нет объектов."

            out = [f"### Объекты сцены '{scene['name']}' (всего: {len(objects)})\n"]
            out.append("| Имя переменной (`SceneObjects`) | Тип обёртки (`SceneObjectTypes`) |")
            out.append("| :--- | :--- |")
            for obj in objects:
                out.append(f"| `{obj['variable_name']}` | `{obj['wrapper_type']}` |")

            return "\n".join(out)
        except Exception as e:
            return f"Ошибка: {e}"

    def _tool_get_code_modules(self, args: Dict[str, Any]) -> str:
        try:
            modules = self.client.get_code_modules(args["scene_id"])
            if not modules:
                return "В этой сцене нет активных модулей кода."

            out = []
            for name, code in modules.items():
                out.append(f"### Файл: `{name}`\n```python\n{code}\n```\n")
            return "\n".join(out)
        except Exception as e:
            return f"Ошибка получения кода: {e}"

    def _tool_update_code_modules(self, args: Dict[str, Any]) -> str:
        scene_id = args["scene_id"]
        modules = args["code_modules"]
        skip_val = args.get("skip_validation", False)

        # Validation step
        if not skip_val:
            validation_reports = []
            has_errors = False
            for filename, code in modules.items():
                res = self.validator.validate(code, filename=filename)
                if not res["valid"]:
                    has_errors = True
                    validation_reports.append(f"❌ **{filename} содержит ошибки:**\n" + "\n".join(f"- {e}" for e in res["errors"]))
                elif res["warnings"]:
                    validation_reports.append(f"⚠️ **{filename} (предупреждения):**\n" + "\n".join(f"- {w}" for w in res["warnings"]))

            if has_errors:
                return (
                    "⛔ **Код отклонён валидатором Varwin 18:**\n\n" +
                    "\n\n".join(validation_reports) +
                    "\n\nИсправьте ошибки перед отправкой в сцену (или укажите skip_validation=true)."
                )

        try:
            res = self.client.update_code_modules(scene_id, modules)
            return (
                f"✅ **Код успешно записан в сцену (ID: {scene_id})!**\n"
                f"- Обновлено модулей: {len(modules)} ({', '.join(modules.keys())})\n"
                f"- Изменения применятся в Varwin 18 мгновенно."
            )
        except Exception as e:
            return f"Ошибка обновления кода через GraphQL: {e}"

    def _tool_validate_python(self, args: Dict[str, Any]) -> str:
        code = args["code"]
        filename = args.get("filename", "Main.py")
        res = self.validator.validate(code, filename=filename)

        if res["valid"] and not res["warnings"]:
            return "✅ **Код полностью валиден для Varwin 18!** Запрещённых вызовов и синтаксических ошибок не обнаружено."

        out = []
        if not res["valid"]:
            out.append("❌ **Обнаружены критические ошибки:**")
            for e in res["errors"]:
                out.append(f"- {e}")

        if res["warnings"]:
            out.append("\n⚠️ **Предупреждения:**")
            for w in res["warnings"]:
                out.append(f"- {w}")

        return "\n".join(out)

    def _tool_search_api(self, args: Dict[str, Any]) -> str:
        query = args["query"]
        limit = args.get("limit", 5)
        results = self.docs.search(query, limit=limit)

        if not results:
            return f"По запросу '{query}' ничего не найдено в справочнике Varwin 18."

        out = [f"### Результаты поиска по API Varwin 18 для '{query}':\n"]
        for r in results:
            out.append(f"#### `{r['class_name']}`")
            out.append(f"```python\n{r['snippet']}\n```\n")
        return "\n".join(out)

    def _tool_get_wrapper_doc(self, args: Dict[str, Any]) -> str:
        name = args["wrapper_name"]
        doc = self.docs.get_wrapper_doc(name)
        if not doc:
            wrappers = self.docs.list_wrappers()
            close = [w for w in wrappers if name.lower() in w.lower()][:8]
            close_hint = f"\nВозможно вы имели в виду: {', '.join(close)}" if close else ""
            return f"Документация для '{name}' не найдена.{close_hint}"
        return doc[:3500] + ("\n\n*(документация обрезана по лимиту символов)*" if len(doc) > 3500 else "")

    def _tool_create_project(self, args: Dict[str, Any]) -> str:
        try:
            res = self.client.create_project(
                name=args["name"],
                mobile_ready=args.get("mobile_ready", True),
                multiplayer=args.get("multiplayer", False)
            )
            node = res.get("createProject", {})
            return f"✅ Проект **'{node.get('name')}'** успешно создан! ID: `{node.get('id')}`, GUID: `{node.get('guid')}`."
        except Exception as e:
            return f"Ошибка создания проекта: {e}"

    def _tool_launch_client(self, args: Dict[str, Any]) -> str:
        sid = args.get("scene_sid")
        mode = args.get("mode", "desktop")
        url = f"varwin-client-18://open?mode={mode}"
        if sid:
            url += f"&sceneSid={sid}"

        try:
            subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"🚀 Клиент Varwin запущен через URL `{url}`."
        except Exception as e:
            return f"Ошибка запуска через xdg-open: {e}"

    # JSON-RPC Dispatcher
    def handle_request(self, req: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": self.PROTOCOL_VERSION,
                    "capabilities": {
                        "tools": {},
                    },
                    "serverInfo": {
                        "name": "varwin-mcp",
                        "version": "1.0.0",
                    },
                },
            }

        elif method == "notifications/initialized":
            logger.info("Client connected and initialized.")
            return None

        elif method == "ping":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

        elif method == "tools/list":
            tools_list = []
            for name, meta in self.tools.items():
                tools_list.append({
                    "name": name,
                    "description": meta["description"],
                    "inputSchema": meta["inputSchema"],
                })
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools_list}}

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error: Tool '{tool_name}' not found."}],
                        "isError": True,
                    },
                }

            handler = self.tools[tool_name]["handler"]
            try:
                text_result = handler(arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": text_result}],
                        "isError": False,
                    },
                }
            except Exception as e:
                logger.exception("Error executing tool %s", tool_name)
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Exception executing {tool_name}: {e}"}],
                        "isError": True,
                    },
                }

        else:
            if msg_id is not None:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not found",
                    },
                }
            return None

    def run_stdio(self):
        logger.info("Varwin MCP Server started listening on STDIN...")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                req = json.loads(line)
            except Exception as e:
                logger.error("JSON parse error: %s", e)
                continue

            resp = self.handle_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                sys.stdout.flush()


def main():
    server = VarwinMCPServer()
    server.run_stdio()


if __name__ == "__main__":
    main()
