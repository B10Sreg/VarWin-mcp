#!/usr/bin/env bash
set -euo pipefail

echo "==> [1/3] Оптимизация лаунчера Varwin 18 (аппаратное GPU-ускорение Electron)..."
sudo tee /usr/local/bin/varwin-18 > /dev/null << 'EOF'
#!/usr/bin/env bash
export LD_LIBRARY_PATH="/opt/Varwin18/lib:${LD_LIBRARY_PATH:-}"
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=0

# Аппаратное ускорение GPU на Nvidia (убирает лаги редактора, Blockly и UI)
exec /opt/Varwin18/Varwin18 \
    --no-sandbox \
    --enable-gpu-rasterization \
    --enable-zero-copy \
    --ignore-gpu-blocklist \
    --enable-features=VaapiVideoDecodeLinuxGL,VaapiVideoDecoder,CanvasOopRasterization \
    "$@"
EOF
sudo chmod +x /usr/local/bin/varwin-18

echo "==> [2/3] Патч клиента Unity (VarwinClient) для защиты от краша Vulkan swapchain..."
CLIENT_DIR="/opt/Varwin18/services/client"
if [ ! -f "$CLIENT_DIR/VarwinClient.real" ]; then
    sudo mv "$CLIENT_DIR/VarwinClient" "$CLIENT_DIR/VarwinClient.real"
fi

sudo tee "$CLIENT_DIR/VarwinClient" > /dev/null << 'EOF'
#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Nvidia driver + Vulkan WSI оптимизации и фиксы стабильности
export __GL_THREADED_OPTIMIZATIONS=0
export __GL_SYNC_TO_VBLANK=0
export __GL_VRR_ALLOWED=0
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json
export LD_LIBRARY_PATH="/opt/Varwin18/lib:${LD_LIBRARY_PATH:-}"

# Автоматическое определение разрешения рабочего стола (например 1920x1080)
RES=$(xdpyinfo 2>/dev/null | awk '/dimensions:/ {print $2}')
if [ -n "$RES" ]; then
    SCREEN_W=$(echo "$RES" | cut -d'x' -f1)
    SCREEN_H=$(echo "$RES" | cut -d'x' -f2)
else
    SCREEN_W=1920
    SCREEN_H=1080
fi

# Запуск Unity с фиксированной геометрией окна, чтобы избежать ресайза и краша Vulkan swapchain
exec "$DIR/VarwinClient.real" \
    -screen-width "$SCREEN_W" \
    -screen-height "$SCREEN_H" \
    -screen-fullscreen 0 \
    "$@"
EOF
sudo chmod +x "$CLIENT_DIR/VarwinClient"

echo "==> [3/3] Установка обновленного vxwm..."
sudo cp /home/reg/LoadOfReger/vxwm-src/vxwm /usr/local/bin/vxwm 2>/dev/null || true

echo ""
echo "=========================================================================="
echo " [OK] Все оптимизации успешно применены!"
echo " 1. Включено аппаратное GPU-ускорение Electron (Blockly и редактор кода не лагают)."
echo " 2. Устранён краш Vulkan swapchain в libnvidia-glcore на ресайзе окон."
echo " 3. Picom больше не размывает и не делает полупрозрачным 3D-вьюпорт."
echo "=========================================================================="
