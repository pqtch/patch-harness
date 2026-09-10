# .claude/hooks/

| Hook | Event | Job |
|---|---|---|
| `sessionstart/thread/thread_delivery.py` | `SessionStart` | finds `thread.<agent>.md` for the booting specialist, injects it, deletes it |
| `pretooluse/gitlink_guard.sh` | `PreToolUse` (Bash) | refuses a `git commit` that would stage a gitlink (mode 160000) — layer 2; layer 1 is the `.git/hooks/pre-commit` that `setup.sh` installs |
| `pretooluse/readonly_guard.sh` | `PreToolUse` (Bash) | refuses a Bash command that would mutate a `p.*` file — the half of rule 4 the `Edit(p.*)` permission cannot see |

All three are registered in `~/workspace/.claude/settings.json` and resolve through
`$CLAUDE_PROJECT_DIR`, so nothing here carries an absolute path.

**Few hooks, deliberately.** Hooks are answers: build the substrate, run it, and let friction
name the next one. Each of the two guards here was written after the thing it refuses
actually happened — a gitlink reached a commit; a `sed -i` walked past a permission rule.
Their header comments name their blind spots, and that is the honest part.

The distinction that keeps this from being dogma: **security hooks are optional, context hooks
are architecture.** `SessionStart` and `SubagentStart` are the loading mechanism itself.

**Every guard fails OPEN.** A hook that dies of its own machinery has done more damage than
the thing it guarded against. And **every guard needs a positive test** — plant the failure
it exists to refuse and watch it refuse. A test that only checks clean input passes proves
nothing; two of the checks in this tree shipped a bug that only a planted failure found.

Before writing one, read `~/workspace/docs/harness-hooks.md` — the event table (what can
block, what can inject) and the three failure modes, one of which destroyed a baton in
testing.
