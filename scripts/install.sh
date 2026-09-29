#!/usr/bin/env bash
# Thin wrapper around install.py — all installer logic lives there.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$SCRIPT_DIR/install.py" "$@"
elif command -v python >/dev/null 2>&1; then
    exec python "$SCRIPT_DIR/install.py" "$@"
else
    echo "noassume: python 3 is required (tried python3 and python)" >&2
    exit 1
fi
