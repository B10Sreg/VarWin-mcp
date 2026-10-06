# Varwin 18 MCP Server

Полноценный сервер **Model Context Protocol (MCP)** по спецификации JSON-RPC 2.0 (версия `2024-11-05`) для двусторонней интеграции AI-ассистентов (Antigravity, Claude, Cursor) с платформой **Varwin 18 XRMS**.

---

## 🚀 Возможности

1. **Интроспекция сервера и воркспейсов**:
   - Автоматическая авторизация по JWT Bearer токену (`loginAsDefaultUser`).
   - Определение активного воркспейса пользователя (`workspaceMembership`).
   - Получение статуса сервера и версии приложения (`18.5.231`).

2. **Работа с проектами и сценами**:
   - `varwin_list_projects`: вывод всех проектов с флагами Mobile, Multiplayer, списком сцен.
   - `varwin_get_project`: детальная информация по ID или GUID проекта.
   - `varwin_get_scene`: данные о сцене, окружении (Template), SID и структуре.
   - `varwin_create_project`: программное создание новых проектов.

3. **Объекты сцены и автогенерируемый код**:
   - `varwin_list_scene_objects`: список всех 3D-объектов на сцене, их русские названия, привязанные переменные Python и типы обёрток (`SceneObjectTypes`).

4. **Двустороннее управление Python-скриптами (`codeModules`)**:
   - `varwin_get_code_modules`: чтение `Main.py` и пользовательских модулей напрямую из базы Varwin.
   - `varwin_update_code_modules`: атомарная запись и сохранение обновлённого кода в проект через GraphQL Mutation `updateCodeModules`.

5. **AST-валидация и линтинг кода**:
   - `varwin_validate_python`: строгая проверка скриптов перед отправкой в движок:
     - Запрет синхронных блокирующих библиотек (`time.sleep`, `asyncio`, `threading`, `multiprocessing`, `requests`).
     - Контроль корректной регистрации циклов (`Varwin.Async.AddStart/AddUpdate`).
     - Проверка сигнатур обработчиков событий (наличие аргумента `sender`).
     - Предупреждение об Enum `None` -> `None_`.

6. **Встроенный поисковик по документации**:
   - `varwin_search_api`: быстрый полнотекстовый поиск по 90+ разделам и 83 обёрткам Varwin Python API (`docs/varwin18_python_api_full.md`).
   - `varwin_get_wrapper_doc`: получение полной справки по конкретному классу обёртки.

7. **Запуск 3D-клиента**:
   - `varwin_launch_client`: запуск сцены в режиме Desktop или VR через нативный URL-лаунчер Varwin.

---

## 🛠️ Набор инструментов (12 MCP Tools)

| Инструмент | Описание |
|---|---|
| `varwin_status` | Проверка подключения к серверу, версии и активного Workspace ID |
| `varwin_list_projects` | Список проектов в воркспейсе со сценами |
| `varwin_get_project` | Полная информация о проекте (id / guid) |
| `varwin_get_scene` | Данные сцены и метаданные |
| `varwin_list_scene_objects` | Все объекты сцены, их переменные и типы обёрток |
| `varwin_get_code_modules` | Исходный код Python-модулей сцены (`Main.py`, ...) |
| `varwin_update_code_modules` | Сохранение Python-модулей сцены на сервер |
| `varwin_validate_python` | Валидатор кода под правила рантайма Varwin |
| `varwin_search_api` | Поиск методов, поведений и событий в документации |
| `varwin_get_wrapper_doc` | Документация по конкретной обёртке (например `VBotBoyWrapper`) |
| `varwin_create_project` | Создание нового проекта в воркспейсе |
| `varwin_launch_client` | Запуск 3D Unity-клиента Varwin |

---

## ⚙️ Конфигурация в Antigravity

Сервер зарегистрирован в `~/.gemini/config/mcp_config.json`:

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

## 🧪 Ручной запуск и тестирование

Сервер работает автономно через стандартный ввод/вывод (stdio). Зависимостей, кроме стандартной библиотеки Python 3, не требуется.

```bash
# Тестовый запуск и проверка handshake
python3 -m mcp.server
```

Пример отправки запроса в stdin:
```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "varwin_status", "arguments": {}}}
```
