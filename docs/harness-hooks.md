# Hooks — what each can do, and how they fail

Claude Code hook events — which can block, which can inject, what each receives, and the
three failure modes that bite. Measured on Claude Code 2.1.220–2.1.233. Re-verify before
betting on any line: these are harness internals and they move between releases.

## The distinction that matters
**Security hooks are optional. Context hooks are architecture.** Do not defer them as one
category — `SessionStart` and `SubagentStart` are the loading mechanism itself, not protection.
Isolation in this workspace comes from git worktrees and reversibility, not from permissions.

## The event table
| Event | Can block? | Can inject? | Use |
|---|---|---|---|
| `SessionStart` | no | **yes** (`additionalContext`, `reloadSkills`) | boot identity/state; fires on `compact` too |
| `SubagentStart` | no | **yes** (`additionalContext`) | per-agent-type persona at spawn |
| `InstructionsLoaded` | no | no | pure observability — logs `file_path`, `load_reason`, `trigger_file_path` |
| `PreToolUse` | **yes** | yes | the only real enforcement |
| `PostCompact` / `CwdChanged` / `FileChanged` / `DirectoryAdded` | no | no | side effects only |

`InstructionsLoaded` is the cheapest high-value one: it turns "what is in my context and why"
from guesswork into a measured ledger.

**`SubagentStart.additionalContext` works** (measured 2026-08-02) — a subagent uses injected
facts. An earlier probe showing it refused was an artifact of user-scope config in the test
environment, not a property of Claude Code.

**`SessionStart` does NOT fire for in-process Task subagents** — only real sessions, interactive
or headless `-p`. Two dispatch paths exist and only one fires the hook.

## Failure mode 1 — hook failures are INVISIBLE to the model
A hook that dies takes its effect with it and says nothing the model can see. So a boot hook must
**fail open**: every path ends in exit 0, diagnostics to stderr only. And nothing may be
concluded from the absence of a symptom — check what the hook actually injected.

## Failure mode 2 — a missing script asks or hard-blocks, depending on how the command was WRITTEN
Measured 2026-08-16, Claude Code 2.1.233. Same missing file, opposite blast radius:
- **Wrapped** — `if [ -f "$H" ]; then python3 "$H"; else <ask JSON>; fi` — degrades to a prompt.
- **Bare** — `python3 <path>` — hard `Hook error`, and **the tool call is blocked outright.**

Audit the wrapping, not just the path. A guard block left pointing at deleted scripts is
harmless in the first form and bricks the machine in the second.

## Failure mode 3 — identity from an inherited env var
Measured 2026-08-16, Claude Code 2.1.233, and this one destroyed data in testing.

A `SessionStart` hook receives the agent name **twice**:
- stdin JSON `agent_type` — harness-set per session, **cannot be inherited**. Authoritative.
- `CLAUDE_CODE_AGENT` in the environment — an ordinary exported var, **inherited, not reset**.

Control: launching a blank `claude` (no `--agent`) from inside a specialist session's shell gave the
child's hook `CLAUDE_CODE_AGENT=center` while stdin `agent_type` was correctly absent. A hook
trusting the env var hands the blank session another specialist's handoff — and if the hook deletes on
pickup, destroys it.

**Reaching is not the same as being true.** Where a hook performs an irreversible act, resolve
identity from the harness-set payload only, and prefer the design that fails by doing nothing.

## `SessionStart` stdin payload
`{session_id, transcript_path, cwd, agent_type, hook_event_name, source}` — `agent_type` present
only when `--agent` was passed; `source` is `startup | resume | compact`. `CLAUDE_PROJECT_DIR` is
set for the hook process, to the launch directory.

## git `prepare-commit-msg` fires BEFORE the editor
So on a bare `git commit` the message file is empty, and a trailer appended there becomes the
**subject line** — git stops reading it as a trailer at all. Guard with an emptiness check
(`git stripspace --strip-comments`). Accepted consequence here: an interactive commit with no
`-m` gets no trailer. The only event late enough is `commit-msg`, which receives no `$2` and so
cannot distinguish a merge.

## Measuring hooks: clean-room discipline
Learned the hard way — three false findings in one session. `CLAUDE_CONFIG_DIR=<empty dir>`
severs the config *directory* but NOT exported *env vars*. A real control needs `env -i` or
explicit unsetting. **Measuring inside your own installation measures your installation.** And a
degenerate fixture measures the fixture: gate on a planted token, never on a session's
self-report.

Related: `GUIDE.md` (what loads when; memory and config scoping) · `incidents.md` #2.
