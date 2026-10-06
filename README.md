# VarWin MCP (Model Context Protocol) Server for Varwin 18

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows & Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-0078D6?logo=windows&logoColor=white)](https://github.com/B10Sreg/VarWin-mcp)
[![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?logo=go&logoColor=white)](mcp-go/)
[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](mcp/)
[![Protocol](https://img.shields.io/badge/MCP-2024--11--05-8A2BE2)](https://modelcontextprotocol.io/)
[![Varwin XRMS](https://img.shields.io/badge/Varwin-18%20XRMS-FF6B00)](https://varwin.com/)

Высокопроизводительный кроссплатформенный сервер протокола **Model Context Protocol (MCP)** для **Windows 10/11** и **Linux**, позволяющий AI-ассистентам (**Claude Desktop**, **Cursor**, **Antigravity**, **Cline / Roo Code**, **ChatGPT**) напрямую взаимодействовать с платформой **Varwin 18 XRMS** в реальном времени.

С помощью VarWin MCP нейросетевые модели получают полный контроль над виртуальными мирами: управление проектами, манипуляция 3D-объектами и сценами, мгновенное редактирование логики Python и визуальных блоков Blockly, инспекция типов, валидация скриптов и запуск 3D-клиента Unity.

---

## ✨ Ключевые возможности

- 🚀 **Две производительные реализации**:
  - **Go Edition (`mcp-go`)**: сверхбыстрый нативный бинарник без внешних зависимостей (`varwin-mcp` под Linux и `varwin-mcp.exe` под Windows) с откликом 3–15 мс.
  - **Python Edition (`mcp`)**: гибкая кроссплатформенная реализация на стандартной библиотеке Python для быстрой модификации и отладки.
- 🪟 **Полная поддержка Windows и Linux**:
  - Автоматическое определение путей к данным Varwin (`%APPDATA%\VarwinData18` на Windows и `~/.config/VarwinData18` на Linux).
  - Нативный запуск Unity-клиента через `rundll32` на Windows и `xdg-open` на Linux.
  - Поддержка запуска интерпретаторов Python (`python.exe` / `python3`).
- 🛠️ **28 специализированных инструментов (MCP Tools)**:
  - Полный жизненный цикл проектов и сцен (создание, дублирование, удаление, шаблоны).
  - Управление 3D-объектами сцены, расстановка, привязка параметров и инспекция обёрток.
  - Двусторонняя синхронизация кода Python (`Main.py` и пользовательские модули) и логики Blockly.
  - Универсальный GraphQL-терминал (`varwin_graphql_raw`) со 100% доступом к внутреннему API движка.
- 📖 **Встроенный офлайн-поиск по документации**:
  - Мгновенный полнотекстовый поиск по всей документации Varwin 18 Python API (90+ разделов, 83 обёртки).
  - Получение сигнатур методов, свойств и примеров кода без выхода в интернет.
- 🛡️ **Строгий AST-валидатор Python**:
  - Защита рантайма Unity от крашей и зависаний главного потока: блокировка `time.sleep`, `asyncio`, `threading`, `requests`.
  - Проверка регистрации циклов через `Varwin.Async.AddStart / AddUpdate`.
  - Автоматическая проверка сигнатур обработчиков событий (наличие аргумента `sender`).
- 🎮 **Интеграция с 3D-клиентом**:
  - Запуск сцен в режимах **Desktop** и **VR** непосредственно по команде AI.

---

## 🛠️ Сводная таблица инструментов (MCP Tools)

### 1. Ядро и системная интроспекция
| Инструмент | Назначение |
|---|---|
| `varwin_status` | Проверка подключения к серверу Varwin 18, версии платформы, активного воркспейса и статуса JWT |
| `varwin_graphql_raw` | **Универсальный GraphQL-терминал**: выполнение любого сырого GraphQL-запроса или мутации (все 28 запросов и 71 мутация) |
| `varwin_get_system_module` | Получение системного модуля `Varwin.py` с типами, методами и сигнатурами рантайма движка |

### 2. Управление проектами
| Инструмент | Назначение |
|---|---|
| `varwin_list_projects` | Список всех проектов с метаданными, сценами и флагами Mobile/Multiplayer |
| `varwin_get_project` | Полная информация о проекте (ID, GUID, автор, список сцен) |
| `varwin_create_project` | Создание нового проекта в воркспейсе |
| `varwin_rename_project` | Переименование проекта по ID |
| `varwin_duplicate_project` | Клонирование / дублирование существующего проекта |
| `varwin_delete_project` | Удаление проекта по ID |

### 3. Сцены и 3D-окружения (Templates)
| Инструмент | Назначение |
|---|---|
| `varwin_get_scene` | Полная структура сцены, SID, список 3D-объектов и модулей кода |
| `varwin_create_scene` | Создание новой сцены в проекте на основе шаблона окружения |
| `varwin_rename_scene` | Переименование сцены |
| `varwin_duplicate_scene` | Клонирование сцены в проекте |
| `varwin_delete_scene` | Удаление сцены по ID |
| `varwin_list_scene_templates` | Список доступных локаций и шаблонов (Sci-Fi, Лес, Дом, Таунхаус, Пустая сцена) |

### 4. 3D-объекты и библиотека
| Инструмент | Назначение |
|---|---|
| `varwin_list_scene_objects` | Все объекты на сцене с именами Python-переменных (`SceneObjects`) и типами обёрток (`SceneObjectTypes`) |
| `varwin_list_library_objects` | Каталог доступных 3D-объектов библиотеки Varwin с фильтрацией и поиском |
| `varwin_add_scene_object` | Добавление 3D-объекта из библиотеки на сцену |
| `varwin_update_scene_objects` | Расстановка и трансформация объектов (координаты, поворот, масштаб, свойства) |

### 5. Логика, Python-код и Blockly
| Инструмент | Назначение |
|---|---|
| `varwin_get_code_modules` | Исходный код Python-модулей сцены (`Main.py`, пользовательские скрипты) |
| `varwin_update_code_modules` | Сохранение и компиляция Python-кода с автоматической предвалидацией |
| `varwin_validate_python` | AST-линтинг скрипта под правила рантайма Varwin 18 |
| `varwin_get_blockly` | Получение структуры визуальных блоков и сгенерированного кода Blockly |
| `varwin_update_blockly` | Обновление визуальной логики Blockly на сцене |

### 6. Ресурсы проекта
| Инструмент | Назначение |
|---|---|
| `varwin_list_resources` | Список ресурсов проекта (3D-модели, аудиофайлы, текстуры, видеоматериалы) |

### 7. Справочник API и документация
| Инструмент | Назначение |
|---|---|
| `varwin_search_api` | Полнотекстовый поиск по 90+ разделам официальной документации Python API |
| `varwin_get_wrapper_doc` | Получение полной документации по конкретной обёртке (`PlayerWrapper`, `MotionBehaviour`, `VBotBoyWrapper` и др.) |

### 8. Рантайм и клиент
| Инструмент | Назначение |
|---|---|
| `varwin_launch_client` | Запуск 3D Unity-клиента Varwin для выбранной сцены (режимы Desktop / VR) |

### 9. Командная разработка и Git-синхронизация
| Инструмент | Назначение |
|---|---|
| `varwin_git_export` | Экспорт проекта из Varwin в чистый Git-репозиторий (~60 КБ вместо гигабайтов `.vwp`) |
| `varwin_git_apply` | Импорт и обновление проекта в локальном Varwin из репозитория Git/GitHub |

> 📖 **Подробное руководство по командной работе:** см. [docs/GIT_TEAM_WORKFLOW.md](docs/GIT_TEAM_WORKFLOW.md).

---

## ⚡ Быстрый старт (Quickstart)

### Вариант 1: Использование готового Go-бинарника (Рекомендуется)
Репозиторий уже включает предсобранный бинарник `bin/varwin-mcp` (Linux x86_64, ~7 МБ).

#### Linux:
```bash
chmod +x bin/varwin-mcp
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | ./bin/varwin-mcp
```

#### Windows (PowerShell):
```powershell
Get-Content -Raw init.json | .\bin\varwin-mcp.exe
```

Собрать бинарники для обеих платформ (Linux & Windows):
```bash
./scripts/build_mcp_go.sh
```

### Вариант 2: Запуск на Python
Работает на стандартном интерпретаторе Python 3.10+ (Windows и Linux):

```bash
# Linux / macOS
python3 -m mcp.server

# Windows
python -m mcp.server
```

---

## 🔌 Подключение к AI-ассистентам

Подробные пошаговые инструкции для всех платформ смотрите в [docs/LAUNCH_GUIDE.md](docs/LAUNCH_GUIDE.md).

### Claude Desktop

**Путь к конфигурационному файлу**:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Конфигурация для Windows:
```json
{
  "mcpServers": {
    "varwin": {
      "command": "C:\\path\\to\\VarWin-mcp\\bin\\varwin-mcp.exe",
      "args": [],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

#### Конфигурация для Linux:
```json
{
  "mcpServers": {
    "varwin": {
      "command": "/полный/путь/к/VarWin-mcp/bin/varwin-mcp",
      "args": [],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

### Cursor IDE
Добавьте конфигурацию в `.cursor/mcp.json` в корне рабочего проекта:

```json
{
  "mcpServers": {
    "varwin": {
      "command": "/полный/путь/к/VarWin-mcp/bin/varwin-mcp",
      "args": [],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

### Antigravity / Gemini CLI
Добавьте сервер в `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "varwin": {
      "command": "/полный/путь/к/VarWin-mcp/bin/varwin-mcp",
      "args": [],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

---

## 📂 Структура репозитория

```
.
├── bin/
│   └── varwin-mcp               # Скомпилированный нативный бинарник (Go)
├── mcp-go/                      # Исходный код реализации на Go
│   ├── internal/
│   │   ├── client/              # GraphQL клиент и авторизация Varwin 18
│   │   ├── docs/                # Поисковый движок по документации
│   │   ├── server/              # MCP JSON-RPC 2.0 сервер и обработчики инструментов
│   │   └── validator/           # AST-валидатор Python под рантайм Varwin
│   ├── go.mod
│   └── main.go
├── mcp/                         # Исходный код реализации на Python (Zero dependencies)
│   ├── client.py                # GraphQL HTTP-клиент
│   ├── docs_search.py           # Поисковый модуль по API
│   ├── server.py                # MCP stdio-сервер
│   └── validator.py             # Валидатор кода Python
├── docs/
│   ├── LAUNCH_GUIDE.md          # Полное руководство по запуску и настройке
│   ├── varwin18_python_api_full.md # Офлайн-база знаний Varwin 18 Python API
│   └── vwp_format_and_blender_plugin_spec.md # Спецификация пакетов VWP
├── scripts/
│   ├── build_mcp_go.sh          # Скрипт быстрой сборки Go-бинарника
│   ├── install_varwin_arch.sh   # Скрипт установки Varwin 18 на Arch Linux
│   └── optimize_performance.sh  # Оптимизация производительности GPU/Vulkan
├── LICENSE                      # MIT License
└── README.md
```

---

## 📄 Лицензия

Проект распространяется под лицензией [MIT](LICENSE).

## 👤 Автор и контакты

- **GitHub**: [@B10Sreg](https://github.com/B10Sreg)
- **Репозиторий**: [https://github.com/B10Sreg/VarWin-mcp](https://github.com/B10Sreg/VarWin-mcp)
