# .claude/hooks/

| Hook | Event | Job |
|---|---|---|
| `sessionstart/thread/thread_delivery.py` | `SessionStart` | injects and deletes the baton (`thread.<agent>.md`); injects the specialist's `LAST.md` brief (kept) and its `_ops/inbox/proposals.<name>.md` (deleted) — the objective side, written by `check-digest` |
| `sessionstart/session_register.py` | `SessionStart` | appends `session_id → specialist` to `.claude-config/session-facets.tsv`; transcripts do not record the agent, this is the only join |
| `_ops/bin/check-digest` | `SessionEnd` (background) and `/wrap` | the objective record of the session: journal section, proposals, LAST brief. Writes those three and nothing else |
| `pretooluse/gitlink_guard.sh` | `PreToolUse` (Bash) | refuses a `git commit` that would stage a gitlink (mode 160000) — layer 2; layer 1 is the `.git/hooks/pre-commit` that `setup.sh` installs |
| `pretooluse/readonly_guard.sh` | `PreToolUse` (Bash) | refuses a Bash command that would mutate a `p.*` file — the half of rule 4 the `Edit(p.*)` permission cannot see |
| `pretooluse/commit_scope_guard.sh` | `PreToolUse` (Bash) | refuses `git add <paths> && git commit` when the index already holds files outside those paths — `docs/incidents.md` #3, which happened twice |

All four are registered in `~/workspace/.claude/settings.json` and resolve through
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
`_ops/bin/check-selftest` is that discipline as a script: it plants every failure below and
is run at every wrap.

Before writing one, read `~/workspace/docs/harness-hooks.md` — the event table (what can
block, what can inject) and the three failure modes, one of which destroyed a baton in
testing.
