#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Varwin 18 Native Installer for Arch Linux
# ==============================================================================

VARWIN_DEB_URL="https://dist.varwin.com/debian/stable/18/pool/non-free/v/varwin-18/Varwin%2018.5.512.deb"
ICU63_DEB_URL="https://dist.varwin.com/debian/stable/18/pool/non-free/i/icu/libicu63_63.1-6+deb10u3_amd64.deb"
SSL11_DEB_URL="http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.24_amd64.deb"

INSTALL_DIR="/opt/Varwin18"
TMP_DIR="$(mktemp -d -t varwin-install-XXXXXX)"

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "==> [1/5] Проверка системных пакетов..."
MISSING_PKGS=()
for pkg in gtk3 libnotify nss libxss libxtst xdg-utils at-spi2-core libsecret ffmpeg binutils tar xz curl; do
    if ! pacman -Q "$pkg" &>/dev/null; then
        MISSING_PKGS+=("$pkg")
    fi
done

if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
    echo "==> Установка недостающих пакетов: ${MISSING_PKGS[*]}"
    sudo pacman -S --needed --noconfirm "${MISSING_PKGS[@]}"
else
    echo "==> Все базовые системные пакеты уже установлены."
fi

if ! pacman -Q espeak-ng &>/dev/null; then
    echo "==> Установка espeak-ng (синтез речи для ботов)..."
    sudo pacman -S --needed --noconfirm espeak-ng || echo "Предупреждение: espeak-ng пропущен."
fi

# Проверяем, распакован ли уже Varwin 18
if [ -f "$INSTALL_DIR/Varwin18" ] && [ -d "$INSTALL_DIR/services" ]; then
    echo "==> [2/5] Varwin 18 уже распакован в $INSTALL_DIR (пропускаем повторное скачивание 2 ГБ)."
else
    echo "==> [2/5] Загрузка и распаковка основного дистрибутива Varwin 18 (~1.98 GB)..."
    curl -L --progress-bar -o "$TMP_DIR/varwin.deb" "$VARWIN_DEB_URL"
    sudo mkdir -p "$INSTALL_DIR"
    cd "$TMP_DIR"
    ar x varwin.deb
    echo "==> Распаковка файлов в /opt/Varwin18..."
    sudo tar -xf data.tar.xz -C /
fi

echo "==> [3/5] Загрузка и настройка библиотек совместимости (ICU 63 и OpenSSL 1.1)..."
curl -sL --progress-bar -o "$TMP_DIR/icu63.deb" "$ICU63_DEB_URL"
curl -sL --progress-bar -o "$TMP_DIR/ssl11.deb" "$SSL11_DEB_URL"

sudo mkdir -p "$INSTALL_DIR/lib"
mkdir -p "$TMP_DIR/icu" "$TMP_DIR/ssl"

# В GNU tar для распаковки потока xz из stdin требуется флаг -J
ar p "$TMP_DIR/icu63.deb" data.tar.xz | tar -xJf - -C "$TMP_DIR/icu"
ar p "$TMP_DIR/ssl11.deb" data.tar.xz | tar -xJf - -C "$TMP_DIR/ssl"

# Копируем библиотеки в /opt/Varwin18/lib с сохранением симлинков (-a)
sudo cp -a "$TMP_DIR"/icu/usr/lib/x86_64-linux-gnu/libicu* "$INSTALL_DIR/lib/"
sudo cp -a "$TMP_DIR"/ssl/usr/lib/x86_64-linux-gnu/libssl* "$INSTALL_DIR/lib/"
sudo cp -a "$TMP_DIR"/ssl/usr/lib/x86_64-linux-gnu/libcrypto* "$INSTALL_DIR/lib/"

# Добавляем /opt/Varwin18/lib в системный кэш библиотек
echo "$INSTALL_DIR/lib" | sudo tee /etc/ld.so.conf.d/varwin18.conf > /dev/null
sudo ldconfig || true

# Копируем библиотеки к .NET Core сервисам
sudo cp -a "$INSTALL_DIR"/lib/* "$INSTALL_DIR/services/client/UrlSchemaLauncher/" 2>/dev/null || true
sudo cp -a "$INSTALL_DIR"/lib/* "$INSTALL_DIR/services/converter/" 2>/dev/null || true

echo "==> [4/5] Настройка лаунчера и песочницы..."
sudo tee /usr/local/bin/varwin-18 > /dev/null << 'EOF'
#!/usr/bin/env bash
export LD_LIBRARY_PATH="/opt/Varwin18/lib:${LD_LIBRARY_PATH:-}"
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=0
exec /opt/Varwin18/Varwin18 --no-sandbox "$@"
EOF
sudo chmod +x /usr/local/bin/varwin-18

if [ -f "$INSTALL_DIR/chrome-sandbox" ]; then
    sudo chown root:root "$INSTALL_DIR/chrome-sandbox"
    sudo chmod 4755 "$INSTALL_DIR/chrome-sandbox"
fi

echo "==> [5/5] Регистрация ярлыков рабочего стола и URL-схемы varwin-client-18://..."
sudo tee /usr/share/applications/Varwin18.desktop > /dev/null << 'EOF'
[Desktop Entry]
Name=Varwin 18
Comment=Varwin XRMS for Linux (Arch)
Exec=/usr/local/bin/varwin-18 %U
Terminal=false
Type=Application
Icon=Varwin18
Categories=Development;3DGraphics;
EOF

sudo tee /usr/share/applications/VarwinClient18.desktop > /dev/null << 'EOF'
[Desktop Entry]
Name=Varwin Client 18
Comment=Varwin Client for Linux (Arch)
Exec=env LD_LIBRARY_PATH=/opt/Varwin18/lib /opt/Varwin18/services/client/UrlSchemaLauncher/UrlSchemaLauncher %U
Terminal=false
Type=Application
MimeType=x-scheme-handler/varwin-client-18;
Icon=Varwin18
Categories=Development;3DGraphics;
NoDisplay=true
EOF

sudo update-desktop-database /usr/share/applications || true
xdg-mime default VarwinClient18.desktop x-scheme-handler/varwin-client-18

echo ""
echo "======================================================================"
echo " [OK] Установка Varwin 18 успешно завершена!"
echo " Запуск приложения:"
echo "   - В терминале:    varwin-18"
echo "   - В меню системы: Varwin 18"
echo "======================================================================"
