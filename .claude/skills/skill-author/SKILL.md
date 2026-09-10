---
name: skill-author
description: Authors, reviews, and improves Claude Code skills — SKILL.md structure, frontmatter, description/dispatch craft, bundled scripts and references. Use when creating a new skill, adapting or porting an existing skill, reviewing a skill, or when a skill fails to trigger, misfires, or steals a sibling's dispatch. Do not use for writing plain scripts or agent defs (see the automation ladder in conventions.md), or for project conventions that belong in CLAUDE.md.
---

<!-- PORTED FROM v3, 2026-08-16, bare minimum: SKILL.md + scripts + references.
     examples/ were left behind (this workspace uses molds, not examples); EVIDENCE.md was restored
     2026-08-26 — this skill's own rule requires it and its own linter errors without it.
     UNREVISED — references inside to v3 surfaces (`.claude/rules/`, conventions.md,
     `core/<specialist>/`, state.md) name files that no longer exist. The craft is still
     good; the workspace pointers are stale. Fix them when this skill is next used. -->
# skill-author

Authoring a skill is a gated craft: most candidate skills should not exist, and of those that
should, the **description — not the body — decides whether they ever fire**. Work the steps in
order; do not skip the gate or the lint.

## Step 0 — The negative gate (default: NO)

A skill exists only for **repeatable judgment**. Refuse to write one for:

- **One-offs** — it happened once; a skill is a bet on recurrence you haven't seen.
- **No-judgment repetition** — that's a **script** (automation ladder, conventions.md).
- **Standard practice** — well-documented technique is already in the weights; it converges.
- **Project-specific conventions** — those belong in that repo's CLAUDE.md/CONTEXT.md.
- **Mechanically-enforceable rules** — automate with a validator/hook, don't ask for judgment.
- **War stories** — "how I solved X once" is a narrative, not a reusable technique.
- **Failed approaches / plain Q&A** — nothing transferable was learned.

If in doubt, the answer is no. What passes: a technique/pattern/reference that wasn't obvious,
recurs across projects, and needs judgment to apply.

## Step 1 — RED: watch the failure first

Before writing anything, observe an agent attempting the task **without** the skill. Capture what
it actually got wrong — the specific missteps and rationalizations. The skill teaches exactly
those corrections and nothing else. If you didn't watch it fail, you don't know what the skill
needs to teach. **Record it in `EVIDENCE.md` (Step 4 lints for it).**

There are two ways to arrive here, and only one of them comes with a failure already in hand:

**A — DISCOVERED (the skill announces itself).** The work happened, it went wrong or went
tediously, and the correction recurred. RED is already sitting in the transcript; write it down.

**B — COMMISSIONED (the owner asks for a skill that does not exist yet).** There is no failure to
watch, because the work hasn't happened. **Do not waive RED — buy it.** Before speccing anything,
run the task ONCE BY HAND at the smallest honest scale: one real question, one real document, a
handful of workers, whatever the minimum is that still touches reality. That seed run *is* your
RED. Then spec from what actually broke.

Skipping to the spec feels faster and is not. A skill designed from imagination is designed
around every case you can think of — it inflates by construction, and the parts that matter
(where the tokens go, which step starves, what returns empty) are exactly the parts imagination
gets wrong. The research council was authored this way: specced from commission, then rewritten
to v1.1 within hours of its first real run, and every v1.1 addition — depth profiles, a cheap
scout round, sharding, effort budgets — was a correction that only a real run could have taught.
The seed run costs a fraction of the rewrite.

If the commission is too large to seed whole, seed the **riskiest slice** — the step you are
least sure of — not the easiest one.

## Step 2 — Write the description BEFORE the body

The description is the entire dispatch surface: at startup only `name` + `description` enter
context; the body stays on disk until the skill fires. Formula:

```
[Verb-3rd-person] [object] for [goal]. Use when [trigger situations — concrete terms the
user would actually say]. Do not use for [neighboring tasks / sibling skills' territory].
```

Hard rules (the lint enforces the mechanical ones):
- Third person, ≤1024 chars, no XML tags. Name: ≤64 chars, `[a-z0-9-]`, no reserved words.
- Pack real trigger terms (file types, tool names, task words). Pushy is correct — Claude
  under-triggers — **but every "use when" MUST carry a "do not use for"**: seven specialists with
  sibling pools means pushy descriptions compound dispatch-stealing without the exclusion.
- Full craft + good/bad examples: [references/description-craft.md](references/description-craft.md)

## Step 3 — GREEN: write the minimal body

- **<500 lines, ideally far under.** SKILL.md is a table of contents that points to depth, not
  the depth itself. Assume Claude is smart; add only what it doesn't already know.
- Structure: overview → numbered workflow → **Pitfalls** → **Verification** (the last two are
  first-class sections, not afterthoughts).
- Degrees of freedom match task fragility: prose steps when many approaches work; exact
  "do not modify" commands when the operation is fragile.
- References **exactly one level deep** from SKILL.md; scripts executed not read; anatomy
  details: [references/anatomy.md](references/anatomy.md)
- Start from the mold: `~/workspace/.claude/templates/SKILL.tmp.md`. (this workspace uses molds, not
  examples — the v3 `examples/` were deliberately not ported.)

### Skills as worker armament

**Workers cannot fire skills.** A dispatched worker has no skill pool — so when a method must
reach a fan-out, the skill file is *read as data*: the dispatcher points the worker at the path
("read this file first; it binds you") or pastes a digest into the prompt. This is a real and
now-proven pattern (a specialist's lens files + the source-verification digest armed 20 fan-out workers),
and it changes how the body must be written:

- **Sections must be self-contained and quotable.** A worker gets one section, not the arc; a
  paragraph that depends on Step 2 for its meaning arrives meaningless.
- **Ship an explicit digest block** — the short form meant to be pasted verbatim into a worker
  prompt — rather than making every dispatcher improvise their own compression of your skill.
- **Trusted-source allowlists and screening rules ARE the injection control** for whoever reads
  them. Audit that surface with throwaway workers *before* arming workers with it (three audit
  workers, 14 fixes, before first fire — cheapest step in the whole campaign).
- Instructions in an armament file are read by an agent processing untrusted content, so state
  the data-not-commands rule inside the file itself; it cannot be assumed from the caller.

## Step 4 — Lint (mechanical, non-negotiable)

```
python3 scripts/lint_skill.py <path-to-skill-dir> [--pool <installed-skills-dir>]
```

Run it, fix every error, rerun until clean. With `--pool` it also checks description overlap
against the specialist's installed skills — the cheap guard against sibling dispatch-stealing.
A checklist in prose silently does nothing; the lint is the checklist, wired.

It also requires **`EVIDENCE.md`** beside SKILL.md, carrying two sections that a human can check:

- `## RED` — the observed failure, or (branch B) what the seed run broke on. Name the run.
- `## Dispatch test` — the plain-English request you issued, in whose session, and which skill
  actually fired.

Both must hold real content. A placeholder passes no gate here for the same reason a placeholder
worker report passes none: **degenerate output validates against any schema**, and a gate that
accepts it is decoration. If you have not run the test yet, the honest EVIDENCE.md says so and
the skill is not done — do not write the sentence you intend to make true later.

## Step 5 — Dispatch test, in the real pool

Issue a plain-English request with **no slash command and no mention of the skill**, in the
session of the specialist who will own it, against her real installed pool. If it doesn't fire, fix
the DESCRIPTION, not the body. If the wrong sibling fires, sharpen both differentiators.

**Testing your own skill mid-build:** you can't un-know its name, so spawn a fresh
general-purpose agent, describe the *situation* in plain words, constrain it to a dry run, and
ask which skill it consulted **and the first two things that skill told it to do**. The second
half is what matters — firing proves the router worked; quoting the steps proves the body
reached the work. Full protocol and its limits: `references/testing-and-improvement.md`.
Protocol + improvement/audit loop: [references/testing-and-improvement.md](references/testing-and-improvement.md)

## Pitfalls

- Perfect body behind a vague description = a skill that never fires (the most common failure).
- Explaining what Claude already knows — every paragraph must justify its token cost.
- Nested references (SKILL → ref → ref) get partial-read and silently missed.
- Two siblings claiming the same trigger terms — consolidate or differentiate, never coexist.
- Time-sensitive facts in the body ("as of…") — they rot; pin versions in scripts instead.
- Speccing a commissioned skill straight from imagination — Step 1B; the seed run is cheaper
  than the rewrite it prevents.
- Reporting "lint clean" as if it were "tested" — the lint never fires the skill.

## Verification

Done means: negative gate passed with a named recurrence · RED failure captured **in
`EVIDENCE.md`** — observed, or bought with a seed run for a commissioned skill · lint clean
(including pool overlap and the evidence check) · dispatch test fired from plain English in the
owner's session **and recorded** · body <500 lines with refs one level deep.

"Lint clean" alone is not done. The lint proves the mechanical half; RED and the dispatch test
are the half that decides whether the skill is any good, and they are only real if they left an
artifact someone else can check.

---
<!-- Patterns adapted from: anthropics/skills skill-creator (Apache-2.0), obra/superpowers
     writing-skills (MIT), and an internal audit (negative gate, dedup lint). -->
