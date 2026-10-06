# 🔄 Полный контекст сессии: Varwin 18 XRMS Ecosystem & MCP

> **Дата создания:** 2026-10-06  
> **Назначение:** Полный слепок состояния диалога, архитектуры, репозиториев и кодовой базы для бесшовного переноса работы на другое устройство (PC / Laptop / Server) в любого AI-ассистента (Antigravity, Cursor, Claude Desktop, ChatGPT, Cline).

---

## 📌 1. Сводка репозиториев и исходного кода

| Репозиторий | Назначение | Технологии | Ссылка на GitHub |
|---|---|---|---|
| **`VarWin-mcp`** | Кроссплатформенный сервер MCP (Go & Python) + утилита командной работы `varwin-git` | Go 1.21, Python 3.10+, GraphQL, SQLite | [https://github.com/B10Sreg/VarWin-mcp.git](https://github.com/B10Sreg/VarWin-mcp.git) |
| **`VarWin-Arch`** | Рецепт упаковки Varwin 18 под Arch Linux (PKGBUILD, .SRCINFO, фиксы Vulkan/ICU) | Bash, Makepkg, Systemd, XDG | [https://github.com/B10Sreg/VarWin-Arch.git](https://github.com/B10Sreg/VarWin-Arch.git) |

### Локальные пути на рабочей машине:
- Основной проект / MCP: `/home/reg/Projects/NOVAT.varwin`
- Репозиторий пакета Arch: `/home/reg/Projects/varwin-bin`
- Установленный рантайм Varwin: `/opt/Varwin18/`
- База данных Varwin: `~/.config/VarwinData18/SQLite3/database.db` (на Windows: `%APPDATA%\VarwinData18\SQLite3\database.db`)
- Логи: `~/.config/VarwinData18/Logs/`

---

## 🏗️ 2. Что было сделано и решено в этой сессии

### 1. Решение командной разработки (`varwin-git`):
- **Проблема:** Стандартный экспорт проекта Varwin в `.vwp` весит **2.1 ГБ** (из-за компиляции Unity AssetBundles для Win/Linux/Android). Обмениваться версиями через флешки/облака было невозможно.
- **Решение:** Создана утилита **`varwin-git`** (`scripts/varwin_git.py` + бинарники в `bin/varwin-git` и `bin/varwin-git.cmd`).
- **Результат:** Проект декомпозируется в чистый Git-репозиторий весом **~60 КБ** (**в 30 000 раз меньше!**):
  - `project.json` — метаданные, GUID, автор
  - `scenes/<Scene>/scene.json` — настройки шаблона окружения, камера, точка спавна
  - `scenes/<Scene>/objects.json` — все 3D-объекты сцены с координатами `x,y,z`, поворотами, масштабами и свойствами инспектора
  - `scenes/<Scene>/code/*.py` — чистый Python-код сцены (Main.py)
  - `scenes/<Scene>/logic/Blockly.xml` & `Blockly.py` — блоки визуальной логики
- Протестирован полный цикл: `export` -> `git push` -> `git clone` -> `apply` (восстанавливает проект в Varwin со 100% точностью).
- Подготовлен подробный гайд для команды: [`docs/GIT_TEAM_WORKFLOW.md`](file:///home/reg/Projects/NOVAT.varwin/docs/GIT_TEAM_WORKFLOW.md).

### 2. Пакет под Arch Linux (`VarWin-Arch`):
- Разработан чистый `PKGBUILD` и `.SRCINFO` для Varwin 18 XRMS.
- Учтены зависимости (`icu`, `openssl-1.1`, `vulkan-driver`, `libx11`, `libxcursor`).
- Решена проблема краша Vulkan/Unity в связке с песочницей Chromium через флаги `--no-sandbox` и приоритет OpenGL/Vulkan.
- Опубликован в репозиторий `https://github.com/B10Sreg/VarWin-Arch.git`.

### 3. Model Context Protocol Server (`VarWin-mcp`):
- Реализованы **две версии сервера**:
  - **Go Edition (`mcp-go`)**: собранные бинарники под Linux (`bin/varwin-mcp`) и Windows (`bin/varwin-mcp.exe`). Время отклика 3–15 мс.
  - **Python Edition (`mcp`)**: на стандартной библиотеке Python (`mcp/server.py` + `mcp/client.py`).
- 28+ инструментов для AI: управление проектами, сценами, библиотекой объектов, кодом Python, логикой Blockly, запуск клиента через URI-схему `varwin-client-18://`.
- Офлайн-поиск по всей документации Python API (90+ страниц, 83 обёртки).
- AST-валидатор Python для предотвращения крашей Unity (блокировка `time.sleep`, `asyncio`, `requests`).
- Добавлены гайды запуска для Claude Desktop, Cursor, Antigravity в [`docs/LAUNCH_GUIDE.md`](file:///home/reg/Projects/NOVAT.varwin/docs/LAUNCH_GUIDE.md).

### 4. Тестовые проекты в Varwin 18:
- **Проект 6 ("Color Spheres & Text")**:
  - Нажатие на кнопку меняет текст.
  - Три цветные сферы (Red, Green, Blue) увеличенного диаметра.
  - Наведение взгляда/луча (raycast hover) меняет цвет надписи под цвет сферы.
  - Учтена ориентация спавна игрока и обратные повороты.
  - Реализовано исключительно на чистых блоках Blockly без внешних хаков.
- **Проект 5 ("Duck Hunt 18")**:
  - Сцена охоты на уток с физикой, спавном и счётчиком очков.

### 5. Реверс-инжиниринг формата `.vwp` для Blender плагина:
- Исследована внутренняя структура пакетов `.vwp`, `.vwo`, `.vwm`, `.vwst`.
- Составлена архитектурная спецификация для будущего плагина к Blender (`docs/vwp_format_and_blender_plugin_spec.md`).

---

## ⚙️ 3. Окружение и системные параметры

- **Платформа:** Linux (Arch Linux x86_64) / Windows 10/11
- **Varwin Server:** `http://127.0.0.1:1801`
- **GraphQL Endpoint:** `http://127.0.0.1:1801/query`
- **Активный Workspace ID:** `3`
- **Авторизация:** JWT Bearer через мутацию `loginAsDefaultUser(input: { clientInfo: "..." })`
- **Конфигурация SQLite3 базы:**
  - Linux: `~/.config/VarwinData18/SQLite3/database.db`
  - Windows: `%APPDATA%\VarwinData18\SQLite3\database.db`
  - Ключевые таблицы: `projects`, `scenes`, `scene_objects`, `objects`, `scene_templates`, `scene_object_behaviours`

---

## 📋 4. Готовый промпт для вставки на новом устройстве

Скопируйте текст ниже и отправьте его первой строкой новому AI-ассистенту на другом компьютере:

```markdown
Привет! Мы продолжаем разработку экосистемы вокруг Varwin 18 XRMS.
Контекст предыдущей работы:
1. Репозитории:
   - Основной инструмент: https://github.com/B10Sreg/VarWin-mcp.git (MCP сервер на Go и Python, плюс инструмент varwin-git для командной разработки через GitHub).
   - Пакет Arch Linux: https://github.com/B10Sreg/VarWin-Arch.git (PKGBUILD и лаунчеры).
2. Ключевые достижения:
   - Создана утилита varwin-git (scripts/varwin_git.py), заменяющая 2-гигабайтные архивы .vwp чистыми 60-килобайтными репозиториями на GitHub.
   - Реализован MCP-сервер (varwin-mcp) с 28 инструментами (проекты, сцены, объекты, Blockly, Python, запуск 3D-клиента).
   - Написаны гайды по запуску (LAUNCH_GUIDE.md) и воркфлоу командной работы (GIT_TEAM_WORKFLOW.md).
   - Реализован тестовый проект с кнопкой, тремя сферами и изменением текста по наведению.
3. Окружение:
   - Varwin 18 работает локально на порту 1801 (http://127.0.0.1:1801/query, Workspace ID 3).
   - База данных SQLite: ~/.config/VarwinData18/SQLite3/database.db (Linux) или %APPDATA%\VarwinData18\SQLite3\database.db (Windows).

Я готов продолжить работу. Напомни текущий статус и предложи следующие шаги.
```
