# Adding a new agent

## When to add one
Agents are domain specialists. Create one when an obvious recurring domain has
emerged — a subject the user returns to repeatedly that benefits from focused context
(finances, a hobby, a specific job function). Not before; premature agents rot. For a
one-off task, just do the task directly.

See `.claude/skills/agent-creation/SKILL.md` for the scaffolding steps.

## Note
A newly created agent file is invokable **next session**, not the current one — the
Agent tool enumerates available agents at session start.
