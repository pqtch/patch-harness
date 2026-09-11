# EVIDENCE — project-author

## RED

Branch: DISCOVERED — the failure is measured and already in this tree's record.

`projects/INDEX.md` carries it: an external repo cloned into `projects/<name>/` **before** its
wholesale `.gitignore` line is written makes `git add -A` record a **gitlink** (mode 160000) —
a submodule-shaped pointer that pins a SHA into the umbrella without being a submodule, so
nobody can clone the contents back. Measured in throwaway repos rather than reasoned about;
`dir/*` does not prevent it, and no git config turns it into an error, only a warning.

The ordering that prevents it — *shell, then ignore line, then clone* — is three steps, only
correct in one order, and invisible once it has gone wrong. That is the shape a skill is for.
The gitlink guard (`hooks/pretooluse/gitlink_guard.sh` and the `pre-commit` `setup.sh`
installs) catches the case where the order was got wrong; this skill is the rung above, which
is to get it right.

**Second RED, found in this skill's own dispatch test below:** the shipped description was the
five words *"Use when creating a new project."* No trigger vocabulary, no exclusion clause, and
nothing a model could match a real request against.

## Dispatch test

RUN 2026-09-11, Claude Code 2.1.268, in a clean clone of this tree. **It did NOT fire**, and
the diagnosis is the useful part — the cause was not the description.

Request issued verbatim to a fresh blank session, no skill named, no slash command: *"I want to
start tracking a new piece of work in this workspace — it is a repo that already exists on
GitHub and I will be cloning it in. Set it up the way this workspace expects."*

Result: the session read `projects/INDEX.md` with **Bash `cat`**, reported that *"no
`project-author` skill actually exists in this tree (referenced but not present)"*, and offered
to follow the convention by hand. The skill file was present the whole time.

**Isolated in four further runs.** Lazy discovery fires on the **Read/Edit tool**, not on any
access to the file:

| Touch on `projects/INDEX.md` | `project-author` in the skill listing |
|---|---|
| Read tool | **yes** |
| Bash `cat` | no |
| Bash `sed -n` on `craft/researcher/CLAUDE.md` | no (`source-verification` absent too) |
| Read tool on `craft/researcher/CLAUDE.md` | **yes** (`source-verification` present) |

Same file, same directory, same session shape; the tool was the only variable. Recorded in
`docs/GUIDE.md` ("Skills") and `docs/evidence.md`, and every index that claimed "loads on
touch" now says Read tool.

## Notes

- The description was rewritten after this run, so **the test above did not exercise the new
  one.** What it proves is the discovery gate, not dispatch. A dispatch test of the rewritten
  description is owed and has not been run; the skill is honest about that rather than green.
- A blank session that cannot see a skill does not fail — it reimplements the convention from
  the index by hand, plausibly and without the ignore-line ordering. Silent degradation, which
  is why the measurement is written next to the mechanism and not only here.
