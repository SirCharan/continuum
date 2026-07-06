# Continuum

**Persistent, local-first memory for Claude Code — in your own Obsidian vault.**

**🌐 [continuum-pi-nine.vercel.app](https://continuum-pi-nine.vercel.app)**

![license](https://img.shields.io/badge/license-MIT-blue) ![version](https://img.shields.io/badge/version-0.1.0-informational) ![local](https://img.shields.io/badge/100%25-local-brightgreen) ![no telemetry](https://img.shields.io/badge/telemetry-none-success)

Your AI coding agent forgets everything between sessions. The usual fix is a hosted "memory" service that stores your context **on someone else's servers, for a monthly fee**. Continuum fixes it a different way: plain Markdown notes in **your own [Obsidian](https://obsidian.md) vault**, wired into Claude Code with a handful of hooks. It loads relevant memory into every chat and every prompt, and writes back after every reply — automatically. **Free, open-source, and your data never leaves your machine.**

No account. No API. No cloud. No lock-in. It's just files you already own.

## Why this exists

| | **Continuum** | Hosted memory SaaS |
|---|---|---|
| Where your data lives | Your disk, your vault | Their servers |
| Cost | **Free** (MIT) | $/month, per seat |
| Works offline | ✓ | ✗ |
| Open source | ✓ | usually ✗ |
| Readable/portable format | Markdown + `[[wikilinks]]` | proprietary store / vector DB |
| Telemetry | **None** | varies |
| Lock-in | None — delete the hooks, keep your notes | export, maybe |
| Editable by you | Yes — it's your Obsidian vault | Through their UI |

Same outcome — an agent that remembers — without renting your own memory back from a startup.

## Install

```bash
git clone https://github.com/SirCharan/continuum && cd continuum
./install.sh                     # or: ./install.sh --vault "/path/to/Obsidian Vault"
```

Then add `templates/CLAUDE.snippet.md` to your `~/.claude/CLAUDE.md` and start a new Claude Code session. Check it with:

```bash
python3 ~/.claude/skills/obsidian/scripts/doctor.py
```

Requires: Claude Code, Python 3.9+ (stdlib only — no pip installs), and optionally the Obsidian app to browse the graph.

## How it works — three cadences + consolidation

Continuum is a set of Claude Code **hooks** over a folder of Markdown notes:

- **Each new chat** → a `SessionStart` hook injects your `context.md` briefing + recent activity (recent captures, recently-touched notes, a rollup), project-aware from your working directory.
- **Each prompt** → a `UserPromptSubmit` hook does just-in-time retrieval: it keyword-matches your prompt against the vault and injects only the few relevant notes (deduped so nothing repeats within a session).
- **Each reply** → a `Stop` hook appends a one-line capture of the exchange to a daily note. Research/learnings are also queued for curation into permanent atomic notes.
- **Periodically** → `/obsidian consolidate` distills the daily journal into curated, deduplicated notes; a weekly job can run it for you.

Everything is plain files. Open the vault in Obsidian and you get the graph, backlinks, and search for free.

## The `/obsidian` skill

A Claude Code skill with: `capture · learn · consolidate · reconcile · link · review · health · find · prune · doctor · migrate`. Curate, search, audit, and tidy your memory in natural language.

## Reliability

Built to never break your session: every hook is `timeout`-bounded, pinned to a stable interpreter, writes atomically (safe under concurrent sessions), degrades to a no-op if the vault is missing, and logs failures instead of failing silently. `/obsidian doctor` self-tests the whole system (`--fix` repairs it).

## FAQ

- **Does it send anything anywhere?** No. Zero network calls, zero telemetry. It reads and writes local files.
- **Do I need Obsidian?** No — it's just Markdown; Obsidian makes it nice to browse. The hooks don't require the app running.
- **Will it clobber my existing Claude Code hooks?** No — the installer merges and preserves what you have.
- **Where are my notes?** `~/.claude/memory` by default (configurable via `CLAUDE_MEMORY_DIR`). They're yours.

## License

MIT. See [LICENSE](LICENSE).
