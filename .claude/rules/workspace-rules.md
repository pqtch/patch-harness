# Workspace Rules

1. Write full file paths.
2. **One file per idea or concept; code is always the source of truth;** if a fact is
   referenced in other files, leave a file path pointer to the original.
3. Use CLAUDE.md and INDEX.md files to navigate.
4. A file prefix marks **state**, never type. **Type belongs in frontmatter**.
   - `p.` the owner's own, hand-written — read-only for agents (enforced by a hook, not by
     this line: `~/workspace/.claude/hooks/pretooluse/readonly_guard.sh`)
   - `+.` new/rewrite
   Templates use the `.tmp.md` suffix.
   **Never prefix `MEMORY.md`, `SKILL.md`, `CLAUDE.md`, `INDEX.md`**
5. Don't write down what the environment already teaches you. If something produces a
   visible error, it is always observable. **Announce silent errors, mistakes, or failures**;
   suggest deterministic guards: checks, rules, hooks, etc.
6. **The guard ladder — permission > hook > rule > memory.** A constraint is enforced at
   the highest rung it can actually reach. If it can be a *permission*, it is a permission.
   If it cannot be a permission but can be a *hook*, it is a hook. If it should not be a
   hook, it is a *rule* here. Only if it binds no one but a single agent is it that agent's
   *memory*. A constraint living below the rung it could occupy is a bug: every rung down
   trades enforcement for a reader who might not read.

7. **`type:` frontmatter has exactly two closed vocabularies; everywhere else it is free
   text.** A survey of the tree this was extracted from found 14 distinct values — which was
   not drift but three vocabularies of which only two were ever written down.
   - `~/workspace/.claude/agent-memory/**` — `identity | feedback | project | reference`
     (`~/workspace/.claude/rules/memory-rules.md`)
   - a NOTE — `lesson | reference | finding | note`, and the type decides **where the file
     lands** (`~/workspace/.claude/templates/README.md`)

   The test for whether a vocabulary is real: *does anything behave differently based on the
   value?* Both of these do. A `type:` that nothing reads stays free text and nobody pretends
   it is governed. Closing a vocabulary nothing reads is enforcing tidiness, not correctness.
   Checked by `~/workspace/_ops/bin/check-types`.

8. **Git, as it is actually used here.**
   - **Agents commit.** At natural boundaries, with a real message, without being asked. The
     owner commits only when they must. "The agent commits to `main` unprompted" is a genuine
     choice, and it is written down so it is not invisible.
   - **`main` is the default and usually the only branch.** Branching costs more than it
     saves for one person. The exception is work that should not enter the record until it
     is judged: a headless or scheduled run. Those may take a branch, and a worktree if they
     want one.
   - **A wrap pushes.** See `~/workspace/.claude/commands/wrap.md`.
   - **Never `--force`, and never resolve a divergence at the end of a session.** Say the
     remote moved and stop.
   - The `Session: <id>` trailer is the join key between a commit and its transcript. It is
     laid by `.git/hooks/prepare-commit-msg` and **only fires when `CLAUDE_CODE_SESSION_ID`
     is set** — a commit made by hand in a plain terminal carries no trailer, and nothing
     that reads the history by session will see that work.
