#!/usr/bin/env bash
# file a one-line capture of the finished exchange into today's daily note
PY=/usr/bin/python3; command -v "$PY" >/dev/null 2>&1 || PY=python3
"$PY" "$HOME/.claude/hooks/capture-exchange.py" 2>/dev/null || true
exit 0
