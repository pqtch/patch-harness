# Conventions

## Agents
Agents are domain specialists. Create one when an obvious recurring domain has
emerged — a subject the user returns to repeatedly that benefits from focused context
(finances, a hobby, a specific job function). Not before; premature agents rot.

Each agent gets `memories/agents/<name>/`: `MEMORY.md` (routing index), `craft.md`
(technique it learns), `scratch.md` (working state, wiped at `/wrap`). The
`agent-creation` skill scaffolds this.

Contract: an agent reads `memories/shared/` plus its own folder; writes only its own
folder; persists before finishing. See `.claude/agents/_meta/NEW-AGENT.md`.

## One source of truth per fact
Every fact lives in exactly one file. Other places point to it, they don't restate it.
If you notice a fact duplicated, collapse it to one place and link the rest.

## Memory discipline
- **Durable facts** (true for months, not tied to a date) → `memories/shared/MEMORY.md`
  (routing index) + a detail file. Per-agent facts → that agent's own folder.
- **Status and history** (what happened, what's next, anything dated) → `_ops/journal/`.
- **Project payload** (what a project is, current state, pointers) → that project's
  `CONTEXT.md`.
- If it'll be stale in a week, it's journal, not memory.

## Naming
- Journal: `_ops/journal/YYYY-MM/YYYY-MM-DD.md`.
- Projects: `para/projects/<kebab-case-name>/CONTEXT.md`.
- Skills: `.claude/skills/<skill-name>/SKILL.md`, frontmatter `name` matches the dir.
- Agents: `.claude/agents/<agent-name>.md`, memory at `memories/agents/<agent-name>/`.
- Plans: `_ops/plans/<kebab-case-name>.md`, indexed in `_ops/plans/INDEX.md`.

## Maintenance ritual
- `/wrap` at the end of every session: journal what happened, persist durable facts,
  wipe scratch state.
- `/curate` periodically: sweep for stale facts, unused skills, drift between the
  memory index and its detail files.
- **30-day-unused → archive.** Archive is the default move for closed-out work; delete
  is never the default. If something's truly wrong (secrets committed, junk file),
  delete it deliberately and say so — don't let it rot in para/archive/ instead.

## Leanness
Fewest words that do the job — everywhere, not just in commands. Descriptions (skills,
commands, agents) are dispatch triggers, not documentation; write them so the right one
gets picked, not so they read well in isolation. No file over ~200 lines except
scripts (and `docs/GUIDE.md`, `SETUP.md`); READMEs stay under ~40 lines. If a section
could be a link instead, link it.
