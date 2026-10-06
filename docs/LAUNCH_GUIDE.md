# Руководство по запуску и подключению VarWin MCP

Детальное руководство по установке, компиляции и интеграции **VarWin MCP Server** для платформы **Varwin 18 XRMS** с современными AI-клиентами: **Claude Desktop**, **Cursor**, **Antigravity**, **Cline / Roo Code** и другими.

---

## 📋 Содержание

1. [Требования](#требования)
2. [Архитектура и варианты запуска](#архитектура-и-варианты-запуска)
3. [Сборка Go-бинарника](#сборка-go-бинарника)
4. [Переменные окружения](#переменные-окружения)
5. [Инструкции по подключению клиентов](#инструкции-по-подключению-клиентов)
   - [Claude Desktop](#1-claude-desktop)
   - [Cursor IDE](#2-cursor-ide)
   - [Antigravity / Gemini CLI](#3-antigravity--gemini-cli)
   - [Cline / Roo Code (VS Code)](#4-cline--roo-code-vs-code)
6. [Проверка работоспособности](#проверка-работоспособности)
7. [Решение частых проблем (Troubleshooting)](#решение-частых-проблем-troubleshooting)

---

## ⚙️ Требования

- **Varwin 18 XRMS**: установленный и запущенный сервер (по умолчанию порт `1801`, URL `http://127.0.0.1:1801`).
- **Для Go-версии (рекомендуется)**:
  - Готовый бинарник: `bin/varwin-mcp` (уже скомпилирован под Linux x86_64, ~7 МБ, не требует зависимостей).
  - Для самостоятельной сборки: **Go 1.21+**.
- **Для Python-версии**:
  - **Python 3.10+** (использует только стандартную библиотеку, внешние pip-пакеты не требуются).

---

## 🏗️ Архитектура и варианты запуска

В репозитории доступны **две равноправные реализации**:

| Параметр | Go Edition (`mcp-go`) ⚡ | Python Edition (`mcp`) 🐍 |
|---|---|---|
| **Бинарник / Скрипт** | `bin/varwin-mcp` | `mcp/server.py` |
| **Количество инструментов** | **28 инструментов** (полный охват + сырой GraphQL) | **12 ключевых инструментов** |
| **Скорость запуска** | Около 3–5 мс | Около 80–120 мс |
| **Потребление RAM** | ~15 МБ | ~35 МБ |
| **Внешние зависимости** | Отсутствуют (автономный бинарник) | Только стандартная библиотека Python |
| **Рекомендуемое применение** | Постоянная разработка, Cursor, Claude, Antigravity | Быстрая модификация логики без перекомпиляции |

---

## 🔨 Сборка Go-бинарника

Если вы внесли изменения в код Go или компилируете сервер под другую ОС/архитектуру:

### Быстрая сборка через скрипт:
```bash
./scripts/build_mcp_go.sh
```

### Ручная компиляция:
```bash
cd mcp-go
go build -ldflags="-s -w" -o ../bin/varwin-mcp .
chmod +x ../bin/varwin-mcp
```

### Кросс-компиляция (например, под Windows или macOS):
```bash
# Для Windows:
GOOS=windows GOARCH=amd64 go build -ldflags="-s -w" -o ../bin/varwin-mcp.exe .

# Для macOS (Apple Silicon M1/M2/M3):
GOOS=darwin GOARCH=arm64 go build -ldflags="-s -w" -o ../bin/varwin-mcp-darwin-arm64 .
```

---

## 🌐 Переменные окружения

MCP-сервер настраивается через переменные окружения процесса:

| Переменная | По умолчанию | Описание |
|---|---|---|
| `VARWIN_URL` | `http://127.0.0.1:1801` | Базовый URL бэкенда Varwin 18. Порт 1801 используется встроенным HTTP/GraphQL API сервисом Varwin. |

> **Примечание об авторизации**: Сервер автоматически проходит процедуру `loginAsDefaultUser` в GraphQL API Varwin, получает Bearer JWT-токен и определяет активный `Workspace ID`. Никаких ручных ключей указывать не требуется!

---

## 🔌 Инструкции по подключению клиентов

### 1. Claude Desktop

Конфигурационный файл Claude Desktop находится по пути:
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### Вариант A: Нативный Go-бинарник (Рекомендуется)
```json
{
  "mcpServers": {
    "varwin": {
      "command": "/home/reg/Projects/NOVAT.varwin/bin/varwin-mcp",
      "args": [],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

#### Вариант B: Python-версия
```json
{
  "mcpServers": {
    "varwin": {
      "command": "python3",
      "args": [
        "/home/reg/Projects/NOVAT.varwin/mcp/server.py"
      ],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

---

### 2. Cursor IDE

В Cursor MCP-серверы можно настраивать глобально или локально в проекте.

#### Способ 1: Конфигурационный файл проекта `.cursor/mcp.json`
Создайте файл `.cursor/mcp.json` в корне вашего рабочего каталога:

```json
{
  "mcpServers": {
    "varwin": {
      "command": "/home/reg/Projects/NOVAT.varwin/bin/varwin-mcp",
      "args": [],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

#### Способ 2: Через интерфейс Cursor
1. Откройте **Settings** (`Ctrl+,` или `Cmd+,`) -> **Features** -> **MCP Servers**.
2. Нажмите **Add New MCP Server**.
3. Укажите:
   - **Name**: `varwin`
   - **Type**: `command`
   - **Command**: `/home/reg/Projects/NOVAT.varwin/bin/varwin-mcp`
4. Сохраните и проверьте статус подключения (зеленый индикатор).

---

### 3. Antigravity / Gemini CLI

Конфигурационный файл Antigravity располагается в `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "varwin": {
      "command": "/home/reg/Projects/NOVAT.varwin/bin/varwin-mcp",
      "args": [],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

Либо для Python-версии:
```json
{
  "mcpServers": {
    "varwin": {
      "command": "/usr/bin/python3",
      "args": ["/home/reg/Projects/NOVAT.varwin/mcp/server.py"],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      }
    }
  }
}
```

---

### 4. Cline / Roo Code (VS Code)

В расширениях Cline или Roo Code для VS Code:
1. Откройте панель расширения Cline.
2. Нажмите иконку **MCP Servers** (шестеренка/кубик).
3. Нажмите **Edit Global MCP Settings** (откроется `cline_mcp_settings.json`).
4. Добавьте блок:

```json
{
  "mcpServers": {
    "varwin": {
      "command": "/home/reg/Projects/NOVAT.varwin/bin/varwin-mcp",
      "args": [],
      "env": {
        "VARWIN_URL": "http://127.0.0.1:1801"
      },
      "disabled": false,
      "autoApprove": [
        "varwin_status",
        "varwin_list_projects",
        "varwin_get_project",
        "varwin_get_scene",
        "varwin_list_scene_objects",
        "varwin_search_api",
        "varwin_get_wrapper_doc"
      ]
    }
  }
}
```

---

## 🧪 Проверка работоспособности

### 1. Тест инициализации JSON-RPC Handshake:
Отправьте тестовый запрос в STDIN бинарника:

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | ./bin/varwin-mcp
```

Ожидаемый ответ:
```json
{"jsonrpc":"2.0","id":1,"result":{"capabilities":{"tools":{}},"protocolVersion":"2024-11-05","serverInfo":{"name":"varwin-mcp-go","version":"2.0.0"}}}
```

### 2. Тест вызова инструмента `varwin_status`:
```bash
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "varwin_status", "arguments": {}}}' | ./bin/varwin-mcp
```

При запущенном Varwin 18 ответ содержит версию приложения (`18.x.xxx`) и ID активного рабочего пространства.

---

## 🩺 Решение частых проблем (Troubleshooting)

### 1. Ошибка подключения (`Connection refused` к `127.0.0.1:1801`)
- **Причина**: Сервер платформы Varwin 18 не запущен.
- **Решение**:
  - Запустите Varwin 18 в системе (`varwin-18` или ярлык приложения).
  - Проверьте доступность порта:
    ```bash
    curl -I http://127.0.0.1:1801/query
    ```
    Должен вернуться HTTP-ответ `200 OK` или `400 Bad Request` от GraphQL-эндпоинта.

### 2. Ошибка прав доступа к бинарнику (`Permission denied`)
- **Причина**: Файл `bin/varwin-mcp` не имеет флага исполняемого файла.
- **Решение**:
  ```bash
  chmod +x /home/reg/Projects/NOVAT.varwin/bin/varwin-mcp
  ```

### 3. Ошибка авторизации Bearer JWT (`Authentication failed`)
- **Причина**: Varwin 18 запущен в защищенном режиме с кастомной базой данных пользователей, где отключен дефолтный вход.
- **Решение**: Проверьте через `varwin_graphql_raw` доступность мутации `loginAsDefaultUser`. В стандартной локальной установке Varwin 18 авторизация по умолчанию включена.

### 4. Конфликт портов или удалённый сервер
- Если Varwin 18 запущен на другом порту или удалённом хосте, задайте точный адрес в `VARWIN_URL`:
  ```json
  "env": {
    "VARWIN_URL": "http://192.168.1.100:1801"
  }
  ```

### 5. Поиск по документации возвращает пустой результат
- Убедитесь, что файл справочника `docs/varwin18_python_api_full.md` присутствует в репозитории. Go-бинарник и Python-сервер автоматически находят его по относительному и абсолютному пути.
