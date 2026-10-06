#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$REPO_DIR/bin"

echo "==> [1/2] Компиляция Varwin MCP для Linux (x86_64)..."
cd "$REPO_DIR/mcp-go"
GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o "$REPO_DIR/bin/varwin-mcp" .

echo "==> [2/2] Компиляция Varwin MCP для Windows (x86_64)..."
GOOS=windows GOARCH=amd64 go build -ldflags="-s -w" -o "$REPO_DIR/bin/varwin-mcp.exe" .

echo "==> Успешно собраны бинарники:"
ls -lh "$REPO_DIR/bin"
