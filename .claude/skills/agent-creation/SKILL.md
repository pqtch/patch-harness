---
name: agent-creation
description: Use when a recurring domain has emerged that would benefit from a dedicated agent — creating a new persona under .claude/agents/, not for one-off tasks.
---

# Agent creation

## The domain test
Only create an agent when the user has returned to the same subject repeatedly and it
would benefit from focused context (finances, a hobby, a specific job function). Not
for a single task, however complex — do that directly instead. Premature agents rot.

## Steps
1. Copy `.claude/agents/_meta/TEMPLATE.md` to `.claude/agents/<agent-name>.md`. Fill in:
   - `name`, matching the file name.
   - `description` as a dispatch trigger — the situations that should invoke it, not a
     bio.
   - `tools`, scoped to what the persona actually needs. Least privilege per
     `.claude/rules/security.md`: web-facing agents don't get `Bash`; read-only work
     doesn't get write tools.
2. Scaffold its memory: create `memories/agents/<agent-name>/` with `MEMORY.md`
   (routing index, empty to start), `craft.md` (technique it learns over time), and
   `scratch.md` (working state, wiped at `/wrap`).
3. Validate: the agent's frontmatter tool list matches what the persona needs, and it
   only ever reads `memories/shared/` plus its own folder.
4. Tell the user: the agent is invokable **next session** — the Agent tool enumerates
   available agents at session start, so it won't show up in the current one.
