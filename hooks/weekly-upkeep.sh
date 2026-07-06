#!/usr/bin/env bash
# Weekly Obsidian memory upkeep (launchd: ${UPKEEP_LABEL:-com.continuum.upkeep}). Best-effort, fully logged.
# Default = deterministic (health report + index regen + consolidation NUDGE).
# Set OBSIDIAN_AUTO_CONSOLIDATE=1 to also run unattended `claude -p /obsidian consolidate`.
PY=/usr/bin/python3; command -v "$PY" >/dev/null 2>&1 || PY=python3
MEM="${CLAUDE_MEMORY_DIR:-$HOME/.claude/memory}"
SK="${CONTINUUM_SKILL_DIR:-$HOME/.claude/skills/obsidian/scripts}"
LOG="$HOME/.claude/hooks/upkeep.log"
[ -d "$MEM" ] || exit 0
D=$("$PY" -c "from datetime import datetime;print(datetime.now().strftime('%Y-%m-%d'))" 2>/dev/null || date +%Y-%m-%d)
mkdir -p "$MEM/Weekly"
{
  echo "=== upkeep $(date '+%Y-%m-%d %H:%M') ==="
  REV="$MEM/Weekly/$D-review.md"
  {
    printf -- '---\nname: %s-review\ntags: [meta, type/review]\n---\n\n' "$D"
    printf '# Weekly review — %s\n\n↩ [[_Home]]\n\n```\n' "$D"
    "$PY" "$SK/health.py" 2>&1
    printf '```\n'
  } > "$REV.tmp" 2>/dev/null && mv "$REV.tmp" "$REV" && echo "wrote $REV"
  "$PY" "$SK/regen-index.py" --write 2>&1 || echo "regen failed"
  DAILY_N=$(ls "$MEM/Daily/"*.md 2>/dev/null | wc -l | tr -d ' ')
  if [ "${OBSIDIAN_AUTO_CONSOLIDATE:-0}" = "1" ] && command -v claude >/dev/null 2>&1; then
    echo "auto-consolidate ON — running headless claude (max 15m)..."
    claude -p "/obsidian consolidate" >/dev/null 2>&1 & CPID=$!
    ( sleep 900; kill "$CPID" 2>/dev/null ) & WPID=$!
    if wait "$CPID" 2>/dev/null; then echo "consolidate ok"; else echo "consolidate failed/killed"; fi
    kill "$WPID" 2>/dev/null || true
  else
    printf '\n> **Consolidation due** — %s Daily file(s) to distill. Run `/obsidian consolidate` when convenient.\n' "$DAILY_N" >> "$REV"
    echo "consolidation nudge written ($DAILY_N daily files); auto-consolidate off"
  fi
  echo "=== done ==="
} >> "$LOG" 2>&1
exit 0
