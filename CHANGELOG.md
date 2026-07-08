# Changelog
All notable changes to this project are documented here. Format: [Keep a Changelog](https://keepachangelog.com); versioning: [SemVer](https://semver.org).

## [0.1.3] — unreleased
### Added
- `/obsidian pull <query>` — full-content 'unstick' search across notes + Daily + _system.
- `stuck-detector` PostToolUse(Bash) hook — nudges to query memory when the same command fails repeatedly.

## [0.1.2] — unreleased
### Changed
- The per-turn memory-stats line is now surfaced by the assistant at the TOP of each reply (the hook computes it; hook output isn't user-visible, so the CLAUDE.md snippet instructs the model to echo it).

## [0.1.1] — unreleased
### Added
- Per-turn memory stats line: every prompt now shows `📊 <N> notes · <n> on <project> · latest: <last addition>` (via the recall hook, before the gate).

## [0.1.0] — unreleased
### Added
- Initial release: file-based memory for Claude Code over an Obsidian vault.
- Hooks: session load (each chat), just-in-time recall (each prompt), capture (each reply), note-hygiene lint, weekly upkeep.
- `/obsidian` skill: capture · learn · consolidate · reconcile · link · review · health · find · prune · doctor · migrate.
- v2 frontmatter (recency/confidence/supersession), promote-queue for research/learnings, atomic writes, hook timeouts, `doctor` self-test.
- `install.sh` / `uninstall.sh` (settings-merge, non-destructive), sample vault, docs.
