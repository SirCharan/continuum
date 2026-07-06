## Memory capture (auto-journal)
- End every substantive reply with a capture footer so the `capture-exchange` Stop hook files it into today's daily note:
  `<!--CAPTURE: <≤15-word summary> || type: decision|win|incident|context|research|learning || tags: #project/<x> || links: [[note]]-->`
- Research/learning → also write a curated atomic note in the relevant folder (v2 frontmatter, [[links]]); the Stop hook queues it in `_infra/_promote-queue.md` as a safety net that `/obsidian consolidate` sweeps.
- Frontmatter v2: `tags:[domain, project/x, type/y]`, `asserted`, `last_confirmed`, `source`, `confidence`, `status`, `supersedes`. Newest wins; never delete — set `status: retired` + `supersedes: [[old]]`.
