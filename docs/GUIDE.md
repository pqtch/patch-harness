# GUIDE — how the parts fit

Design record. Nothing here is law; the law is the structure itself. Read this when deciding
whether to *change* the shape, or when something loaded that you did not expect — or did not.
Measured lines carry a date and a Claude Code version; re-verify before betting on one.

## Progressive disclosure — the six questions
| # | Question | Answered by | When |
|---|---|---|---|
| 1 | Who are you? | specialist def + root `CLAUDE.md` | session start (frozen) |
| 2 | What are we doing? | user prompt | — |
| 3 | Where are we going? | the root routing table | session start |
| 4 | Why are we doing this? | project `CLAUDE.md` | on touch |
| 5 | When do I fetch resources? | project `.claude/skills/` | on touch |
| 6 | How do I do it? | rules / conventions | deferred — progressively disclosed too |

## Where state lives
Current state of anything belongs to the **project that owns it.** Nothing outside a project
is authoritative about it.

| Surface | Where | Lifespan | Trust | Written by |
|---|---|---|---|---|
| **brief** | `projects/<p>/CLAUDE.md` | stable; updated at wrap | law on touch | the session |
| **sticky** | `projects/<p>/.claude/STICKY.md` | to-dos + one-liner ideas | least trusted, read on demand | the session |
| **thread** | `projects/<p>/thread.<agent>.md` | ephemeral baton — deleted on pickup | handoff only | the closing session |
| **journal** | `_ops/journal/<YYYY-MM-DD>.md` | one per day, one section per session, append-only | historical record | `check-digest`, from the transcript — objective |
| **brief** (LAST) | `.claude/agent-memory/<name>/LAST.md` | overwritten every session | injected at boot; not a memory | `check-digest` |
| **proposals** | `_ops/inbox/proposals.<name>.md` | until the next boot, then deleted | filing decision for the specialist | `check-digest` |
| **note** | `_ops/inbox/<slug>.md` | distilled, pruned | durable law | whoever distilled it |

**The session IS the record.** Every commit carries a `Session: <id>` trailer; `/wrap` closes
the session — brief updated if understanding changed, leftovers to the sticky, a closing
commit, a push. End-of-session invariant: **nothing open, no confusion.** An idea too big for
a sticky line becomes a sketch or a subproject.

**Thread is a baton, not a record**: written only when clearing a session the next session
will continue (`/thread`), injected by the `SessionStart` hook when present, deleted on pickup.
Committed work is the source of truth. Its existence means a handoff is pending. Workspace-
level volatile items live in `.claude/STICKY.md`.

## The session lifecycle
1. **Launch** once, at the root: `claude` or `ws [specialist]`. Agents, root skills, commands,
   rules, settings and the boot hook all load from here and nowhere else.
2. **Walk down.** Reading any file in a directory loads that directory's `CLAUDE.md` **and**
   its `.claude/skills/`. Native Claude Code behaviour, not a local rule — which is why it is
   recorded here and not stated at boot. `/cd` is ergonomics only: it injects the target
   `CLAUDE.md` but loads no skills and no agents.
3. **Work.** Commit at natural boundaries; the trailer hook stamps each commit.
4. **Close.** `/wrap` if the topic is finished; `/thread` first if the next session will
   continue it. A wrap that does not push has not finished.

## What loads, when, and what it costs
**Skills arrive lazily and ratchet; agents do not arrive at all after boot.**

### Agents — the namespace is FROZEN at session start
Measured 2026-08-02, Claude Code 2.1.220. Nothing adds an agent mid-session — not `/cd`, not
touching a file, not `/reload-skills` (skills and commands only). The only ways in: a def in
the root `.claude/agents/` at launch; a def in the user-scope config dir's `agents/`;
`--add-dir <path>` at launch. **Identity is the one context type with no lazy path.** A def
in a project subdirectory does *not* load — unlike `.claude/skills/` beside it.

| Want | Use |
|---|---|
| a persona available everywhere | a def in the root `.claude/agents/` |
| agent-shaped behaviour that arrives lazily | a skill with `context: fork` + `agent:` |
| capability scoped to one project | `.claude/skills/` inside that project |

### Skills — lazy, but root skills are not
| Location | Loads |
|---|---|
| `<config dir>/skills/` | every project, always |
| `<root>/.claude/skills/` | session start |
| `<subdir>/.claude/skills/` | **lazily** — first time a file in that subdir is read or edited |

Once discovered, a skill stays for the session — **discovery is a one-way ratchet.** Root
skills are resident for the whole session and are paid again by every subagent spawned.
Hence: *a skill lives at root only if its absence would make output WRONG rather than merely
WORSE.* Everything else nests.

What is resident (measured 2026-08-02, Claude Code 2.1.220): every skill's `name`, always;
the `description`, usually — under budget pressure descriptions are *shortened*,
least-invoked first, and a truncated description still occupies a slot but stops dispatching
correctly (**silent degradation, not a silent delete**); the body only on invoke; anything
else bundled only on navigation. Budget is `skillListingBudgetFraction` (default 1% of the
window); per-entry cap `skillListingMaxDescChars` (default 1536). `paths:` on a skill gates
auto-activation only — the name stays in the listing. On a *rules* file, `paths:` does gate
loading; different surface.

| Key | Effect |
|---|---|
| `context: fork` + `agent:` | runs the skill in a forked subagent of that type |
| `allowed-tools:` / `disallowed-tools:` | shapes the tool pool for the invoking turn |
| `disable-model-invocation: true` | user-only — the model can never self-trigger it |
| `user-invocable: false` | model-only — hidden from the `/` menu |
| `argument-hint:` / `arguments:` | autocomplete hint and named `$arg` substitution |

### Commands — the deciding question
**Must the model notice this UNPROMPTED?** Yes → skill (its description is resident). No →
command (the body is not resident until invoked; a skill in that position is boot cost with
no dispatch). One command per job. **Every `.md` in a commands directory becomes a command —
including a `README.md`**, which shows up as a junk `/README` (observed 2026-08-16). Document
a command set elsewhere.

### Resident cost
Roughly **`28 + description_chars / 4.8` tokens** per surface listed at boot. A whole roster
is cheap; the description is also the dispatch trigger, so write it to be *picked correctly*,
not to read well.

### Discovery walls
- **Gitignore is the wall, not `.git`.** A gitignored directory is INVISIBLE to skill
  discovery — an explicit `/reload-skills` finds nothing either; `.git/info/exclude` too. A
  nested `.git` blocks nothing. Nested repos are therefore ignored **wholesale** and their own
  `.claude/` is accepted as dark; capability for such a repo goes in the tracked shell above
  the clone (`projects/INDEX.md` has the measurement).
- **`/cd` gives place, not capability.**
- **`--add-dir` asymmetry:** the launch flag loads the added dir's skills AND agents and
  bypasses gitignore; mid-session `/add-dir` refuses a path already covered. And `--add-dir`
  promotes a directory's files from DATA to INSTRUCTION authority — add only directories
  whose authors may write your system prompt.

## Memory and config scoping
### `memory: user` resolves against `$CLAUDE_CONFIG_DIR`
Not literally `~/.claude` — the config dir. The path is not configurable per agent, so a repo
that wants to own its agents' memory relocates the config dir into itself and symlinks
`agent-memory` back into the tracked tree (`setup.sh` section 3). One file, two paths: there
is no separate user-scope copy to keep in sync.

**`memory: project` is the trap** — measured 2026-09-09, Claude Code 2.1.267: it resolves
against the session's live cwd at spawn time, not the launch root, and a session that has
`cd`'d hands the specialist an empty lane, silently. `incidents.md` #5;
`.claude/agent-memory/README.md` for the revert signal. `autoMemoryDirectory` governs
main-session auto memory only and does not move a subagent lane.

### Memory injection is TRUST-GATED, and fails SILENTLY
Measured 2026-08-16, Claude Code 2.1.233. An untrusted workspace boots the agent def normally
— right identity, right voice — and simply **omits the memory injection**. The only warning
mentions *permissions*. An agent that boots as itself but amnesiac is a trust problem, not a
bridge problem: check `hasTrustDialogAccepted` in the config dir's `.claude.json` before
suspecting the symlink. Moving a repo, or cloning it to a new machine, triggers this.

### Why project knowledge does not live in agent memory
Native auto memory is scoped to the **launch repo**, not to where the session walks: one
workspace, one launch point, one shared blob resident in every session. Wrong granularity. A
project's knowledge lives in the project; its `CLAUDE.md` is its routing file.

### Where settings files are read from
- `.claude/settings.json` is read for the **launch directory** and does not cascade up from
  subdirectories. Fine with one launch point; a trap otherwise.
- `.claude/settings.local.json` is the ONLY local settings file Claude Code reads. It is
  gitignored, so it **survives operations that only touch tracked files** — a stale guard
  block inside it can outlive the tree it pointed at. `harness-hooks.md`, failure mode 2.
- `CLAUDE_CONFIG_DIR` cannot be set in a settings file: the config dir is resolved before
  settings are read. It is a shell-profile line, the one thing `setup.sh` writes outside the
  repo.

### Per-machine config is the highest-risk surface
Because it is invisible to everyone else and changes behaviour silently. A session once lost
three findings to an env var set in a local settings file, inherited by every child process,
that changed what `--add-dir` did. Nobody was wrong on purpose; the switch had no note.
**Rule: every entry in a local settings file carries a `_note` stating the consequence and
the date.** Env vars are the dangerous class — inherited by every child process, including
probe sessions, subagents, and git hooks. An env var carrying *identity* leaks down every
process tree it touches (`incidents.md` #2).

## Conventions
**Findings live with the mechanism.** A fact about how something behaves goes in the file
that does the behaving — a comment, a `_note` key, or a companion `<name>.NOTES.md` with a
pointer at the top of the source. Record the consequence, the date, and what it invalidates.
Code wins on conflict; the date tells you which side drifted.

**Molds, not examples.** Every repeated shape starts from `.claude/templates/`. A template is
exactly the file it produces; the mechanics of each surface live in the templates README.
There are no `example-*` files in live directories — an annotated example copied as a
starting point carries its explanation into the new file, where it rots.

**Measuring the harness: clean-room discipline.** `CLAUDE_CONFIG_DIR=<empty dir>` severs the
config *directory* but not exported *env vars*; a real control needs `env -i` or explicit
unsetting. Measuring inside your own installation measures your installation. Gate on a
planted token, never on a session's self-report.
