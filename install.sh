#!/usr/bin/env bash
# Continuum installer — wires the memory hooks + /obsidian skill into Claude Code. Idempotent.
# Usage: ./install.sh [--vault "/path/to/Obsidian Vault"]
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
PY=/usr/bin/python3; command -v "$PY" >/dev/null 2>&1 || PY=python3

MEM="${CLAUDE_MEMORY_DIR:-$HOME/.claude/memory}"
HOOKS="$HOME/.claude/hooks"
SKILL="$HOME/.claude/skills/obsidian"
SETTINGS="$HOME/.claude/settings.json"
VAULT=""
[ "${1:-}" = "--vault" ] && VAULT="${2:-}"

echo "→ Continuum: installing memory system"
mkdir -p "$MEM"/{Daily,_infra} "$MEM/.recall-state" "$HOOKS" "$SKILL/scripts"

# 1. hooks + skill
cp "$REPO"/hooks/* "$HOOKS"/ && chmod +x "$HOOKS"/*.sh
cp "$REPO"/skill/obsidian/SKILL.md "$SKILL"/ && cp "$REPO"/skill/obsidian/scripts/* "$SKILL/scripts"/ && chmod +x "$SKILL"/scripts/*.py
echo "  ✓ hooks → $HOOKS ; skill → $SKILL"

# 2. seed the memory dir (only if empty of an index)
if [ ! -f "$MEM/MEMORY.md" ]; then
  cp "$REPO/templates/MEMORY.md" "$MEM/MEMORY.md"
  cp "$REPO/templates/_Home.md" "$MEM/_Home.md"
  [ -f "$MEM/context.md" ] || cp "$REPO/templates/context.md" "$MEM/context.md"
  echo "  ✓ seeded $MEM (MEMORY.md, _Home.md, context.md)"
fi

# 3. merge hook registrations into settings.json (never clobber existing hooks)
[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.continuum.bak"
"$PY" - "$SETTINGS" <<'PYE'
import json, os, sys
p = sys.argv[1]
try: d = json.load(open(p))
except Exception: d = {}
H = d.setdefault("hooks", {})
REG = {
  "SessionStart": [("session-memory.sh", 8), ("session-resume.sh", 8)],
  "UserPromptSubmit": [("memory-recall.sh", 5)],
  "Stop": [("capture-exchange.sh", 6)],
  "PostToolUse": [("memory-lint.sh", 5)],
}
def has(ev, cmd): return any(h.get("command")==cmd for e in H.get(ev,[]) for h in e.get("hooks",[]))
for ev, items in REG.items():
    arr = H.setdefault(ev, [])
    for name, to in items:
        cmd = f"bash ~/.claude/hooks/{name}"
        if has(ev, cmd): continue
        entry = {"hooks": [{"type":"command","command":cmd,"timeout":to}]}
        if ev == "PostToolUse": entry["matcher"] = "Edit|Write"
        arr.append(entry)
os.makedirs(os.path.dirname(p), exist_ok=True)
json.dump(d, open(p,"w"), indent=2); open(p,"a").write("\n")
print("  ✓ registered 5 hooks in", p, "(existing hooks preserved)")
PYE

# 4. optional Obsidian vault symlink
if [ -n "$VAULT" ] && [ -d "$VAULT" ]; then
  ln -sfn "$MEM" "$VAULT/Memory" && echo "  ✓ Obsidian: $VAULT/Memory → $MEM  (set CLAUDE_VAULT_LINK=\"$VAULT/Memory\")"
fi

cat <<DONE

✓ Continuum installed.
  • Memory dir: $MEM
  • Add templates/CLAUDE.snippet.md to your ~/.claude/CLAUDE.md so replies emit the capture footer.
  • Optional weekly upkeep:  cp "$REPO"/hooks/weekly-upkeep.sh $HOOKS/  (launchd/cron — see docs/how-it-works.md)
  • Health check:  $PY $SKILL/scripts/doctor.py
Restart Claude Code (or start a new session) to load the hooks.
DONE
