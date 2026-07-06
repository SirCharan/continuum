---
name: alpha-deploy-gotcha
tags: [example, project/project-alpha, type/learning]
asserted: 2025-01-01
last_confirmed: 2025-01-01
source: user
confidence: high
status: active
supersedes: []
description: "Example note — deploys need FLAG=1 or the build silently ships stale assets"
---
Setting `FLAG=1` before build is required; without it the CDN serves a stale bundle.

## Related
- [[_MOC-project-alpha]]
