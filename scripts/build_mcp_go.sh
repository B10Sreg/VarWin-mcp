#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$REPO_DIR/bin"

echo "==> Компиляция Varwin MCP (Golang)..."
cd "$REPO_DIR/mcp-go"
go build -ldflags="-s -w" -o "$REPO_DIR/bin/varwin-mcp" .

echo "==> Успешно собрано: $REPO_DIR/bin/varwin-mcp"
ls -lh "$REPO_DIR/bin/varwin-mcp"
