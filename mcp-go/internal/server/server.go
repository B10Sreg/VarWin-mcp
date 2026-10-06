package server

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"sort"
	"strconv"
	"strings"
	"sync"

	"varwin-mcp/internal/client"
	"varwin-mcp/internal/docs"
	"varwin-mcp/internal/validator"
)

type ToolHandler func(args map[string]interface{}) (string, error)

type ToolDefinition struct {
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	InputSchema map[string]interface{} `json:"inputSchema"`
	Handler     ToolHandler            `json:"-"`
}

type JSONRPCRequest struct {
	JSONRPC string                 `json:"jsonrpc"`
	ID      interface{}            `json:"id,omitempty"`
	Method  string                 `json:"method"`
	Params  map[string]interface{} `json:"params,omitempty"`
}

type JSONRPCResponse struct {
	JSONRPC string        `json:"jsonrpc"`
	ID      interface{}   `json:"id,omitempty"`
	Result  interface{}   `json:"result,omitempty"`
	Error   *JSONRPCError `json:"error,omitempty"`
}

type JSONRPCError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

type Server struct {
	client    *client.VarwinClient
	validator *validator.VarwinCodeValidator
	docs      *docs.VarwinDocsSearch
	tools     map[string]ToolDefinition
	mu        sync.Mutex
}

func NewServer() *Server {
	s := &Server{
		client:    client.NewVarwinClient(""),
		validator: validator.NewVarwinCodeValidator(),
		docs:      docs.NewVarwinDocsSearch(""),
		tools:     make(map[string]ToolDefinition),
	}
	s.registerTools()
	return s
}

func (s *Server) registerTools() {
	// 1. Status & Core
	s.tools["varwin_status"] = ToolDefinition{
		Name:        "varwin_status",
		Description: "Проверить статус подключения к серверу Varwin 18, версию платформы и активный воркспейс.",
		InputSchema: map[string]interface{}{
			"type":       "object",
			"properties": map[string]interface{}{},
		},
		Handler: s.toolStatus,
	}

	s.tools["varwin_graphql_raw"] = ToolDefinition{
		Name:        "varwin_graphql_raw",
		Description: "Выполнить произвольный GraphQL запрос или мутацию напрямую к Varwin 18. Даёт 100% доступ ко всем 28 запросам и 71 мутации бэкенда.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"query": map[string]interface{}{
					"type":        "string",
					"description": "Строка GraphQL запроса или мутации",
				},
				"variables": map[string]interface{}{
					"type":        "object",
					"description": "Словарь переменных GraphQL (необязательно)",
				},
				"auth": map[string]interface{}{
					"type":        "boolean",
					"description": "Включать ли авторизацию Bearer JWT (по умолчанию true)",
				},
			},
			"required": []string{"query"},
		},
		Handler: s.toolGraphQLRaw,
	}

	// 2. Projects
	s.tools["varwin_list_projects"] = ToolDefinition{
		Name:        "varwin_list_projects",
		Description: "Получить список всех проектов в рабочем пространстве Varwin (имена, ID, GUID, статус мобильной готовности).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"workspace_id": map[string]interface{}{
					"type":        "integer",
					"description": "Необязательный ID воркспейса (по умолчанию используется активный)",
				},
			},
		},
		Handler: s.toolListProjects,
	}

	s.tools["varwin_get_project"] = ToolDefinition{
		Name:        "varwin_get_project",
		Description: "Получить подробную информацию о проекте Varwin (список сцен, конфигураций, шаблонов) по ID.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"project_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID проекта",
				},
			},
			"required": []string{"project_id"},
		},
		Handler: s.toolGetProject,
	}

	s.tools["varwin_create_project"] = ToolDefinition{
		Name:        "varwin_create_project",
		Description: "Создать новый проект в текущем рабочем пространстве Varwin 18.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"name": map[string]interface{}{
					"type":        "string",
					"description": "Название нового проекта",
				},
				"mobile_ready": map[string]interface{}{
					"type":        "boolean",
					"description": "Поддержка мобильных гарнитур / standalone (по умолчанию true)",
				},
				"multiplayer": map[string]interface{}{
					"type":        "boolean",
					"description": "Сетевой многопользовательский режим (по умолчанию false)",
				},
			},
			"required": []string{"name"},
		},
		Handler: s.toolCreateProject,
	}

	s.tools["varwin_rename_project"] = ToolDefinition{
		Name:        "varwin_rename_project",
		Description: "Переименовать существующий проект по ID.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"project_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID проекта",
				},
				"name": map[string]interface{}{
					"type":        "string",
					"description": "Новое название проекта",
				},
			},
			"required": []string{"project_id", "name"},
		},
		Handler: s.toolRenameProject,
	}

	s.tools["varwin_duplicate_project"] = ToolDefinition{
		Name:        "varwin_duplicate_project",
		Description: "Клонировать/дублировать проект с новым именем.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"project_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID клонируемого проекта",
				},
				"name": map[string]interface{}{
					"type":        "string",
					"description": "Название копии проекта",
				},
				"workspace_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID целевого воркспейса (по умолчанию текущий)",
				},
			},
			"required": []string{"project_id", "name"},
		},
		Handler: s.toolDuplicateProject,
	}

	s.tools["varwin_delete_project"] = ToolDefinition{
		Name:        "varwin_delete_project",
		Description: "Удалить проект по его ID.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"project_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID удаляемого проекта",
				},
			},
			"required": []string{"project_id"},
		},
		Handler: s.toolDeleteProject,
	}

	// 3. Scenes & Environments
	s.tools["varwin_get_scene"] = ToolDefinition{
		Name:        "varwin_get_scene",
		Description: "Получить детальную информацию о сцене: имя, SID, список объектов и модули кода.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
			},
			"required": []string{"scene_id"},
		},
		Handler: s.toolGetScene,
	}

	s.tools["varwin_create_scene"] = ToolDefinition{
		Name:        "varwin_create_scene",
		Description: "Создать новую сцену в проекте на основе шаблона окружения (Location Template).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"project_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID проекта, в котором создается сцена",
				},
				"name": map[string]interface{}{
					"type":        "string",
					"description": "Название сцены",
				},
				"scene_template_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID шаблона окружения (см. varwin_list_scene_templates)",
				},
				"lang": map[string]interface{}{
					"type":        "string",
					"enum":        []string{"ru", "en", "auto"},
					"description": "Язык сцены (по умолчанию 'ru')",
				},
			},
			"required": []string{"project_id", "name", "scene_template_id"},
		},
		Handler: s.toolCreateScene,
	}

	s.tools["varwin_rename_scene"] = ToolDefinition{
		Name:        "varwin_rename_scene",
		Description: "Переименовать сцену по её ID.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
				"name": map[string]interface{}{
					"type":        "string",
					"description": "Новое название сцены",
				},
			},
			"required": []string{"scene_id", "name"},
		},
		Handler: s.toolRenameScene,
	}

	s.tools["varwin_duplicate_scene"] = ToolDefinition{
		Name:        "varwin_duplicate_scene",
		Description: "Клонировать сцену (в тот же или другой проект).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID клонируемой сцены",
				},
				"target_project_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID целевого проекта",
				},
				"name": map[string]interface{}{
					"type":        "string",
					"description": "Название новой сцены",
				},
			},
			"required": []string{"scene_id", "target_project_id", "name"},
		},
		Handler: s.toolDuplicateScene,
	}

	s.tools["varwin_delete_scene"] = ToolDefinition{
		Name:        "varwin_delete_scene",
		Description: "Удалить сцену по её ID.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID удаляемой сцены",
				},
			},
			"required": []string{"scene_id"},
		},
		Handler: s.toolDeleteScene,
	}

	s.tools["varwin_list_scene_templates"] = ToolDefinition{
		Name:        "varwin_list_scene_templates",
		Description: "Получить список доступных шаблонов 3D-окружений (Sci-Fi, Лес, Дом, Таунхаус, Пустая сцена).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"workspace_id": map[string]interface{}{
					"type":        "integer",
					"description": "Необязательный ID воркспейса",
				},
			},
		},
		Handler: s.toolListSceneTemplates,
	}

	// 4. Scene Objects & Hierarchy
	s.tools["varwin_list_scene_objects"] = ToolDefinition{
		Name:        "varwin_list_scene_objects",
		Description: "Получить список всех объектов на сцене с их именами переменных в Python (SceneObjects) и типами обёрток (SceneObjectTypes).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
			},
			"required": []string{"scene_id"},
		},
		Handler: s.toolListSceneObjects,
	}

	s.tools["varwin_add_scene_object"] = ToolDefinition{
		Name:        "varwin_add_scene_object",
		Description: "Добавить 3D-объект из библиотеки на сцену с точными 3D-координатами (X, Y, Z), углами вращения (Pitch, Yaw, Roll) и масштабом.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
				"object_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID объекта из библиотеки (см. varwin_list_library_objects)",
				},
				"name": map[string]interface{}{
					"type":        "string",
					"description": "Отображаемое имя объекта (например 'Duck 1')",
				},
				"variable_name": map[string]interface{}{
					"type":        "string",
					"description": "Имя переменной в Python (например 'duck1')",
				},
				"x": map[string]interface{}{"type": "number", "description": "Позиция X в метрах"},
				"y": map[string]interface{}{"type": "number", "description": "Позиция Y в метрах"},
				"z": map[string]interface{}{"type": "number", "description": "Позиция Z в метрах"},
				"rx": map[string]interface{}{"type": "number", "description": "Поворот Pitch (X) в градусах"},
				"ry": map[string]interface{}{"type": "number", "description": "Поворот Yaw (Y) в градусах"},
				"rz": map[string]interface{}{"type": "number", "description": "Поворот Roll (Z) в градусах"},
				"sx": map[string]interface{}{"type": "number", "description": "Масштаб X (по умолчанию 1.0)"},
				"sy": map[string]interface{}{"type": "number", "description": "Масштаб Y (по умолчанию 1.0)"},
				"sz": map[string]interface{}{"type": "number", "description": "Масштаб Z (по умолчанию 1.0)"},
			},
			"required": []string{"scene_id", "object_id", "name", "variable_name", "x", "y", "z"},
		},
		Handler: s.toolAddSceneObject,
	}

	s.tools["varwin_list_library_objects"] = ToolDefinition{
		Name:        "varwin_list_library_objects",
		Description: "Каталог готовых 3D-объектов библиотеки Varwin (боты, свет, интерактивные предметы, триггеры, сокеты).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"search": map[string]interface{}{
					"type":        "string",
					"description": "Строка поиска по имени объекта",
				},
				"limit": map[string]interface{}{
					"type":        "integer",
					"description": "Максимальное количество результатов (по умолчанию 50)",
				},
				"workspace_id": map[string]interface{}{
					"type":        "integer",
					"description": "Необязательный ID воркспейса",
				},
			},
		},
		Handler: s.toolListLibraryObjects,
	}

	s.tools["varwin_update_scene_objects"] = ToolDefinition{
		Name:        "varwin_update_scene_objects",
		Description: "Низкоуровневое обновление или расстановка 3D-объектов на сцене (координаты, повороты, масштабы, свойства).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
				"data": map[string]interface{}{
					"type":        "object",
					"description": "Словарь данных сцены (data)",
				},
				"scene_objects": map[string]interface{}{
					"type":        "array",
					"description": "Массив объектов сцены (sceneObjects)",
				},
				"object_behaviours": map[string]interface{}{
					"type":        "array",
					"description": "Массив поведений объектов (objectBehaviours)",
				},
			},
			"required": []string{"scene_id", "data"},
		},
		Handler: s.toolUpdateSceneObjects,
	}

	// 5. Logic, Scripts & Blockly
	s.tools["varwin_get_code_modules"] = ToolDefinition{
		Name:        "varwin_get_code_modules",
		Description: "Получить исходный код Python-скриптов (Main.py, пользовательские модули) выбранной сцены.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
			},
			"required": []string{"scene_id"},
		},
		Handler: s.toolGetCodeModules,
	}

	s.tools["varwin_update_code_modules"] = ToolDefinition{
		Name:        "varwin_update_code_modules",
		Description: "Записать и применить Python-скрипты к сцене Varwin с автоматической проверкой на запрещённые модули (asyncio, sleep) и корректность сигнатур.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
				"code_modules": map[string]interface{}{
					"type":        "object",
					"description": "Словарь модулей: {'Main.py': 'код...', 'my_module.py': 'код...'}",
				},
				"skip_validation": map[string]interface{}{
					"type":        "boolean",
					"description": "Пропустить предварительную проверку кода (по умолчанию false)",
				},
			},
			"required": []string{"scene_id", "code_modules"},
		},
		Handler: s.toolUpdateCodeModules,
	}

	s.tools["varwin_validate_python"] = ToolDefinition{
		Name:        "varwin_validate_python",
		Description: "Проверить Python-код на совместимость с движком Varwin 18 (поиск time.sleep, asyncio, некорректных Add*Handler и Enums).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"code": map[string]interface{}{
					"type":        "string",
					"description": "Исходный код скрипта",
				},
				"filename": map[string]interface{}{
					"type":        "string",
					"description": "Имя файла (по умолчанию Main.py)",
				},
			},
			"required": []string{"code"},
		},
		Handler: s.toolValidatePython,
	}

	s.tools["varwin_get_blockly"] = ToolDefinition{
		Name:        "varwin_get_blockly",
		Description: "Получить визуальную логику Blockly для сцены (blocklyCodeModule).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
			},
			"required": []string{"scene_id"},
		},
		Handler: s.toolGetBlockly,
	}

	s.tools["varwin_update_blockly"] = ToolDefinition{
		Name:        "varwin_update_blockly",
		Description: "Обновить визуальную логику Blockly сцены.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_id": map[string]interface{}{
					"type":        "integer",
					"description": "ID сцены",
				},
				"blockly_data": map[string]interface{}{
					"type":        "object",
					"description": "JSON-структура блоков Blockly",
				},
				"blockly_code_module": map[string]interface{}{
					"type":        "string",
					"description": "Сгенерированный Python-код модуля Blockly.py",
				},
				"used_object_ids": map[string]interface{}{
					"type":        "array",
					"description": "ID объектов, задействованных в логике",
				},
			},
			"required": []string{"scene_id", "blockly_data", "blockly_code_module"},
		},
		Handler: s.toolUpdateBlockly,
	}

	s.tools["varwin_get_system_module"] = ToolDefinition{
		Name:        "varwin_get_system_module",
		Description: "Получить официальный рантайм-модуль Varwin Python (Varwin.py) со всеми сигнатурами классов, методов и событий напрямую из движка.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"locale": map[string]interface{}{
					"type":        "string",
					"description": "Язык локализации документации сигнатур (ru / en, по умолчанию ru)",
				},
			},
		},
		Handler: s.toolGetSystemModule,
	}

	// 6. Resources & Assets
	s.tools["varwin_list_resources"] = ToolDefinition{
		Name:        "varwin_list_resources",
		Description: "Список медиаресурсов проекта (текстуры, звуки, видео, 3D-модели).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"limit": map[string]interface{}{
					"type":        "integer",
					"description": "Максимальное количество ресурсов (по умолчанию 50)",
				},
				"workspace_id": map[string]interface{}{
					"type":        "integer",
					"description": "Необязательный ID воркспейса",
				},
			},
		},
		Handler: s.toolListResources,
	}

	// 7. Docs & Search
	s.tools["varwin_search_api"] = ToolDefinition{
		Name:        "varwin_search_api",
		Description: "Поиск по официальной документации Python API Varwin 18: методы, поведения (Motion, Rotate, Physics, Interaction), события, свойства.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"query": map[string]interface{}{
					"type":        "string",
					"description": "Поисковый запрос (например: 'MoveToObject', 'AddGrabStartedHandler', 'ChangeColorOverTime')",
				},
				"limit": map[string]interface{}{
					"type":        "integer",
					"description": "Максимальное количество результатов (по умолчанию 5)",
				},
			},
			"required": []string{"query"},
		},
		Handler: s.toolSearchAPI,
	}

	s.tools["varwin_get_wrapper_doc"] = ToolDefinition{
		Name:        "varwin_get_wrapper_doc",
		Description: "Получить полную документацию конкретного класса обёртки (например: 'PlayerWrapper', 'BotBoyWrapper', 'MotionBehaviour').",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"wrapper_name": map[string]interface{}{
					"type":        "string",
					"description": "Имя обёртки (например: 'PlayerWrapper', 'Light', 'BotBoy')",
				},
			},
			"required": []string{"wrapper_name"},
		},
		Handler: s.toolGetWrapperDoc,
	}

	// 8. Runtime & Client
	s.tools["varwin_launch_client"] = ToolDefinition{
		Name:        "varwin_launch_client",
		Description: "Запустить 3D Unity-клиент Varwin для сцены или проекта через системный URL-лаунчер.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"scene_sid": map[string]interface{}{
					"type":        "string",
					"description": "SID сцены (например из varwin_get_scene)",
				},
				"mode": map[string]interface{}{
					"type":        "string",
					"enum":        []string{"desktop", "vr"},
					"description": "Режим запуска: desktop или vr (по умолчанию desktop)",
				},
			},
		},
		Handler: s.toolLaunchClient,
	}

	// 9. Git & Version Control
	s.tools["varwin_git_export"] = ToolDefinition{
		Name:        "varwin_git_export",
		Description: "Экспортировать проект Varwin в легкую (~60 КБ), версионируемую структуру Git/GitHub (project.json, scene.json, objects.json, code/*.py, logic/Blockly.xml).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"project": map[string]interface{}{
					"type":        "string",
					"description": "ID, GUID или название проекта для экспорта",
				},
				"dir": map[string]interface{}{
					"type":        "string",
					"description": "Опциональный путь к целевой папке Git-репозитория",
				},
			},
			"required": []string{"project"},
		},
		Handler: s.toolGitExport,
	}

	s.tools["varwin_git_apply"] = ToolDefinition{
		Name:        "varwin_git_apply",
		Description: "Импортировать или обновить проект в локальном Varwin 18 из репозитория Git/GitHub.",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"dir": map[string]interface{}{
					"type":        "string",
					"description": "Путь к папке Git-репозитория (по умолчанию '.')",
				},
				"name": map[string]interface{}{
					"type":        "string",
					"description": "Опциональное переопределение имени проекта",
				},
			},
		},
		Handler: s.toolGitApply,
	}

	s.tools["varwin_git_status"] = ToolDefinition{
		Name:        "varwin_git_status",
		Description: "Сравнить локальный Git-репозиторий проекта с базой данных Varwin 18 (показывает измененные файлы кода, Blockly, 3D-объекты).",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"dir": map[string]interface{}{
					"type":        "string",
					"description": "Путь к папке Git-репозитория (по умолчанию '.')",
				},
				"project": map[string]interface{}{
					"type":        "string",
					"description": "ID, GUID или имя проекта (необязательно)",
				},
			},
		},
		Handler: s.toolGitStatus,
	}
}

// Handlers

func (s *Server) toolStatus(args map[string]interface{}) (string, error) {
	info, err := s.client.GetServerInfo()
	if err != nil {
		return fmt.Sprintf("❌ Ошибка подключения к Varwin Server: %v\nУбедитесь, что Varwin 18 запущен.", err), nil
	}

	authStatus := "Готов к подключению"
	if auth, ok := info["authenticated"].(bool); ok && auth {
		authStatus = "Успешна (Bearer токен получен)"
	}

	return fmt.Sprintf(
		"✅ **Varwin Server 18 активен**\n"+
			"- **URL:** `%v`\n"+
			"- **Версия приложения:** `%v`\n"+
			"- **Активный Workspace ID:** `%v`\n"+
			"- **Авторизация:** %s",
		info["url"],
		info["appVersion"],
		info["activeWorkspaceId"],
		authStatus,
	), nil
}

func (s *Server) toolGraphQLRaw(args map[string]interface{}) (string, error) {
	query, _ := args["query"].(string)
	if query == "" {
		return "Ошибка: пустой GraphQL query", nil
	}

	vars, _ := args["variables"].(map[string]interface{})
	auth := true
	if a, ok := args["auth"].(bool); ok {
		auth = a
	}

	res, err := s.client.ExecuteRaw(query, vars, auth)
	if err != nil {
		return fmt.Sprintf("GraphQL Execution Error: %v", err), nil
	}

	jsonBytes, err := json.MarshalIndent(res, "", "  ")
	if err != nil {
		return fmt.Sprintf("%+v", res), nil
	}
	return fmt.Sprintf("```json\n%s\n```", string(jsonBytes)), nil
}

func (s *Server) toolListProjects(args map[string]interface{}) (string, error) {
	wsID := getIntArg(args, "workspace_id")
	projects, err := s.client.ListProjects(wsID)
	if err != nil {
		return fmt.Sprintf("Ошибка получения списка проектов: %v", err), nil
	}

	if len(projects) == 0 {
		return "В рабочем пространстве пока нет проектов.", nil
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("### Найдено проектов: %d\n\n", len(projects)))
	for _, p := range projects {
		var scenesNames []string
		if scenes, ok := p["scenes"].([]interface{}); ok {
			for _, sc := range scenes {
				if scMap, ok := sc.(map[string]interface{}); ok {
					scenesNames = append(scenesNames, fmt.Sprintf("'%v' (ID: %v)", scMap["name"], scMap["id"]))
				}
			}
		}

		scenesStr := strings.Join(scenesNames, ", ")
		if scenesStr == "" {
			scenesStr = "нет сцен"
		}

		sb.WriteString(fmt.Sprintf(
			"- **%v** (ID: `%v`, GUID: `%v`)\n  - Сцены: %s\n  - Mobile: `%v`, Multiplayer: `%v`\n",
			p["name"], p["id"], p["guid"], scenesStr, p["mobileReady"], p["multiplayer"],
		))
	}
	return strings.TrimSpace(sb.String()), nil
}

func (s *Server) toolGetProject(args map[string]interface{}) (string, error) {
	pID := getIntArg(args, "project_id")
	p, err := s.client.GetProject(pID, 0)
	if err != nil {
		return fmt.Sprintf("Ошибка: %v", err), nil
	}
	if p == nil {
		return fmt.Sprintf("Проект с ID %d не найден.", pID), nil
	}

	authorName := "Не указан"
	if author, ok := p["author"].(map[string]interface{}); ok {
		if name, ok := author["name"].(string); ok && name != "" {
			authorName = name
		}
	}

	var scenesLines []string
	if scenes, ok := p["scenes"].([]interface{}); ok {
		for _, sc := range scenes {
			if scMap, ok := sc.(map[string]interface{}); ok {
				scenesLines = append(scenesLines, fmt.Sprintf("  - %v (ID: `%v`, SID: `%v`)", scMap["name"], scMap["id"], scMap["sid"]))
			}
		}
	}

	return fmt.Sprintf(
		"## Проект: %v\n"+
			"- **ID:** `%v`\n"+
			"- **GUID:** `%v`\n"+
			"- **Автор:** %s\n"+
			"- **Сцены:**\n%s",
		p["name"], p["id"], p["guid"], authorName, strings.Join(scenesLines, "\n"),
	), nil
}

func (s *Server) toolCreateProject(args map[string]interface{}) (string, error) {
	name, _ := args["name"].(string)
	mobileReady := true
	if mr, ok := args["mobile_ready"].(bool); ok {
		mobileReady = mr
	}
	multiplayer := false
	if mp, ok := args["multiplayer"].(bool); ok {
		multiplayer = mp
	}

	res, err := s.client.CreateProject(name, mobileReady, multiplayer, 0)
	if err != nil {
		return fmt.Sprintf("Ошибка создания проекта: %v", err), nil
	}

	node, _ := res["createProject"].(map[string]interface{})
	proj, _ := node["project"].(map[string]interface{})
	return fmt.Sprintf(
		"✅ Проект **'%v'** успешно создан! ID: `%v`, GUID: `%v`.",
		proj["name"], node["projectId"], proj["guid"],
	), nil
}

func (s *Server) toolRenameProject(args map[string]interface{}) (string, error) {
	pID := getIntArg(args, "project_id")
	name, _ := args["name"].(string)
	res, err := s.client.RenameProject(pID, name)
	if err != nil {
		return fmt.Sprintf("Ошибка переименования: %v", err), nil
	}
	node, _ := res["renameProject"].(map[string]interface{})
	return fmt.Sprintf("✅ Проект %v успешно переименован в '%s'!", node["projectId"], name), nil
}

func (s *Server) toolDuplicateProject(args map[string]interface{}) (string, error) {
	pID := getIntArg(args, "project_id")
	name, _ := args["name"].(string)
	wsID := getIntArg(args, "workspace_id")
	res, err := s.client.DuplicateProject(pID, name, wsID)
	if err != nil {
		return fmt.Sprintf("Ошибка клонирования: %v", err), nil
	}
	node, _ := res["duplicateProject"].(map[string]interface{})
	proj, _ := node["project"].(map[string]interface{})
	return fmt.Sprintf("✅ Проект успешно дублирован как **'%v'** (ID: `%v`)!", proj["name"], node["projectId"]), nil
}

func (s *Server) toolDeleteProject(args map[string]interface{}) (string, error) {
	pID := getIntArg(args, "project_id")
	res, err := s.client.DeleteProject(pID)
	if err != nil {
		return fmt.Sprintf("Ошибка удаления проекта: %v", err), nil
	}
	node, _ := res["deleteProject"].(map[string]interface{})
	return fmt.Sprintf("🗑️ Проект ID %v успешно удалён.", node["projectId"]), nil
}

func (s *Server) toolGetScene(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	scene, err := s.client.GetScene(sID, 0)
	if err != nil {
		return fmt.Sprintf("Ошибка получения сцены: %v", err), nil
	}
	if scene == nil {
		return fmt.Sprintf("Сцена с ID %d не найдена.", sID), nil
	}

	objects := s.client.ParseSceneObjects(scene)
	codeModules, _ := scene["codeModules"].(map[string]interface{})

	var moduleNames []string
	for k := range codeModules {
		moduleNames = append(moduleNames, k)
	}
	modStr := strings.Join(moduleNames, ", ")
	if modStr == "" {
		modStr = "нет"
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("## Сцена: %v (ID: `%v`)\n\n", scene["name"], scene["id"]))
	sb.WriteString(fmt.Sprintf("- **Проект:** %v (ID: `%v`)\n", scene["projectName"], scene["projectId"]))
	sb.WriteString(fmt.Sprintf("- **SID:** `%v`\n", scene["sid"]))
	sb.WriteString(fmt.Sprintf("- **Всего объектов:** %d\n", len(objects)))
	sb.WriteString(fmt.Sprintf("- **Модули кода:** %s\n\n", modStr))
	sb.WriteString("### Ключевые объекты на сцене:\n")

	limit := 15
	if len(objects) < limit {
		limit = len(objects)
	}
	for i := 0; i < limit; i++ {
		sb.WriteString(fmt.Sprintf("- `%s`: type `%s`\n", objects[i].VariableName, objects[i].WrapperType))
	}
	if len(objects) > 15 {
		sb.WriteString(fmt.Sprintf("*(ещё %d объектов, вызовите varwin_list_scene_objects для полного списка)*\n", len(objects)-15))
	}

	return strings.TrimSpace(sb.String()), nil
}

func (s *Server) toolCreateScene(args map[string]interface{}) (string, error) {
	pID := getIntArg(args, "project_id")
	name, _ := args["name"].(string)
	tmplID := getIntArg(args, "scene_template_id")
	lang, _ := args["lang"].(string)

	res, err := s.client.CreateScene(pID, name, tmplID, lang)
	if err != nil {
		return fmt.Sprintf("Ошибка создания сцены: %v", err), nil
	}
	node, _ := res["createScene"].(map[string]interface{})
	sc, _ := node["scene"].(map[string]interface{})
	return fmt.Sprintf("✅ Сцена **'%v'** успешно создана! ID: `%v`, SID: `%v`.", sc["name"], node["sceneId"], sc["sid"]), nil
}

func (s *Server) toolRenameScene(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	name, _ := args["name"].(string)
	res, err := s.client.RenameScene(sID, name)
	if err != nil {
		return fmt.Sprintf("Ошибка переименования сцены: %v", err), nil
	}
	node, _ := res["renameScene"].(map[string]interface{})
	return fmt.Sprintf("✅ Сцена ID %v успешно переименована в '%s'.", node["sceneId"], name), nil
}

func (s *Server) toolDuplicateScene(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	targetPID := getIntArg(args, "target_project_id")
	name, _ := args["name"].(string)

	res, err := s.client.DuplicateScene(sID, targetPID, name)
	if err != nil {
		return fmt.Sprintf("Ошибка дублирования сцены: %v", err), nil
	}
	node, _ := res["duplicateScene"].(map[string]interface{})
	sc, _ := node["scene"].(map[string]interface{})
	return fmt.Sprintf("✅ Сцена успешно скопирована как **'%v'** (ID: `%v`, SID: `%v`)!", sc["name"], node["sceneId"], sc["sid"]), nil
}

func (s *Server) toolDeleteScene(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	res, err := s.client.DeleteScene(sID)
	if err != nil {
		return fmt.Sprintf("Ошибка удаления сцены: %v", err), nil
	}
	node, _ := res["deleteScene"].(map[string]interface{})
	return fmt.Sprintf("🗑️ Сцена ID %v успешно удалена.", node["sceneId"]), nil
}

func (s *Server) toolListSceneTemplates(args map[string]interface{}) (string, error) {
	wsID := getIntArg(args, "workspace_id")
	templates, err := s.client.ListSceneTemplates(wsID)
	if err != nil {
		return fmt.Sprintf("Ошибка получения шаблонов: %v", err), nil
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("### Доступные шаблоны 3D-окружений (%d):\n\n", len(templates)))
	for _, t := range templates {
		nameMap, _ := t["name"].(map[string]interface{})
		ruName, _ := nameMap["ru"].(string)
		enName, _ := nameMap["en"].(string)
		sb.WriteString(fmt.Sprintf("- **%s** (%s) — ID: `%v`, GUID: `%v`\n", ruName, enName, t["id"], t["guid"]))
	}
	return strings.TrimSpace(sb.String()), nil
}

func (s *Server) toolListSceneObjects(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	scene, err := s.client.GetScene(sID, 0)
	if err != nil {
		return fmt.Sprintf("Ошибка: %v", err), nil
	}
	if scene == nil {
		return fmt.Sprintf("Сцена с ID %d не найдена.", sID), nil
	}

	objects := s.client.ParseSceneObjects(scene)
	if len(objects) == 0 {
		return fmt.Sprintf("На сцене '%v' нет объектов.", scene["name"]), nil
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("### Объекты сцены '%v' (всего: %d)\n\n", scene["name"], len(objects)))
	sb.WriteString("| Имя переменной (`SceneObjects`) | Тип обёртки (`SceneObjectTypes`) |\n")
	sb.WriteString("| :--- | :--- |\n")
	for _, obj := range objects {
		sb.WriteString(fmt.Sprintf("| `%s` | `%s` |\n", obj.VariableName, obj.WrapperType))
	}
	return strings.TrimSpace(sb.String()), nil
}

func (s *Server) toolListLibraryObjects(args map[string]interface{}) (string, error) {
	wsID := getIntArg(args, "workspace_id")
	search, _ := args["search"].(string)
	limit := getIntArg(args, "limit")
	if limit == 0 {
		limit = 50
	}

	objects, total, err := s.client.ListLibraryObjects(wsID, search, limit)
	if err != nil {
		return fmt.Sprintf("Ошибка получения каталога объектов: %v", err), nil
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("### Каталог 3D-объектов библиотеки Varwin (Всего: %d, показано: %d):\n\n", total, len(objects)))
	sb.WriteString("| ID | Название (RU) | Name (EN) | GUID | Mobile |\n")
	sb.WriteString("| :--- | :--- | :--- | :--- | :--- |\n")
	for _, obj := range objects {
		nameMap, _ := obj["name"].(map[string]interface{})
		ruName, _ := nameMap["ru"].(string)
		enName, _ := nameMap["en"].(string)
		sb.WriteString(fmt.Sprintf("| `%v` | %s | %s | `%v` | `%v` |\n", obj["id"], ruName, enName, obj["guid"], obj["mobileReady"]))
	}
	return strings.TrimSpace(sb.String()), nil
}

func (s *Server) toolUpdateSceneObjects(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	data := args["data"]
	sceneObjects, _ := args["scene_objects"].([]interface{})
	behaviours, _ := args["object_behaviours"].([]interface{})

	res, err := s.client.UpdateSceneObjects(sID, data, sceneObjects, behaviours)
	if err != nil {
		return fmt.Sprintf("Ошибка обновления 3D-объектов сцены: %v", err), nil
	}
	node, _ := res["updateSceneObjects"].(map[string]interface{})
	return fmt.Sprintf("✅ 3D-объекты сцены ID %v успешно обновлены!", node["sceneId"]), nil
}

func (s *Server) toolGetCodeModules(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	modules, err := s.client.GetCodeModules(sID)
	if err != nil {
		return fmt.Sprintf("Ошибка получения кода: %v", err), nil
	}
	if len(modules) == 0 {
		return "В этой сцене нет активных модулей кода.", nil
	}

	var sb strings.Builder
	for name, code := range modules {
		sb.WriteString(fmt.Sprintf("### Файл: `%s`\n```python\n%s\n```\n\n", name, code))
	}
	return strings.TrimSpace(sb.String()), nil
}

func (s *Server) toolUpdateCodeModules(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	rawModules, ok := args["code_modules"].(map[string]interface{})
	if !ok {
		return "Ошибка: поле code_modules должно быть словарем {'filename': 'code'}", nil
	}

	skipVal := false
	if sv, ok := args["skip_validation"].(bool); ok {
		skipVal = sv
	}

	codeModules := make(map[string]string)
	for k, v := range rawModules {
		if str, ok := v.(string); ok {
			codeModules[k] = str
		}
	}

	if !skipVal {
		var reports []string
		hasErrors := false

		for filename, code := range codeModules {
			res := s.validator.Validate(code, filename)
			if !res.Valid {
				hasErrors = true
				var errLines []string
				for _, e := range res.Errors {
					errLines = append(errLines, "- "+e)
				}
				reports = append(reports, fmt.Sprintf("❌ **%s содержит ошибки:**\n%s", filename, strings.Join(errLines, "\n")))
			} else if len(res.Warnings) > 0 {
				var warnLines []string
				for _, w := range res.Warnings {
					warnLines = append(warnLines, "- "+w)
				}
				reports = append(reports, fmt.Sprintf("⚠️ **%s (предупреждения):**\n%s", filename, strings.Join(warnLines, "\n")))
			}
		}

		if hasErrors {
			return fmt.Sprintf(
				"⛔ **Код отклонён валидатором Varwin 18:**\n\n%s\n\nИсправьте ошибки перед отправкой в сцену (или укажите skip_validation=true).",
				strings.Join(reports, "\n\n"),
			), nil
		}
	}

	_, err := s.client.UpdateCodeModules(sID, codeModules)
	if err != nil {
		return fmt.Sprintf("Ошибка обновления кода через GraphQL: %v", err), nil
	}

	var keys []string
	for k := range codeModules {
		keys = append(keys, k)
	}

	return fmt.Sprintf(
		"✅ **Код успешно записан в сцену (ID: %d)!**\n- Обновлено модулей: %d (%s)\n- Изменения применятся в Varwin 18 мгновенно.",
		sID, len(codeModules), strings.Join(keys, ", "),
	), nil
}

func (s *Server) toolValidatePython(args map[string]interface{}) (string, error) {
	code, _ := args["code"].(string)
	filename, _ := args["filename"].(string)
	if filename == "" {
		filename = "Main.py"
	}

	res := s.validator.Validate(code, filename)
	if res.Valid && len(res.Warnings) == 0 {
		return "✅ **Код полностью валиден для Varwin 18!** Запрещённых вызовов и синтаксических ошибок не обнаружено.", nil
	}

	var lines []string
	if !res.Valid {
		lines = append(lines, "❌ **Обнаружены критические ошибки:**")
		for _, e := range res.Errors {
			lines = append(lines, "- "+e)
		}
	}

	if len(res.Warnings) > 0 {
		lines = append(lines, "\n⚠️ **Предупреждения:**")
		for _, w := range res.Warnings {
			lines = append(lines, "- "+w)
		}
	}

	return strings.Join(lines, "\n"), nil
}

func (s *Server) toolGetBlockly(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	blk, err := s.client.GetBlockly(sID)
	if err != nil {
		return fmt.Sprintf("Ошибка получения Blockly: %v", err), nil
	}
	code, _ := blk["blocklyCodeModule"].(string)
	return fmt.Sprintf("### Сгенерированный код Blockly сцены ID %d:\n```python\n%s\n```", sID, code), nil
}

func (s *Server) toolUpdateBlockly(args map[string]interface{}) (string, error) {
	sID := getIntArg(args, "scene_id")
	bData := args["blockly_data"]
	codeMod, _ := args["blockly_code_module"].(string)
	usedIDs, _ := args["used_object_ids"].([]interface{})

	res, err := s.client.UpdateBlockly(sID, bData, codeMod, usedIDs)
	if err != nil {
		return fmt.Sprintf("Ошибка обновления Blockly: %v", err), nil
	}
	node, _ := res["updateBlockly"].(map[string]interface{})
	return fmt.Sprintf("✅ Логика Blockly успешно обновлена для сцены ID %v!", node["sceneId"]), nil
}

func (s *Server) toolGetSystemModule(args map[string]interface{}) (string, error) {
	locale, _ := args["locale"].(string)
	mod, err := s.client.GetSystemModule(locale)
	if err != nil {
		return fmt.Sprintf("Ошибка получения системного модуля: %v", err), nil
	}

	limit := 4000
	if len(mod) > limit {
		return fmt.Sprintf("### Системный модуль Varwin Python (показаны первые %d символов из %d):\n```python\n%s\n```\n\n*(полный модуль содержит 77+ КБ определений API)*", limit, len(mod), mod[:limit]), nil
	}
	return fmt.Sprintf("### Системный модуль Varwin Python:\n```python\n%s\n```", mod), nil
}

func (s *Server) toolListResources(args map[string]interface{}) (string, error) {
	wsID := getIntArg(args, "workspace_id")
	limit := getIntArg(args, "limit")
	if limit == 0 {
		limit = 50
	}

	resources, total, err := s.client.ListResources(wsID, limit)
	if err != nil {
		return fmt.Sprintf("Ошибка получения ресурсов: %v", err), nil
	}

	if total == 0 {
		return "В проекте пока нет загруженных медиаресурсов (аудио, текстур, видео).", nil
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("### Медиаресурсы проекта (Всего: %d, показано: %d):\n\n", total, len(resources)))
	for _, r := range resources {
		nameMap, _ := r["name"].(map[string]interface{})
		ruName, _ := nameMap["ru"].(string)
		enName, _ := nameMap["en"].(string)
		sb.WriteString(fmt.Sprintf("- **%s** (%s) — ID: `%v`, GUID: `%v`\n", ruName, enName, r["id"], r["guid"]))
	}
	return strings.TrimSpace(sb.String()), nil
}

func (s *Server) toolSearchAPI(args map[string]interface{}) (string, error) {
	query, _ := args["query"].(string)
	limit := 5
	if l, ok := args["limit"].(float64); ok && l > 0 {
		limit = int(l)
	}

	results := s.docs.Search(query, limit)
	if len(results) == 0 {
		return fmt.Sprintf("По запросу '%s' ничего не найдено в справочнике Varwin 18.", query), nil
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("### Результаты поиска по API Varwin 18 для '%s':\n\n", query))
	for _, r := range results {
		sb.WriteString(fmt.Sprintf("#### `%s`\n```python\n%s\n```\n\n", r.ClassName, r.Snippet))
	}
	return strings.TrimSpace(sb.String()), nil
}

func (s *Server) toolGetWrapperDoc(args map[string]interface{}) (string, error) {
	name, _ := args["wrapper_name"].(string)
	doc, found := s.docs.GetWrapperDoc(name)
	if !found {
		wrappers := s.docs.ListWrappers()
		var closeNames []string
		nameLower := strings.ToLower(name)
		for _, w := range wrappers {
			if strings.Contains(strings.ToLower(w), nameLower) {
				closeNames = append(closeNames, w)
				if len(closeNames) >= 8 {
					break
				}
			}
		}
		closeHint := ""
		if len(closeNames) > 0 {
			closeHint = fmt.Sprintf("\nВозможно вы имели в виду: %s", strings.Join(closeNames, ", "))
		}
		return fmt.Sprintf("Документация для '%s' не найдена.%s", name, closeHint), nil
	}

	limit := 3500
	if len(doc) > limit {
		return doc[:limit] + "\n\n*(документация обрезана по лимиту символов)*", nil
	}
	return doc, nil
}

func launchURL(url string) error {
	switch runtime.GOOS {
	case "windows":
		return exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		return exec.Command("open", url).Start()
	default:
		return exec.Command("xdg-open", url).Start()
	}
}

func (s *Server) toolLaunchClient(args map[string]interface{}) (string, error) {
	sid, _ := args["scene_sid"].(string)
	mode, _ := args["mode"].(string)
	if mode == "" {
		mode = "desktop"
	}

	url := fmt.Sprintf("varwin-client-18://open?mode=%s", mode)
	if sid != "" {
		url += "&sceneSid=" + sid
	}

	if err := launchURL(url); err != nil {
		return fmt.Sprintf("Ошибка запуска клиента: %v", err), nil
	}
	return fmt.Sprintf("🚀 Клиент Varwin запущен через URL `%s`.", url), nil
}

func findVarwinGitCLI() (string, []string) {
	if path, err := exec.LookPath("varwin-git"); err == nil {
		return path, nil
	}
	exe, err := os.Executable()
	if err == nil {
		dir := filepath.Dir(exe)
		cand := filepath.Join(dir, "varwin-git")
		if _, err := os.Stat(cand); err == nil {
			return cand, nil
		}
		cand = filepath.Join(dir, "..", "bin", "varwin-git")
		if _, err := os.Stat(cand); err == nil {
			return cand, nil
		}
		cand = filepath.Join(dir, "..", "scripts", "varwin_git.py")
		if _, err := os.Stat(cand); err == nil {
			return "python3", []string{cand}
		}
	}
	if _, err := os.Stat("/usr/bin/varwin-git"); err == nil {
		return "/usr/bin/varwin-git", nil
	}
	return "python3", []string{"scripts/varwin_git.py"}
}

func (s *Server) toolGitExport(args map[string]interface{}) (string, error) {
	proj, _ := args["project"].(string)
	if proj == "" {
		return "❌ Ошибка: не указан проект (ID, GUID или имя)", nil
	}
	targetDir, _ := args["dir"].(string)

	bin, baseArgs := findVarwinGitCLI()
	cmdArgs := append(baseArgs, "export", proj)
	if targetDir != "" {
		cmdArgs = append(cmdArgs, "--dir", targetDir)
	}

	cmd := exec.Command(bin, cmdArgs...)
	out, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Sprintf("❌ Ошибка экспорта в Git: %v\n%s", err, string(out)), nil
	}
	return string(out), nil
}

func (s *Server) toolGitApply(args map[string]interface{}) (string, error) {
	repoDir, _ := args["dir"].(string)
	if repoDir == "" {
		repoDir = "."
	}
	nameOverride, _ := args["name"].(string)

	bin, baseArgs := findVarwinGitCLI()
	cmdArgs := append(baseArgs, "apply", "--dir", repoDir)
	if nameOverride != "" {
		cmdArgs = append(cmdArgs, "--name", nameOverride)
	}

	cmd := exec.Command(bin, cmdArgs...)
	out, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Sprintf("❌ Ошибка применения Git проекта: %v\n%s", err, string(out)), nil
	}
	return string(out), nil
}

func (s *Server) toolGitStatus(args map[string]interface{}) (string, error) {
	repoDir, _ := args["dir"].(string)
	if repoDir == "" {
		repoDir = "."
	}
	proj, _ := args["project"].(string)

	bin, baseArgs := findVarwinGitCLI()
	cmdArgs := append(baseArgs, "status")
	if proj != "" {
		cmdArgs = append(cmdArgs, proj)
	} else {
		cmdArgs = append(cmdArgs, repoDir)
	}

	cmd := exec.Command(bin, cmdArgs...)
	out, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Sprintf("❌ Ошибка получения статуса Git: %v\n%s", err, string(out)), nil
	}
	return string(out), nil
}

func (s *Server) HandleRequest(req JSONRPCRequest) *JSONRPCResponse {
	switch req.Method {
	case "initialize":
		return &JSONRPCResponse{
			JSONRPC: "2.0",
			ID:      req.ID,
			Result: map[string]interface{}{
				"protocolVersion": "2024-11-05",
				"capabilities": map[string]interface{}{
					"tools": map[string]interface{}{},
				},
				"serverInfo": map[string]interface{}{
					"name":    "varwin-mcp-go",
					"version": "2.0.0",
				},
			},
		}

	case "notifications/initialized":
		return nil

	case "ping":
		return &JSONRPCResponse{
			JSONRPC: "2.0",
			ID:      req.ID,
			Result:  map[string]interface{}{},
		}

	case "tools/list":
		var toolList []map[string]interface{}
		var sortedNames []string
		for name := range s.tools {
			sortedNames = append(sortedNames, name)
		}
		sort.Strings(sortedNames)

		for _, name := range sortedNames {
			t := s.tools[name]
			toolList = append(toolList, map[string]interface{}{
				"name":        t.Name,
				"description": t.Description,
				"inputSchema": t.InputSchema,
			})
		}

		return &JSONRPCResponse{
			JSONRPC: "2.0",
			ID:      req.ID,
			Result: map[string]interface{}{
				"tools": toolList,
			},
		}

	case "tools/call":
		toolName, _ := req.Params["name"].(string)
		args, _ := req.Params["arguments"].(map[string]interface{})
		if args == nil {
			args = make(map[string]interface{})
		}

		tool, exists := s.tools[toolName]
		if !exists {
			return &JSONRPCResponse{
				JSONRPC: "2.0",
				ID:      req.ID,
				Result: map[string]interface{}{
					"content": []map[string]interface{}{
						{
							"type": "text",
							"text": fmt.Sprintf("Error: Unknown tool '%s'", toolName),
						},
					},
					"isError": true,
				},
			}
		}

		outText, err := tool.Handler(args)
		isError := false
		if err != nil {
			outText = fmt.Sprintf("Error: %v", err)
			isError = true
		}

		return &JSONRPCResponse{
			JSONRPC: "2.0",
			ID:      req.ID,
			Result: map[string]interface{}{
				"content": []map[string]interface{}{
					{
						"type": "text",
						"text": outText,
					},
				},
				"isError": isError,
			},
		}

	default:
		if req.ID != nil {
			return &JSONRPCResponse{
				JSONRPC: "2.0",
				ID:      req.ID,
				Error: &JSONRPCError{
					Code:    -32601,
					Message: fmt.Sprintf("Method '%s' not found", req.Method),
				},
			}
		}
		return nil
	}
}

func (s *Server) RunStdio() {
	scanner := bufio.NewScanner(os.Stdin)
	buf := make([]byte, 1024*1024)
	scanner.Buffer(buf, 10*1024*1024)

	writer := bufio.NewWriter(os.Stdout)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}

		var req JSONRPCRequest
		if err := json.Unmarshal([]byte(line), &req); err != nil {
			log.Printf("JSON parse error: %v", err)
			continue
		}

		resp := s.HandleRequest(req)
		if resp != nil {
			respBytes, err := json.Marshal(resp)
			if err != nil {
				log.Printf("JSON marshal error: %v", err)
				continue
			}
			writer.Write(respBytes)
			writer.WriteByte('\n')
			writer.Flush()
		}
	}
}

func getIntArg(args map[string]interface{}, key string) int {
	if val, ok := args[key]; ok && val != nil {
		if f, ok := val.(float64); ok {
			return int(f)
		}
		if s, ok := val.(string); ok {
			if i, err := strconv.Atoi(s); err == nil {
				return i
			}
		}
	}
	return 0
}

func getFloatArg(args map[string]interface{}, key string) float64 {
	if val, ok := args[key]; ok && val != nil {
		if f, ok := val.(float64); ok {
			return f
		}
		if i, ok := val.(int); ok {
			return float64(i)
		}
		if s, ok := val.(string); ok {
			if f, err := strconv.ParseFloat(s, 64); err == nil {
				return f
			}
		}
	}
	return 0
}

func (s *Server) toolAddSceneObject(args map[string]interface{}) (string, error) {
	sceneID := getIntArg(args, "scene_id")
	objectID := getIntArg(args, "object_id")
	name, _ := args["name"].(string)
	varName, _ := args["variable_name"].(string)

	x := getFloatArg(args, "x")
	y := getFloatArg(args, "y")
	z := getFloatArg(args, "z")

	rx := getFloatArg(args, "rx")
	ry := getFloatArg(args, "ry")
	rz := getFloatArg(args, "rz")

	sx := getFloatArg(args, "sx")
	sy := getFloatArg(args, "sy")
	sz := getFloatArg(args, "sz")

	newID, err := s.client.AddSceneObject(sceneID, objectID, name, varName, x, y, z, rx, ry, rz, sx, sy, sz)
	if err != nil {
		return fmt.Sprintf("Ошибка добавления объекта: %v", err), nil
	}

	return fmt.Sprintf("✅ Объект **'%s'** (переменная: `%s`, ID: `%d`) успешно добавлен на сцену %d в координаты (X: %.2f, Y: %.2f, Z: %.2f)!", name, varName, newID, sceneID, x, y, z), nil
}
