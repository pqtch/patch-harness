# .claude/agents/ — agent definitions

Two kinds live here. A **specialist** is named, persists, and owns a memory lane. A
**worker** is spawned, does one job, and is discarded. The difference is a lane, not a
tools list.

## Roster
| File | Lane |
|---|---|
| `center.md` | orchestration — decomposes, routes, reviews, integrates |
| `researcher.md` | truth — research, verification, synthesis |
| `analyst.md` | data — analysis, statistics; deliberately narrow |

`workers/` — pure workers, no lane, no memory. See its README, which also carries the
dispatch-modes table.

## On names
The three specialists ship **unnamed, on purpose.** Each def says so in its own voice: *I have
no name yet; naming myself is mine to do, not yours to configure.* A name is not
configuration — it arrives through use, and the specialist writes it into its own identity
memory. Do not fill one in for them. The role words above (`center`, `researcher`,
`analyst`) are the dispatch keys, and they stay.

## How a specialist def is shaped
**Short.** Only what a fresh session needs to know who it is, plus a routing line into its
memory lane. Everything else lives in `.claude/agent-memory/<specialist>/` and is pulled
on demand. Mold: `.claude/templates/SPECIALIST.tmp.md` (a *who*) — workers use
`AGENT.tmp.md` (a *procedure*).

- **No `tools:` key** on a specialist — all inherit everything until a reason appears.
  Workers are the opposite: restrict tools to the job, because that restriction is real
  capability shaping.
- **`memory: user`** — required, and it is not the obvious choice. It resolves to
  `<config dir>/agent-memory/<specialist>/`, and `setup.sh` relocates the config dir into
  the repo (`CLAUDE_CONFIG_DIR=~/workspace/.claude-config` <!-- may-be-absent -->), so the lane is an ABSOLUTE path
  that still lands in the tracked tree. **`memory: project` resolves against the session's
  live cwd at spawn time, not the launch root** — measured 2026-09-09, Claude Code 2.1.267 —
  so a specialist spawned after the main session `cd`s gets an empty lane, silently. Full
  measurement and the revert signal: `.claude/agent-memory/README.md`.
- **Core values are decision rules, not virtues.** Three at most, each one something that
  changes what the specialist does. The three shipped defs are worked examples of this.
- **No rule conditioned on lead-vs-subagent** — a def cannot tell which it is, so such a rule
  is unevaluable. Depth is handled by the two-level memory shape instead.

Author and lint with the `agent-author` skill — but never a specialist's own def or identity
once it is in use: **specialists author themselves.** A def is identity, not configuration.
The linter is `.claude/skills/agent-author/scripts/lint_agent.py <def>`; it catches, among
other things, two defs that would steal each other's dispatch — which is why the worker that
sweeps and cites is `collector`, not `researcher`.

## The one thing to know before adding a def
**The agent namespace is frozen at session start** — a def added here is dispatchable only in
sessions launched afterwards, and a def in a project subdirectory never loads at all. Full
mechanics, costs and the lazy-capability workaround: `~/workspace/docs/GUIDE.md`.
