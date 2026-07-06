# Why file-based memory (and not a plugin or a hosted service)

Continuum stores memory as plain Markdown you own. Two alternatives fall short for an autonomous coding agent:

## Obsidian GUI plugins can't serve a headless agent
Plugins like Dataview, Smart Connections, and Templater only run **inside the Obsidian app**. A Claude Code hook runs headless, with the app closed — so it can't query a plugin or use its embeddings. Continuum therefore builds its own headless equivalents: an index regenerator, a keyword retriever, a health auditor — all scripts over the files. (Keep the plugins for *human* browsing; they're great for that.)

## Hosted "memory" services trade ownership for convenience
They work, but your context lives on their servers, behind a subscription and an API, in a proprietary store you can't `grep`. For a lot of people that's a poor trade: memory is the most personal thing an agent holds.

## The principles Continuum follows
Drawn from proven practice in the agent-memory space (e.g. [obsidian-mind](https://github.com/breferrari/obsidian-mind), [basic-memory](https://github.com/basicmachines-co/basic-memory), [mem0](https://github.com/mem0ai/mem0), [Letta/MemGPT](https://github.com/letta-ai/letta), [Cline Memory Bank](https://docs.cline.bot/best-practices/memory-bank), and Anthropic's [context-engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)):

- **Atomic notes** — one concept per file; dense `[[wikilinks]]`; the graph accretes meaning.
- **Distill, don't dump** — consolidation merges and updates notes instead of appending duplicates.
- **Deterministic recency** — newest fact wins via explicit frontmatter, not by asking a model to judge freshness. Never auto-delete; supersede.
- **Just-in-time retrieval** — load a small index always; pull full notes only when a prompt is relevant.
- **Tiered memory** — a stable core (`context.md`, `_Home`) vs a volatile journal (`Daily/`) that gets consolidated.

The result: portable, auditable, greppable memory that you can read, edit, and keep forever — with or without this tool.
