## Memory capture (auto-journal)
- End every substantive reply with a capture footer so the `capture-exchange` Stop hook files it into today's daily note:
  `<!--CAPTURE: <≤15-word summary> || type: decision|win|incident|context|research|learning || tags: #project/<x> || links: [[note]]-->`
- Research/learning → also write a curated atomic note in the relevant folder (v2 frontmatter, [[links]]); the Stop hook queues it in `_infra/_promote-queue.md` as a safety net that `/obsidian consolidate` sweeps.
- Frontmatter v2: `tags:[domain, project/x, type/y]`, `asserted`, `last_confirmed`, `source`, `confidence`, `status`, `supersedes`. Newest wins; never delete — set `status: retired` + `supersedes: [[old]]`.
- **Show the memory-stats line.** At the top of every reply, echo verbatim the `📊 Obsidian memory: …` line the `memory-recall` hook injects (total notes · N on project · latest addition). The hook's output isn't shown to the user — your reply is; so surface it. Skip only if no stats line was injected.
- **Query memory when stuck.** When a command fails ≥2×, you hit an unknown gotcha, or "have we hit this before" — before guessing or asking, run `/obsidian pull <terms>` (full-content search across notes + Daily + _system). A `stuck-detector` hook also nudges you on repeated failures.
