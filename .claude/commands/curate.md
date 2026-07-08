---
description: Periodic memory/skill hygiene pass — stale facts, unused skills, index drift
---

1. Read `memories/shared/MEMORY.md` and every per-agent `MEMORY.md`. For each entry,
   check the detail file still exists and still reads true. Flag anything stale or
   contradicted by current project state.
2. Check every skill's frontmatter still matches its directory name and description.
3. Anything (project, skill, memory) unused for 30+ days: propose moving it to
   `para/archive/` (never delete outright — see conventions.md). Confirm with the user
   before moving.
4. Report what you found and what you changed.
