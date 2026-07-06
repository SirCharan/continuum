#!/usr/bin/env bash
# non-blocking hygiene warnings for memory notes
PY=/usr/bin/python3; command -v "$PY" >/dev/null 2>&1 || PY=python3
"$PY" "$HOME/.claude/hooks/memory-lint.py" 2>/dev/null || true
exit 0
