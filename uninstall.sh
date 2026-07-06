#!/usr/bin/env bash
# Remove Continuum hook registrations (leaves your memory notes untouched).
set -euo pipefail
PY=/usr/bin/python3; command -v "$PY" >/dev/null 2>&1 || PY=python3
SETTINGS="$HOME/.claude/settings.json"
[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.continuum.bak"
"$PY" - "$SETTINGS" <<'PYE'
import json, sys
p=sys.argv[1]
try: d=json.load(open(p))
except Exception: sys.exit(0)
names={"session-memory.sh","session-resume.sh","memory-recall.sh","capture-exchange.sh","memory-lint.sh"}
for ev, arr in d.get("hooks",{}).items():
    for e in arr: e["hooks"]=[h for h in e.get("hooks",[]) if not any(n in h.get("command","") for n in names)]
    d["hooks"][ev]=[e for e in arr if e.get("hooks")]
json.dump(d,open(p,"w"),indent=2); open(p,"a").write("\n")
print("✓ Continuum hooks unregistered. Hook files + your memory notes were left in place.")
PYE
echo "  (to fully remove: rm ~/.claude/hooks/{_hooklib,session-memory,session-resume,capture-exchange,memory-lint,memory-recall,weekly-upkeep}* ; your notes in \$CLAUDE_MEMORY_DIR are yours to keep.)"
