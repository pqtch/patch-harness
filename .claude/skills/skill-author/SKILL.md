---
name: skill-author
description: Use when writing a NEW skill for this workspace, or adapting one from elsewhere.
---

# Skill author

## Frontmatter contract
- `name`: matches the directory name exactly.
- `description`: the dispatch trigger. Write it so a reader picks the right skill from
  the description alone — mention the situations that should trigger it, not just
  what it does.

## Leanness rule
Shortest procedure that reliably works. No preamble, no restating the frontmatter
description in the body. If a step is obvious from the skill's name, cut it.

## Provenance stub
If adapting from an external or prior skill, add one line near the top: what it's
adapted from and what changed for this workspace. Skip this line for skills written
fresh.

## Placement
Put it under `.claude/skills/<name>/SKILL.md`. Skills are shared across all agents —
there's no per-agent skill location.
