package validator

import (
	"bytes"
	"fmt"
	"os/exec"
	"regexp"
	"strings"
)

type ValidationResult struct {
	Valid    bool     `json:"valid"`
	Errors   []string `json:"errors"`
	Warnings []string `json:"warnings"`
}

type VarwinCodeValidator struct {
	forbiddenModules map[string]string
}

func NewVarwinCodeValidator() *VarwinCodeValidator {
	return &VarwinCodeValidator{
		forbiddenModules: map[string]string{
			"asyncio":         "Стандартная библиотека asyncio не поддерживается в Varwin. Используйте Varwin.Async.Run() и await Varwin.WaitForSeconds().",
			"threading":       "Модуль threading запрещён — весь код должен выполняться синхронно с игровым циклом в основном потоке.",
			"multiprocessing": "Модуль multiprocessing не поддерживается игровым движком Varwin.",
			"requests":        "Синхронный модуль requests блокирует кадр симуляции. Используйте await Varwin.Requests.Get/Post/Put/Delete().",
		},
	}
}

var (
	reImportSimple   = regexp.MustCompile(`^\s*import\s+([a-zA-Z0-9_]+)`)
	reImportFrom     = regexp.MustCompile(`^\s*from\s+([a-zA-Z0-9_]+)\s+import`)
	reTimeSleep      = regexp.MustCompile(`\btime\.sleep\s*\(`)
	reAddStartUpdate = regexp.MustCompile(`Varwin\.Async\.(AddStart|AddUpdate)\s*\(\s*([a-zA-Z0-9_]+)\s*\(`)
	reAddHandlerCall = regexp.MustCompile(`\b(Add[a-zA-Z0-9_]*Handler)\s*\(\s*([a-zA-Z0-9_]+)\s*\(`)
	reEnumDotNone    = regexp.MustCompile(`\b([a-zA-Z0-9_]+)\.None\b`)
)

func (v *VarwinCodeValidator) Validate(codeStr string, filename string) ValidationResult {
	if filename == "" {
		filename = "Main.py"
	}

	var errors []string
	var warnings []string

	// 1. Python AST syntax check if python3 exists
	if pyPath, err := exec.LookPath("python3"); err == nil {
		checkScript := `
import ast, sys
try:
    ast.parse(sys.stdin.read(), filename=sys.argv[1])
except SyntaxError as e:
    print(f"Синтаксическая ошибка на строке {e.lineno}, колонка {e.offset}: {e.msg}")
    sys.exit(1)
`
		cmd := exec.Command(pyPath, "-c", checkScript, filename)
		cmd.Stdin = strings.NewReader(codeStr)
		var out bytes.Buffer
		cmd.Stdout = &out
		cmd.Stderr = &out
		if err := cmd.Run(); err != nil {
			msg := strings.TrimSpace(out.String())
			if msg != "" {
				return ValidationResult{
					Valid:    false,
					Errors:   []string{msg},
					Warnings: []string{},
				}
			}
		}
	}

	lines := strings.Split(codeStr, "\n")
	for idx, line := range lines {
		lineNo := idx + 1
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "#") {
			continue
		}

		// Check import
		if m := reImportSimple.FindStringSubmatch(trimmed); len(m) > 1 {
			mod := m[1]
			if reason, exists := v.forbiddenModules[mod]; exists {
				errors = append(errors, fmt.Sprintf("Строка %d: Запрещённый импорт '%s'. %s", lineNo, mod, reason))
			}
		} else if m := reImportFrom.FindStringSubmatch(trimmed); len(m) > 1 {
			mod := m[1]
			if reason, exists := v.forbiddenModules[mod]; exists {
				errors = append(errors, fmt.Sprintf("Строка %d: Запрещённый импорт из '%s'. %s", lineNo, mod, reason))
			}
		}

		// Check time.sleep
		if reTimeSleep.MatchString(trimmed) {
			errors = append(errors, fmt.Sprintf("Строка %d: time.sleep() замораживает движок. Замените на 'await Varwin.WaitForSeconds(...)'.", lineNo))
		}

		// Check Varwin.Async.AddStart / AddUpdate call instead of func reference
		if m := reAddStartUpdate.FindStringSubmatch(trimmed); len(m) > 2 {
			method := m[1]
			funcName := m[2]
			errors = append(errors, fmt.Sprintf("Строка %d: В Varwin.Async.%s() передаётся вызов функции вместо самой функции. Пишите: Varwin.Async.%s(%s), без скобок ()!", lineNo, method, method, funcName))
		}

		// Check Add*Handler call instead of func reference
		if m := reAddHandlerCall.FindStringSubmatch(trimmed); len(m) > 2 {
			method := m[1]
			funcName := m[2]
			errors = append(errors, fmt.Sprintf("Строка %d: В %s() передаётся вызов функции вместо ссылки на обработчик. Передавайте саму функцию: %s(%s).", lineNo, method, method, funcName))
		}

		// Check .None vs .None_
		if m := reEnumDotNone.FindStringSubmatch(trimmed); len(m) > 1 {
			prefix := m[1]
			if prefix != "None" && !strings.HasSuffix(trimmed, ".None_") {
				warnings = append(warnings, fmt.Sprintf("Строка %d: Обнаружено обращение к атрибуту '.None'. В Varwin Enum-значение для Python-слова None пишется как 'None_' (например, %s.None_).", lineNo, prefix))
			}
		}
	}

	return ValidationResult{
		Valid:    len(errors) == 0,
		Errors:   errors,
		Warnings: warnings,
	}
}
