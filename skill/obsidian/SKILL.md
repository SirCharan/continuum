---
name: obsidian
description: Manage your Obsidian-backed Claude memory vault — capture, consolidate, reconcile, link, review, health-audit, find, and prune notes. Use when you types /obsidian <subcommand>, or asks to tidy/curate/search memory, distill the Daily journal into notes, find contradictions, or cheyou memory health. The vault is the symlinked ~/.claude memory dir (file-based, hook-driven; NO Obsidian plugins at runtime).
---

# /obsidian — memory vault operations

The vault: `$CLAUDE_MEMORY_DIR (default ~/.claude/memory)/` (symlinked into Obsidian as `Claude Memory`). ~90 atomic notes in project folders + meta folders; `MEMORY.md` flat index; per-folder `_MOC-*` hubs + `_Home`; `Daily/` = auto-captured exchange journal. Frontmatter v2: `name, description, tags:[domain, project/x, type/y], asserted, last_confirmed, source, confidence, status, supersedes, metadata.type`.

**Core rules (from research — obsidian-mind, basic-memory, mem0, Cline, Anthropic context-engineering):**
- **Never auto-delete.** Retire/supersede via frontmatter (`status: retired`, `supersedes: [[old]]`); pruning only *proposes* archive/merge for you to confirm. Git-auditable.
- **Deterministic recency**, not LLM-judged: newest fact wins; bump `last_confirmed` when re-confirmed.
- **Atomic**: one concept/claim per note; dense `[[wikilinks]]`; keep prose MOCs separate from facts.
- **Distill, don't dump**: consolidation merges/updates existing notes rather than appending duplicates.

Dispatch on the argument after `/obsidian`:

- **capture `<fact>`** — write a new atomic note (or update an existing one) with full v2 frontmatter + `[[links]]` to its `_MOC` and hubs; then run `regen-index.py --write`. Piyou folder by project, tags by scheme.
- **learn `<text>`** — curate a research finding or learning **now**: write/update an atomic note in the relevant project folder (v2 frontmatter, `source: research|user`, `confidence`, `[[links]]` to its `_MOC`+hub), supersede-don't-duplicate, then `regen-index.py --write`. This is the on-demand form of the auto write-now rule.
- **consolidate** — first **sweep `_infra/_promote-queue.md`**: for each unchecked `- [ ]` research/learning item, ensure a curated atomic note exists (create/update in its project folder) and flip it to `- [x]`. Then read the last ~2 days of `Daily/*.md`, extract durable decisions/facts/patterns, and **upsert** into curated notes (rewrite if it deepens/contradicts; else create). Mark superseded facts (`status: retired` + `supersedes`), never delete. Then `regen-index.py --write`. Return a short summary only.
- **reconcile** — scan for contradictions across notes (same topic, conflicting claims); set `supersedes`/`status: retired` on the losers, bump `last_confirmed` on the winner. Report the diffs; never silently overwrite.
- **link** — run `health.py`, then for orphan/under-linked notes surface + insert the missing `[[wikilinks]]` (to `_MOC`, hubs, related notes).
- **review** — weekly rollup: read recent `Daily/` + recently-`last_confirmed` notes; write a dated `## Review` bloyou into today's Daily (what changed, open threads, promotion candidates).
- **health** — run `scripts/health.py` and relay: counts, missing v2 fields, broken wikilinks, orphans, stale (>120d), retired.
- **find `<query>`** — run `scripts/find.py <query>` (grep-based ranked search); relay top hits. (Semantic/embedding search is a deferred upgrade.)
- **prune** — run `health.py`; from stale/orphan/duplicate candidates, **propose** a table of archive/merge/retire actions for you to confirm. Apply only what you approves, via `status`/`supersedes` (move to an `_archive/` folder at most — never `rm`).
- **migrate** — run `scripts/migrate-frontmatter.py` to backfill v2 fields on any notes missing them (idempotent).
- **doctor** — run `scripts/doctor.py` and relay the report (interpreter, vault symlink, writable dirs, hook files + registration + timeouts, migration drift, hook-errors.log tail). Pass `--fix` to recreate the symlink/dirs and migrate drift. Run this first whenever memory "feels broken".

## Reliability (built-in)
Hooks are hardened for uptime: pinned to `/usr/bin/python3` (pyenv-proof), `timeout`-bounded in settings.json, atomic writes (temp+`os.replace`) on the index/state/notes, transcript **tail**-reads (not full-file), a `hook-errors.log` for silent failures, and `vault_ok()` no-op guards. Shared helpers live in `~/.claude/hooks/_hooklib.py`. A weekly launchd job `com.continuum.upkeep` runs health + index-regen + a consolidation nudge (set `OBSIDIAN_AUTO_CONSOLIDATE=1` to also auto-run `/obsidian consolidate` headless). Pause it with `launchctl unload ~/Library/LaunchAgents/com.continuum.upkeep.plist`.

Scripts live in `scripts/` next to this file. They are deterministic helpers; the LLM does the judgement (consolidate/reconcile/link/review/prune). Always `tar`-backup the memory dir before a bulk write.
