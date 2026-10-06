# Varwin 18 for Arch Linux (`varwin-bin`)

[![Arch Linux](https://img.shields.io/badge/Arch_Linux-Package-1793D1?logo=arch-linux&logoColor=white)](https://archlinux.org/)
[![License](https://img.shields.io/badge/license-Proprietary-blue.svg)](https://varwin.com/)
[![Version](https://img.shields.io/badge/version-18.5.512-green.svg)](https://dist.varwin.com/)

Нативный пакет сборки **Varwin XRMS 18** для **Arch Linux** и производных (EndeavourOS, Manjaro, CachyOS, Garuda).

Позволяет установить и запустить полную версию платформы Varwin 18 со всеми сервисами (.NET Core, Electron, Python API и 3D Unity-клиентом).

---

## ⚡ Быстрая установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/B10Sreg/VarWin-Arch.git

# 2. Перейдите в папку пакета
cd VarWin-Arch

# 3. Соберите и установите пакет
makepkg -si
```

---

## 🛠 Особенности и встроенные фиксы для Arch Linux

1. **Библиотеки обратной совместимости .NET Core 3.1 и сохранение статических сборок**:
   - Автоматически включает `libicu63` и `libssl1.1` в изолированную директорию `/opt/Varwin18/lib/` и в директории бэкенд-сервисов (не затрагивая системные OpenSSL 3 и ICU 78+).
   - Включает опцию `staticlibs`, предотвращая удаление `makepkg` нативных библиотек рантайма (`System.IO.Compression.Native.a` и др.), что исключает ошибку `failed to start library migrator: timeout exceeded`.
2. **Аппаратное GPU-ускорение Electron**:
   - Лаунчер `/usr/bin/varwin` запускает редактор с флагами аппаратной растеризации GPU, устраняя лаги в визуальном редакторе Blockly и Monaco Editor.
3. **Патч стабильности Unity Vulkan swapchain**:
   - Клиент Unity обернут в лаунчер с защитой от крашей видеодрайвера при изменении геометрии окон на современных версиях ядра и драйверах Nvidia/Mesa.
4. **Интеграция с рабочим столом**:
   - Ярлык приложения в системном меню (`Varwin 18`).
   - Регистрация системного обработчика URL-схемы `varwin-client-18://` для запуска проектов из браузера и редактора.

---

## 🚀 Запуск

- **Через терминал**:
  ```bash
  varwin
  ```
- **Через меню приложений**: найдите и запустите **Varwin 18**.

---

## 📦 Файлы пакета

- `PKGBUILD` — сценарий сборки Arch Linux.
- `.SRCINFO` — сгенерированные метаданные пакета.
- `varwin.install` — пост-установочные хуки (обновление кэшей иконок, MIME и ldconfig).
- `varwin.sh` — оптимизированный лаунчер редактора.
- `varwin-client.sh` — обёртка 3D-клиента Unity.
- `varwin18.conf` — конфигурация системного загрузчика библиотек.
- `Varwin18.desktop` / `VarwinClient18.desktop` — интеграция в среду рабочего стола.
