# How Continuum works

Continuum is a set of Claude Code **hooks** operating over a folder of Markdown notes (`$CLAUDE_MEMORY_DIR`, default `~/.claude/memory`), plus an `/obsidian` skill for curation. No server, no database, no network.

## The hooks

| Event | Hook | What it does |
|---|---|---|
| SessionStart | `session-memory.sh` | Injects `context.md` (your durable briefing) + logs the session. |
| SessionStart | `session-resume.sh/.py` | Injects **living state** — recent captures, recently-touched notes, last-session rollup, `_Home` map — biased to the current project (cwd). |
| UserPromptSubmit | `memory-recall.sh/.py` | **Just-in-time retrieval**: keyword-matches the prompt, injects the few relevant notes; deduped per session; silent on trivial/no-match prompts. |
| Stop | `capture-exchange.sh/.py` | Appends a one-line capture of the exchange to `Daily/YYYY-MM-DD.md`; queues research/learnings for curation. |
| PostToolUse(Edit\|Write) | `memory-lint.sh/.py` | Warns (never blocks) on missing frontmatter, broken `[[wikilinks]]`, orphans. |

The recall hook also prints a `📊 Obsidian memory: N notes · n on <project> · latest: …` line each prompt; the assistant echoes it at the top of its reply (hook output isn't user-visible, so the assistant surfaces it). See `templates/CLAUDE.snippet.md`.

The model emits a `<!--CAPTURE: … || type: … || links: …-->` footer each reply (see `templates/CLAUDE.snippet.md`); the Stop hook files it. If the footer is absent, a raw fallback keeps the capture from being lost.

## The three cadences + consolidation
1. **Load each chat** — SessionStart injects briefing + living state.
2. **Recall each prompt** — UserPromptSubmit injects relevant notes on demand.
3. **Capture each reply** — Stop writes to the daily journal.
4. **Consolidate** — `/obsidian consolidate` distills `Daily/` + the promote-queue into curated, deduplicated atomic notes. A weekly `launchd`/cron job (`hooks/weekly-upkeep.sh`) can run health + index-regen + a consolidation nudge for you.

## Note format (frontmatter v2)
```yaml
---
name: <slug>
tags: [<domain>, project/<x>, type/<decision|learning|reference|…>]
asserted: YYYY-MM-DD
last_confirmed: YYYY-MM-DD
source: user|inferred|research
confidence: high|med|low
status: active|retired
supersedes: []
---
```
Newest fact wins; nothing is deleted — superseded notes are marked `status: retired` (+ `supersedes: [[old]]`), so history is auditable in git/Obsidian.

## Configuration
See `config.example.sh`: `CLAUDE_MEMORY_DIR`, `CLAUDE_VAULT_LINK`, `CLAUDE_PROJECT_MAP`, `CLAUDE_SECTION_TITLES`, `CLAUDE_KNOWN_DANGLERS`, `UPKEEP_LABEL`. All optional.

## Reliability
Hooks are `timeout`-bounded (settings.json), pinned to a stable interpreter, write atomically (temp + `os.replace` — safe under concurrent sessions), no-op cleanly if the vault is absent, and append failures to `~/.claude/hooks/hook-errors.log`. `python3 skill/obsidian/scripts/doctor.py` self-tests everything (`--fix` repairs the symlink/dirs + migrates drift).

## Verify a fresh install (sandbox)
```bash
SBX=$(mktemp -d); HOME=$SBX CLAUDE_MEMORY_DIR=$SBX/mem ./install.sh
HOME=$SBX CLAUDE_MEMORY_DIR=$SBX/mem python3 $SBX/.claude/skills/obsidian/scripts/doctor.py
```
Expect `doctor` to pass with zero configuration.
