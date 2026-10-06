"""
Varwin Python AST Validator & Linter.
Checks scripts against Varwin 18 engine runtime rules, threading constraints,
and event handler signatures before deployment to a scene.
"""

import ast
from typing import Any, Dict, List


class VarwinCodeValidator:
    FORBIDDEN_MODULES = {
        "asyncio": "Стандартная библиотека asyncio не поддерживается в Varwin. Используйте Varwin.Async.Run() и await Varwin.WaitForSeconds().",
        "threading": "Модуль threading запрещён — весь код должен выполняться синхронно с игровым циклом в основном потоке.",
        "multiprocessing": "Модуль multiprocessing не поддерживается игровым движком Varwin.",
        "requests": "Синхронный модуль requests блокирует кадр симуляции. Используйте await Varwin.Requests.Get/Post/Put/Delete().",
    }

    def validate(self, code_str: str, filename: str = "Main.py") -> Dict[str, Any]:
        """Validate Python code for Varwin 18 compatibility."""
        errors: List[str] = []
        warnings: List[str] = []

        try:
            tree = ast.parse(code_str, filename=filename)
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [f"Синтаксическая ошибка на строке {e.lineno}, колонка {e.offset}: {e.msg}"],
                "warnings": [],
            }

        # AST visitors
        for node in ast.walk(tree):
            # 1. Check forbidden imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name.split(".")[0]
                    if name in self.FORBIDDEN_MODULES:
                        errors.append(f"Строка {node.lineno}: Запрещённый импорт '{name}'. {self.FORBIDDEN_MODULES[name]}")
            elif isinstance(node, ast.ImportFrom):
                mod = (node.module or "").split(".")[0]
                if mod in self.FORBIDDEN_MODULES:
                    errors.append(f"Строка {node.lineno}: Запрещённый импорт из '{mod}'. {self.FORBIDDEN_MODULES[mod]}")

            # 2. Check time.sleep
            elif isinstance(node, ast.Call):
                func = node.func
                # time.sleep(...)
                if isinstance(func, ast.Attribute) and func.attr == "sleep":
                    if isinstance(func.value, ast.Name) and func.value.id == "time":
                        errors.append(f"Строка {node.lineno}: time.sleep() замораживает движок. Замените на 'await Varwin.WaitForSeconds(...)'.")

                # 3. Check Varwin.Async.AddStart / AddUpdate argument (should not be a Call)
                if isinstance(func, ast.Attribute) and func.attr in ("AddStart", "AddUpdate"):
                    if node.args and isinstance(node.args[0], ast.Call):
                        errors.append(f"Строка {node.lineno}: В Varwin.Async.{func.attr}() передаётся вызов функции вместо самой функции. Пишите: Varwin.Async.{func.attr}(MyFunc), без скобок ()!")

                # 4. Check Varwin.Async.Run argument (must be a Call or Coroutine)
                if isinstance(func, ast.Attribute) and func.attr == "Run":
                    if node.args and isinstance(node.args[0], ast.Name):
                        warnings.append(f"Строка {node.lineno}: В Varwin.Async.Run() обычно передаётся вызов корутины (результат): Varwin.Async.Run({node.args[0].id}()).")

                # 5. Check Add*Handler argument
                if isinstance(func, ast.Attribute) and func.attr.startswith("Add") and func.attr.endswith("Handler"):
                    if node.args and isinstance(node.args[0], ast.Call):
                        errors.append(f"Строка {node.lineno}: В {func.attr}() передаётся вызов функции вместо ссылки на обработчик. Передавайте саму функцию: {func.attr}(handler_func).")

            # 6. Check enum naming with None vs None_
            elif isinstance(node, ast.Attribute):
                if node.attr == "None":
                    warnings.append(f"Строка {node.lineno}: Обнаружено обращение к атрибуту '.None'. В Varwin Enum-значение для Python-слова None пишется как 'None_' (например, ControllerHand.None_).")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
