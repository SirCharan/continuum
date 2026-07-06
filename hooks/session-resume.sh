#!/usr/bin/env bash
# inject living Obsidian state on fresh chats
PY=/usr/bin/python3; command -v "$PY" >/dev/null 2>&1 || PY=python3
"$PY" "$HOME/.claude/hooks/session-resume.py" 2>/dev/null || true
exit 0
