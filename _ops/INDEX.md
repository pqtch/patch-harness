# _ops/ — the machinery

Everything that runs the workspace rather than being the work. Nothing here is ever a
source of truth about a project — the project owns that.

## Index
| Path | Description |
|---|---|
| `~/workspace/_ops/bin/` | `ws` (the launcher), `setup.sh`, the three checks, and `check-selftest` — plants every guard's failure; run at wrap |
| `~/workspace/_ops/scripts/` | one-job scripts, run by hand or by a hook <!-- may-be-absent --> |
| `~/workspace/_ops/docs/` | design records — the *why* behind YOUR structural decisions (the boilerplate's own are at `~/workspace/docs/`) |
| `~/workspace/_ops/journal/` | one dated record per day, append-only |
| `~/workspace/_ops/plans/` | LIVE plans only |
| `~/workspace/_ops/inbox/` | accepted-but-unfiled durable lessons; staging, never a destination |
| `~/workspace/_ops/archive/` | dead plans, retired docs, closed sketches, superseded anything |
| `~/workspace/_ops/private/` | gitignored — the leak guard's wordlist, and anything else that must never leave this machine <!-- may-be-absent --> |

## Location is the status
A plan in `plans/` is live. A plan in `archive/plans/` is dead. Nothing carries a `status:`
field, because a field requires someone to remember to update it, and moving a file is the
same act as finishing. A dead plan left in place reads exactly like a live one — that is
the failure mode this shape engineers out.

Archive, do not delete. The record of having been wrong is the useful part.

## Journal is a record, not a status surface
Nobody reads `journal/` to find out what is live; that is what a project's `CLAUDE.md` and
`.claude/STICKY.md` are for. The journal answers *when did we…* and *why is it like this.*
One entry per day (`<YYYY-MM-DD>.md`). Entries are never edited after the fact — a
correction is a new entry.

## The scripts convention
Any script here carries its findings **with it**:
- short enough → a comment at the top of the script
- long enough → a companion `<script>.NOTES.md` **plus a one-line pointer comment at the
  top of the script itself**, so the pointer cannot drift out of view even if the note does
- **the script wins on conflict**; the date tells you which side drifted

Every note records the **consequence**, the **date**, and **what it invalidates**. Not the
bare fact — "sets X=1" teaches nothing; "sets X=1, which makes `--add-dir` also load
CLAUDE.md; measured 2026-08-02" is the useful form.

## Why bin/ and scripts/ are near-empty
Scripts, hooks and commands are **answers**. Run the substrate first and let the friction
name what is actually needed. The automation ladder: repeatable → script · needs judgment →
skill · series of skills → agent. Climb only as high as the task demands.

What is in `bin/` exists because the workspace cannot start without it (`ws`, `setup.sh`) or
because a check was cheaper than the failure it catches (`check-pointers`, `check-types`,
`check-leak`) — not because friction asked.
