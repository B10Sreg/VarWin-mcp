#!/usr/bin/env bash
export LD_LIBRARY_PATH="/opt/Varwin18/lib:${LD_LIBRARY_PATH:-}"
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=0

# Hardware acceleration and Vulkan/GPU optimizations for UI/Blockly
exec /opt/Varwin18/Varwin18 \
    --no-sandbox \
    --enable-gpu-rasterization \
    --enable-zero-copy \
    --ignore-gpu-blocklist \
    --enable-features=VaapiVideoDecodeLinuxGL,VaapiVideoDecoder,CanvasOopRasterization \
    "$@"
