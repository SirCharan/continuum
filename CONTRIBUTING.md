# Contributing

Thanks for your interest! Continuum is intentionally small and dependency-free (Python stdlib + bash).

- **Before a PR**: run `scripts/privacy-scan.sh` (must pass) and the sandbox install test in `docs/how-it-works.md`.
- Keep hooks non-blocking (`exit 0`), fast, and `timeout`-safe. Never add a network call — this project is 100% local by design.
- Prefer files + config vars over new dependencies. No pip installs in the hot path.
- Discuss larger changes in an issue first.
