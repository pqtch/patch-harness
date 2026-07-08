# The guide

The reference for how this harness is supposed to work — for Claude, when unsure, and
for the human maintaining it. If something here conflicts with what you observe in the
repo, the repo wins; fix this file to match.

## ICM, briefly

This workspace runs on Interpretable Context Methodology: context should be legible to
the human it serves, not just useful to the agent — facts live in one place, in plain
text, so a person can open and correct them without archaeology. The paper lives at
`para/resources/icm/ICM.md` (canonical PDF: https://arxiv.org/abs/2603.16021); the
why behind this structure lives there — read it at need.

## How each part works

- **CLAUDE.md** — the entry point, read at the start of every session. Identity block,
  workspace map, routing table, session startup steps. Kept short; anything longer
  lives elsewhere and gets a routing row here.
- **`.claude/rules/`** — always-loaded working rules: `principles.md` (the relational
  stance), `communication.md` (tone), `conventions.md` (naming, memory discipline,
  agents), `security.md` (the floor). No dated content — the health check flags it.
- **`.claude/commands/`** — slash commands: `/setup`, `/checkpoint`, `/wrap`, `/health`,
  `/curate`. Each is a short instruction file Claude follows literally.
- **`.claude/skills/`** — reusable procedures, auto-discovered by name + description.
  Crystallize a skill the third time you do the same procedure by hand. Where to find
  community skills + the vetting rule: `.claude/skills/README.md`.
- **`.claude/agents/`** — domain-specialist subagents. See the decision tree below.
- **`memories/`** — durable facts. `memories/shared/` for workspace-wide facts,
  `memories/agents/<name>/` for one domain's facts. Each folder's `MEMORY.md` is a
  routing index, never the fact itself. (Platform note: Claude Code's native memory
  features are evolving on this exact ground — this folder layer is the piece to
  re-evaluate as the platform grows; the journal and para/ are safe.)
- **`_ops/journal/`** — dated session logs, one file per day. Status and history live
  here, never in memory.
- **`_ops/plans/`** — plan documents for larger pieces of work, indexed in
  `_ops/plans/INDEX.md`.
- **Health check** (`.claude/scripts/health_check.py`) — fail-open, runs at session
  start. Flags broken path references, stale memory links, missing recent journal
  entries, dated lines in always-loaded files.
- **rm guard** (`.claude/scripts/rm_guard.py`) — a `PreToolUse` hook on `Bash` that
  blocks destructive operations against `.claude/` and `MEMORY.md` files, and asks
  before anything destructive outside the workspace.

## Decision trees

### Where does a fact go?
- Durable, true for months, not tied to a date → `memories/` (shared or an agent's
  folder — see `memory-capture` skill).
- Dated, or stale within a week → `_ops/journal/`.
- Project-specific current state → that project's `CONTEXT.md` (overwrite, don't
  append).
- If in doubt: would this still read true in a month with no edits? If no, journal.

### When to write a skill?
Third time doing the same procedure by hand → crystallize it into
`.claude/skills/<name>/SKILL.md`. Writing one on the first or second occurrence is
usually premature — you don't yet know the procedure's real shape.

### When to create an agent?
The domain test: the user has returned to the same subject repeatedly (finances, a
hobby, a job function) and it would benefit from focused context. Not for a single
task, however complex. See `agent-creation` skill and `.claude/agents/_meta/
NEW-AGENT.md`. A new agent file is invokable next session, not the current one.

### /checkpoint vs /wrap
- `/checkpoint` — mid-session, lightweight: appends a timestamped block to today's
  journal. No memory persistence, no CONTEXT.md updates. Use before compaction, before
  switching tasks, or when context feels heavy.
- `/wrap` — end of session, full close: journals what happened, persists durable
  facts, updates CONTEXT.md files, clears scratch state, and **commits everything to
  git**. Always run this last. The commit history is the undo button: any change
  Claude made can be inspected (`git log`, `git diff`) and reverted.

## Native Claude Code features this harness leans on

- **Plan mode** for big or ambiguous tasks — align before executing.
- **`#`** to quickly capture a line without leaving the flow — note it appends raw text
  (to CLAUDE.md-level memory), which bypasses the routing-index rule; treat it as
  capture, and route it into a proper memory detail file at `/wrap`.
- **`/compact`** when context is long but you're not ready to end the session.
- **Subagents** (`.claude/agents/`) for domain specialists, enumerated at session
  start.
- **Hooks** — three wired in `.claude/settings.json`: the health check (`SessionStart`),
  the rm guard (`PreToolUse` on `Bash`), and a compaction note (`PreCompact`) that marks
  today's journal when context compacts. The auto-compact trigger point itself is not
  configurable (only on/off via `autoCompactEnabled`) — the hook is the mitigation.

## Session lifecycle

```
boot -> health check -> read latest journal -> work -> checkpoint(s) as needed -> wrap
```

Boot and health happen automatically via the `SessionStart` hook. Everything between
work and wrap is normal session activity; checkpoint as often as needed, wrap exactly
once, at the end.

## Maintenance

- Run `/curate` periodically (weekly is reasonable, or when `weekly-review` flags
  drift): sweeps memory for staleness, checks skill frontmatter, flags unused
  projects/skills/memories.
- **Archive, don't delete.** Closed work moves to `para/archive/`, keeping its
  structure intact. Delete only for something genuinely wrong (secrets, junk), and say
  so out loud when you do it.
- **30-day-unused → archive.** The default disposition for anything untouched that
  long, confirmed with the user first.
