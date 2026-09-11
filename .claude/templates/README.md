# .claude/templates/ — the molds

The canonical starting shape for everything created more than once. **Copy, fill.** A
template is exactly the file it produces — placeholders in `<angle brackets>`, nothing to
strip. The structure is decided here so it is not re-improvised in every new file; the
*mechanics* of each surface (where it lands, what loads it, the failure mode it is shaped
against) live in this README, not in the files themselves.


## Index
| Template | For | Lands at |
|---|---|---|
| `CLAUDE.tmp.md` | routing table + brief | `<dir>/CLAUDE.md` |
| `INDEX.tmp.md` | routing table, read on demand | `<dir>/INDEX.md` |
| `STICKY.tmp.md` | project to-do / one-liner ideas | `<dir>/.claude/STICKY.md` |
| `THREAD.tmp.md` | the loose context two sessions on one topic share | `projects/<p>/thread.<agent>.md` |
| `JOURNAL.tmp.md` | a dated record of sessions from a particular day | `_ops/journal/<YYYY-MM-DD>.md` |
| `NOTE.tmp.md` | one atomic thing — a lesson, reference, finding, or note | next to what it is about; `_ops/inbox/<slug>.md` only when unfiled |
| `PLAN.tmp.md` | a multi-phase plan | `_ops/plans/<slug>.md` |
| `SKILL.tmp.md` | a skill | `<any>/.claude/skills/<name>/SKILL.md` |
| `AGENT.tmp.md` | a worker def — a procedure | `.claude/agents/<name>.md` |
| `SPECIALIST.tmp.md` | a specialist def — a who; ships unnamed, and says so | `.claude/agents/<name>.md` |
| `MEMORY.tmp.md` | a specialist's memory index | `<memory dir>/<specialist>/MEMORY.md` |

## Mechanics

### CLAUDE.tmp.md
Same shape at every level: root, project, topic — brief + routing table, nothing else.
Loads when ANY file in its directory is read or edited, together with the sibling
`.claude/skills/`; costs nothing until the directory is entered. This file IS the
project's memory routing file — no separate MEMORY.md. Add child CLAUDE.md in
subsections to compartmentalize context of the project. If the project becomes its own git
repo, give it a shell and one wholesale ignore line in the root `.gitignore` — and note that
its own `.claude/` then goes dark, so put the capability in the shell above it.

### INDEX.tmp.md
An INDEX is a CLAUDE.md read on demand instead of injected on touch, minus the state block.
A ROUTING TABLE: path + one sentence, nothing more. Absolute paths from `~/workspace/` so a row
is copy-pasteable from anywhere. Columns are exactly `Path | Description` — do not re-invent
the header per directory.

### STICKY.tmp.md
`<dir>/.claude/STICKY.md` — one per project. The LEAST trusted surface: to-dos and one-liner
ideas, read on demand, never injected. Written by the session — /wrap pushes anything still
open here so the end-of-session invariant ("nothing open, no confusion") holds. One line per
item, hard: an idea that needs a second line is a sketch or a subproject, and moving it is
the fix. An agent may read it to CHOOSE what to do, never to KNOW what is true.

### THREAD.tmp.md
Written only when clearing a session that the next session will
continue, at `projects/<p>/thread.<agent>.md`. The SessionStart hook injects it when it
exists; the file's own header instructs its deletion on read — its *existence* means a
thread is still waiting, so one left behind after it is read lies. (Hardening option, unruled:
the hook renames to `.consumed` on inject instead of trusting the instruction —
crash-safe and mechanical.) Content is only a blurb + pointers + a to-do list; the
record of what happened lives in transcripts + per-session diffs — nothing in a thread needs
to survive. A thread older than a few days is stale: the reader distrusts it. Write to-dos as TASK LINES — an outcome plus its status; an
instruction ("remember to X") re-fires forever and never retires itself.

### JOURNAL.tmp.md
Filename IS the key (`<YYYY-MM-DD>.md`) — no index. Written from the session's TRANSCRIPT
cross-checked against its per-session git diff (`Session: <id>` trailer) — never from
self-report alone; a maintenance run that does this in the background is the intended
writer, and until one exists the session writes its own entry at wrap. APPEND-ONLY: an entry is
never edited after the day it covers; a correction is a NEW entry — the record of having
been wrong is itself the useful part. Not a status surface: nobody reads the journal to
find out what is live. It answers "when did we…" and "why is it like this."

### NOTE.tmp.md
**Four types, and the type decides where it lands.**

| `type:` | What it is | Lands at |
|---|---|---|
| `lesson` | a law derived from experience — cross-subject, durable | `_ops/inbox/<slug>.md` until it gets a home |
| `reference` | a stable fact worth looking up again | next to the thing it describes |
| `finding` | something measured — carries the `## Measured` section | next to what was measured |
| `note` | notes taken *on* something — a class, a reading, a talk | inside the owning project, e.g. `projects/<p>/<topic>/<slug>.md` |

A `note` is the only one that is not distilled: it is capture, and it lives where the
subject lives. It never lands in `_ops/inbox/` — the inbox is for lessons with no home
yet, and a class note already has one. The `## Measured` section is `finding`-only;
delete it in the other three.

ONE fact per file — a file holding three gets recalled for one and re-read for all three.
Once the lesson is settled, CUT the evidence and keep the law; accretion is what turns a
one-sentence lesson into eighty lines nobody reads. Retrieval material, not prose. Date
anything measured and name the version — an undated finding becomes a confident lie. If it
will be stale in a week it is not a note; it belongs in the project's STICKY.md. A
`[[link]]` to a note that does not exist yet is fine — it marks one worth writing.

### PLAN.tmp.md
`_ops/plans/<slug>.md` while live · `_ops/archive/plans/<slug>.md` once dead. LOCATION IS
THE STATUS — a `status:` field requires someone to remember to update it; moving the file
is the same act as finishing. "Done when" is the whole value of a phase row: a phase
without a checkable condition completes whenever someone feels tired. A plan is not a
thread — the plan says what SHOULD happen, the thread says what IS happening; when they
disagree, the thread is right and the plan needs revising.

### SKILL.tmp.md
WHERE decides cost — the model and the root-skill test live in `.claude/skills/README.md`.
Nested
skills are lazy, discovered on first touch of their directory. The BODY is free (loads on
invoke); the DESCRIPTION is resident and is the one line to labour over. Frontmatter
behaviours (`paths:`, `context: fork` + `agent:`, `disable-model-invocation:`) — see the
skills README.

### AGENT.tmp.md / SPECIALIST.tmp.md
Two molds because they are two kinds of thing. **AGENT** is a WORKER: a procedure with no
lane and no memory, written in the third person, with an explicit output format — use it
wherever a specialist would only be costume, and restrict its `tools:` to the job. **SPECIALIST** is a
WHO: identity and values, first person, continuity across sessions. The namespace is FROZEN
at session start and the whole file is resident
from boot — mechanics, costs, and the loading routes live in `.claude/agents/README.md`.
A subagent never inherits the conversation: only the project instruction layer, the
dispatcher's cwd, and what is written into the prompt. Isolation is INBOUND ONLY — its
report comes back into the caller's window regardless.

**Depth of identity is NOT a def instruction.** The memory system handles it: `memory:`
decides whether a spawn carries memory at all, and the two-level shape does the rest —
`MEMORY.md` resident, memory files pulled only when a trigger reaches for them. A subagent
gets the index and stays shallow by default, with no rule needed.

**A def carries no rule conditioned on lead-vs-subagent** (measured, not merely ruled). Nothing in a
def can tell which one it is running as, so such a rule is unevaluable — it reads as
instruction and does nothing. An `Answering` section was drafted and cut for this reason.

### MEMORY.tmp.md
The resident index for a specialist's memory: file + type + **trigger**, nothing else. The lane is
flat — no topic folders; type lives in each memory's frontmatter and is one
of `identity` / `feedback` / `project` / `reference`, defined once in
`~/workspace/.claude/rules/memory-rules.md`.

The third column is the moment that should send you to the file, **not a summary of it**. A row
that answers its own question is payload wearing a pointer's clothes, and it invites the agent
to act on the summary instead of opening the file.

## Why mechanics live here and not in the files
A template used to end in a delete-me comment carrying its mechanics. That made every copy
a two-step act (fill, strip) with a silent failure mode (forget to strip, ship the
explanation). A mold that is exactly the produced file cannot be shipped wrong; the
explanation lives in the one place a person deciding *how to use the mold* already is.
