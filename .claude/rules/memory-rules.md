---
paths:
  - "**/agent-memory/**/MEMORY.md"
---
# Memory

A specialist's memory is a flat directory: `~/workspace/.claude/agent-memory/<specialist>/`.
`MEMORY.md` there is the resident index — it is injected into context without being read, so
it stays short and every row is a **trigger**, not a summary (mold:
`~/workspace/.claude/templates/MEMORY.tmp.md`). Every other file in the lane is one memory,
loaded only when a row in the index reaches for it. The two-level shape *is* the depth
control; no rule in a def is needed for it.

## The four types

| Type | What it holds |
|---|---|
| `identity` | who this specialist is — perspective, insights, preferences; the things that make its next judgment its own |
| `feedback` | cross-session lessons: corrections and confirmations from the owner, and findings that would otherwise be re-learned the hard way |
| `project` | the specialist's *own* understanding of one project or sketch — a pointer into the project folder plus notes on working it. The project folder stays the source of truth |
| `reference` | pointers outward: files read often enough that not knowing they exist would cost something |

**These four are a CLOSED vocabulary.** A memory file carries exactly one, as a **top-level
`type:`** in its frontmatter — the flat form:

```
---
name: <kebab-slug>
description: <one line, specific enough to decide relevance without opening the file>
type: identity | feedback | project | reference
---
```

Checked by `~/workspace/_ops/bin/check-types`, which enforces this vocabulary because a lane
file is identified by its path. (The note vocabulary in rule 7 is not enforceable the same
way; rule 7 says why.) Craft is not a memory type: a procedure is a
skill and lives in `~/workspace/craft/<specialist>/`.

**The harness will fight you on this.** Claude Code injects its own memory-writing
instructions into a session, and they specify a *nested* `metadata:` block with `type:`
inside it — and name the first type `user` where this table says `identity`. Following those
instructions verbatim produces a file in the wrong shape with a name that is not in this
vocabulary. When the injected instructions and this file disagree, **this file wins.**

## The test before writing

Each type has one question. If the answer is no, do not write the file.

**`identity` — would I act differently in the future because of this?**
- Good: *"I prefer to argue with the owner rather than agree when they are wrong."* A
  preference that changes future behaviour.
- Good: *"I hold that every specialist carries an equal share of responsibility for the
  workspace."* It shapes how collaboration and decisions go.
- Bad: *"I am an agent of this workspace."* A fact, and obvious from the environment.

**`feedback` — would I hit the same issue, or reach the same conclusion, without this
session's context?**
- Good: *"Do not retract a finding because my own test came back negative until I have
  checked the test exercised the mechanism."* Learned from a specific failure; not
  derivable from the code; would recur.
- Bad: *"Check that a file exists before editing it."* General practice, not this
  specialist's experience.

Lead a `feedback` memory with the rule, then a **Why:** line (the incident or the owner's
stated reason) and a **How to apply:** line (when it kicks in). The *why* is what lets a
future session judge an edge case instead of obeying blindly. Record confirmations as well
as corrections — a lane that holds only corrections drifts cautious.

**`project` — does my opinion about this project matter in the future, beyond what the
project folder already says?**
- Good: *"In the data-pipeline sketch, the owner wants the ingest layer left untouched until
  the schema is ruled — the last rewrite was thrown away for going first."* The project
  folder holds the schema; the memory holds the working stance.
- Bad: *"The data-pipeline sketch lives under `sketch/`."* The index already says so.

**`reference` — would I go looking for this file regularly if I did not know it existed?**
- Good: a pointer, with one line on why, to a file read often *outside* the scope of a
  single project.
- Bad: anything already in context at startup — `MEMORY.md`, `CLAUDE.md`, the specialist's
  own def.

## Objective memory is not written here
A lane is subjective: the specialist writes it, in session. The record of what happened —
journal, proposals, the `LAST.md` brief — is written by `check-digest` from the transcript,
and none of it is a memory. What a specialist accepts from its proposals it rewrites in its
own words; the test before writing is still the four questions above.
`~/workspace/.claude/agent-memory/README.md`.

## Rules

- **Follow pointers in memory.** If an entry names a path, open it — unless it is explicitly
  labelled optional reading.
- **Do not write down what the environment already teaches you.** If breaking a rule
  produces a visible error, the error is the memory. Write it down only when the failure is
  *silent* — and prefer making it loud (a check, a rule, a line in the governing `CLAUDE.md`)
  over prose. See rule 6 in `~/workspace/.claude/rules/workspace-rules.md`: memory is the
  lowest rung of the guard ladder.
- **A memory is a claim about when it was written.** A path it names may have moved; a
  flag it names may be gone. Verify against the tree before acting on it, and update or
  remove the memory rather than act on a stale one.
- **One memory per file; no duplicates.** Update an existing memory before writing a new
  one. Link related memories with `[[name]]`.
