# .claude/agent-memory/ — specialist memory

One directory per specialist, here, in the repo. **Flat** — no topic folders
(ruled 2026-08-19):

```
.claude/agent-memory/<specialist>/
├── MEMORY.md          # resident index — file | type | trigger. Mold: templates/MEMORY.tmp.md
└── <memory>.md        # every memory sits here; type lives in its frontmatter
```

Four types — `identity` · `feedback` · `project` · `reference` — defined once in
`~/workspace/.claude/rules/memory-rules.md`, which fires on touching any file under here.
Do not restate the table in a lane. **The project folder is still the source of truth about a
project**; a `project` memory is a pointer plus the specialist's own notes on working it.

Craft is not a memory type. Procedures are skills: `~/workspace/craft/<specialist>/`.

## The two-level shape does the depth control
`MEMORY.md` is resident — it is injected into context without being read. Everything else loads
only when a trigger in the index reaches for it. So a subagent gets the index and stays shallow
by default; no rule in the def is needed, and none would be evaluable anyway.

This is why an index row is a **trigger, not a description**. The row's whole job is to answer
"should I open this now?" — a summary invites the agent to act on the summary instead.

**Revisit the flat shape if a lane passes ~15 files.** Below that, a folder layer costs more
than it returns: its index rows name categories, which tell an agent nothing the type column
does not already.

## Where the lane resolves — `memory: user`, and why (measured 2026-09-09)

Every def carries **`memory: user`**, which resolves to `<config dir>/agent-memory/<specialist>/`.
The config dir is relocated into the repo:

```
CLAUDE_CONFIG_DIR=~/workspace/.claude-config      # set in ~/.bashrc
~/workspace/.claude-config/agent-memory  ->  ../.claude/agent-memory   # symlink
```

So a lane resolves to an **absolute** path, and lands in the tracked tree at
`~/workspace/.claude/agent-memory/<specialist>/` — the path every doc in this workspace names.

**`memory: project` is the trap, and it bit.** MEASURED 2026-09-09, Claude Code 2.1.267: `project`
resolves against the session's **live cwd at subagent-spawn time**, not the launch root. The
docs write it as a bare relative `.claude/agent-memory/<name>/` and never say relative to
what. A main session that has `cd`'d before spawning a specialist hands that specialist an **empty lane
at the new cwd**, silently — and reads there miss everything the root lane holds.

Four such stray lanes were found in the tree this was extracted from. All were empty, so
nothing was lost. Two were inside **gitignored** directories, where a write would never have
shown up in `git status` at all.

Verified after the switch, from a session whose cwd was a project subdirectory: a spawned
agent reported its memory dir as `<config dir>/agent-memory/<name>/`, its lane landed in the
tracked tree through the symlink, and **no scaffolding was created at the cwd.**

**Subagents cannot move their own lane** — `cd` does not persist between a subagent's Bash
calls, and does not affect the parent's cwd. So all drift came from the MAIN session's `cd`,
and nothing about an agent's freedom to move around is restricted by this.

**What does NOT fix it:** `autoMemoryDirectory` governs main-session auto memory only — tested
2026-09-09, it does not move a subagent lane. There is no settings key for this and no path
form for `memory:`; the scope value is the only lever.

**The revert signal.** If a lane comes back empty, or an `agent-memory/` directory appears
anywhere that is not `~/workspace/.claude/agent-memory/`, something is resolving against cwd
again. The `.claude-config/agent-memory` symlink is the load-bearing piece — if it is missing
after a fresh clone, lanes will land in `.claude-config/` directly instead of the tracked tree.

## Why project knowledge does NOT live here
Native auto memory is scoped to the **launch repo**, not to where the session walks: one
workspace, one launch point, one shared blob resident in every session. Wrong granularity. So a
project's knowledge lives in the project and its `CLAUDE.md` is its routing file.
