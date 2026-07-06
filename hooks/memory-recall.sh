#!/usr/bin/env bash
# inject vault notes relevant to the current prompt (JIT recall)
PY=/usr/bin/python3; command -v "$PY" >/dev/null 2>&1 || PY=python3
"$PY" "$HOME/.claude/hooks/memory-recall.py" 2>/dev/null || true
exit 0
