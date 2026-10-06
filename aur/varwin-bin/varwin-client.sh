#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Nvidia driver + Vulkan WSI optimizations and stability fixes
export __GL_THREADED_OPTIMIZATIONS=0
export __GL_SYNC_TO_VBLANK=0
export __GL_VRR_ALLOWED=0
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json
export LD_LIBRARY_PATH="/opt/Varwin18/lib:${LD_LIBRARY_PATH:-}"

# Auto-detect screen resolution
RES=$(xdpyinfo 2>/dev/null | awk '/dimensions:/ {print $2}')
if [ -n "$RES" ]; then
    SCREEN_W=$(echo "$RES" | cut -d'x' -f1)
    SCREEN_H=$(echo "$RES" | cut -d'x' -f2)
else
    SCREEN_W=1920
    SCREEN_H=1080
fi

# Run Unity with fixed window geometry to prevent Vulkan swapchain crash on window resize
exec "$DIR/VarwinClient.real" \
    -screen-width "$SCREEN_W" \
    -screen-height "$SCREEN_H" \
    -screen-fullscreen 0 \
    "$@"
