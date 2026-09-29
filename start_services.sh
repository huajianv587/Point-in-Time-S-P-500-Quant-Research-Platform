#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

cd "$ROOT_DIR"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "错误: 未找到 $PYTHON_BIN。可用 PYTHON_BIN=/path/to/python3.12 ./start_services.sh" >&2
    exit 1
fi

"$PYTHON_BIN" - <<'PY'
import sys

if sys.version_info < (3, 11):
    raise SystemExit(f"需要 Python >= 3.11，当前为 {sys.version.split()[0]}")

try:
    import fastapi  # noqa: F401
    import uvicorn  # noqa: F401
except ImportError as exc:
    raise SystemExit(f"缺少运行依赖: {exc}。请先执行: {sys.executable} -m pip install -r requirements.txt")
PY

echo "Quant Terminal"
echo "项目目录: $ROOT_DIR"
echo "控制台: http://$HOST:$PORT/app/"
echo "API 文档: http://$HOST:$PORT/docs"
echo "按 Ctrl+C 停止服务"

exec "$PYTHON_BIN" -m uvicorn gateway.main:app --host "$HOST" --port "$PORT"
