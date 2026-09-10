# Incidents — the scars, and what each one bought

Every guard in this tree was written after the failure it refuses actually happened. This is
the record of those failures, kept because the reasoning is more useful than the rule. Dates
and harness versions are given where they were recorded; proper nouns are not, because the
mechanism is what generalizes.

## 1. A scheduled maintenance run destroyed a live hand-edit — 2026-08-16
**What happened.** A background pipeline ran with a bounded write-set and a gate rule written
as *"anything else in `git status` at gate time → full revert."* The owner was editing a file
by hand while a run was in flight. The run took the rule literally, saw a path outside its
write-set, and reverted the tree — including the human's uncommitted edit, which was lost.

**What it bought.** The rule was rewritten: **a violation aborts the run and is never
reverted.** A path outside the write-set is by definition not the pipeline's to touch; it
reverts only its own outputs, commits nothing, and names the path. The rule is a promise
that nothing outside the pipeline's surfaces is its business — not a licence to clean the
tree. The pipeline itself is held from this boilerplate until that discipline is proven from
the outside (`lineage.md`).

## 2. A specialist's identity leaked through an inherited env var — 2026-07-21, measured 2026-08-16
**What happened.** A `SessionStart` hook resolved which specialist was booting from
`CLAUDE_CODE_AGENT` in its environment. That variable is an ordinary exported var: a blank
`claude` launched from inside a specialist's shell inherits the parent's name. The hook's one
irreversible act — delivering and deleting a handoff baton — ran on the wrong session and
destroyed the baton. Verified in a clean-room test, Claude Code 2.1.233: garbage stdin plus an
inherited env var delivered and deleted another specialist's baton.

**What it bought.** The hook trusts only the harness-set stdin payload (`agent_type`), which
cannot be inherited, and the env var is not even a fallback. The launcher exports no identity
variable of its own. **Reaching a hook is not the same as being true**; where a hook does
something irreversible, resolve identity from the harness-set payload only, and prefer the
design that fails by doing nothing. `harness-hooks.md`, failure mode 3.

## 3. A commit with no pathspec swept staged files — 2026-08-26, and again 2026-09-10
**What happened.** The maintenance pipeline built a careful `add` list filtered by its
write-set, then called `git commit -m msg` with **no paths** — which commits the whole index,
including anything a human had staged and not yet committed. Found by reading the commit
path first; eleven staged files were unstaged one command before it would have swept them.

**And again.** While building this boilerplate, a probe commit made to test the `Session:`
trailer was run after a `git add -A`; it inherited eleven staged files, and the
`reset --hard HEAD~1` that followed removed them from the working tree. Recovered from the
probe commit's object. Same shape, different hands, two weeks later.

**What it bought.** The pipeline commits with an explicit pathspec. And the lesson that a
rule in a doc does not stop the person who wrote the doc: the second occurrence was by
someone who had the first one in context. The honest guard would be a hook that refuses a
pathspec-less `git commit` when the index holds more than the caller named — not written yet.

## 4. A session launched outside the tree wrote into the ledger with `git status` clean — 2026-09-09
**What happened.** A record file outside git (an append-only ledger in a gitignored
directory) received five lines from a session launched outside the workspace. That session
loaded none of the hooks; the directory was ignored; so the write raised no error and left
no diff. It was found by **mtime**. Five lines were quarantined.

**What it bought.** Nothing closed, and it ships as a standing gap: **a record outside git
needs a check that makes a foreign line detectable**, not a rule asking people to be
careful. The ledger is held with the pipeline (`lineage.md`); the shipped checks print to
stderr and write no record, which is a smaller surface, not a solution.

## 5. `memory: project` handed specialists empty lanes — measured 2026-09-09, Claude Code 2.1.267
**What happened.** Specialist defs were switched to `memory: project` on the reasoning that
the workspace is launched from one directory. The docs write that scope as a bare relative
`.claude/agent-memory/<name>/` and never say relative to what. Measured: it resolves against
the session's **live cwd at subagent-spawn time**. A main session that had `cd`'d into a
project before spawning a specialist gave that specialist an empty lane at the new cwd —
silently, and reads there missed everything the real lane held. Four stray lanes were found,
two inside gitignored directories where a write would never have shown in `git status`.

**What it bought.** `memory: user`, which resolves to an absolute path in the config dir —
and the config dir relocated into the repo with a symlink back, so the lane is both
cwd-proof and tracked. `setup.sh` section 3 exists because of this; the agent-def linter
marks `memory: project` an error; `.claude/agent-memory/README.md` carries the revert signal.

## 6. A check reported clean while scanning nothing — 2026-09-10
**What happened.** The pointer check prunes directories named `*-repo` (nested clones). Run
inside a tree whose own root directory ended in `-repo`, it pruned the root at depth zero,
scanned no files, and printed **"0 dead pointers"**. Found only because a planted dead
pointer failed to appear.

**What it bought.** `-mindepth 1` on the prune — and the rule that is now in
`.claude/hooks/README.md`: **every guard needs a positive test.** A test that asserts clean
input passes proves nothing; two of the checks in this tree shipped a bug that only a planted
failure found. The other was the leak guard's case-sensitivity prefix, which for one revision
split the entry at the wrong colon, matched the literal string `CS`, and reported clean.

## The pattern
Six incidents, one shape: **a mechanism acted on the tree's state instead of on what it had
itself produced**, or **a check passed without exercising the thing it checks.** The fixes are
the same each time — bound the write-set to what you made, and plant the failure before
trusting the pass.
