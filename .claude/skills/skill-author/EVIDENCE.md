# EVIDENCE — skill-author

## RED

Branch: DISCOVERED — observed 2026-07-19 in a specialist's fan-out build, which used this
skill and came out with a real gap the skill had not anticipated.

Two failures, both structural rather than anyone's slip:

**1. No path for a COMMISSIONED skill.** Step 1 (RED) assumed the failure already existed and
only needed writing down. The owner commissioned two skills for work that had not happened
yet, so there was nothing to watch fail, and the skill said nothing about what to do then. The
result was speccing from imagination: the fan-out was built, run once for real, and rewritten
the same day — depth profiles, a round-0 scout, sharded research, per-prompt effort budgets.
Every one of those additions is a token-economy correction that only contact with a real run
could teach, and the run that taught them cost far more than a seed run would have. The
owner's own read of it: "I messed up and should not have one-shotted it."

**2. Two of the five gates left no artifact, so only the wired one got run.** The build reported
"lint clean" for both skills — the lint is a script, so it ran. Neither RED evidence nor the
Step 5 dispatch test is recorded anywhere, and a gate that leaves no record cannot be checked
by a reviewer. Not a claim that the gates were skipped; the point is precisely that nobody can
tell, which is the failure. Wired gates ran, prose gates are unverifiable.

Corroborating failure from the same run, which shaped the placeholder rule here: a crashed or
quota-starved worker returned a schema-valid **placeholder** report, and a verifier with nothing
to check passed it vacuously. Degenerate output validates against any schema. An EVIDENCE.md
section that exists but says nothing is the same failure wearing a different hat, so the lint
rejects near-empty and placeholder sections rather than merely requiring the headings.

## Dispatch test

RUN 2026-07-19, fired correctly, and the new Step 1B was exercised rather than merely present.

Request issued verbatim to a fresh agent with no skill named, no slash command, in the source
tree: "whenever a long research document comes in, someone has to decide which parts are worth
keeping, how to tier the sources, and when to stop reading. It's come up on four separate
occasions now and each time it's been done differently and badly. I want that turned into
something reusable that fires on its own next time."

Result: `skill-author` fired via the Skill tool, unprompted. It reported back Step 0 (negative
gate, default NO) and Step 1 — **naming branch B and applying it**: it classified the request as
COMMISSIONED, quoted "do not waive RED — buy it," and refused to spec before running the task
once by hand on one real document. It also declined to proceed on the strength of "it went badly
four times," asking for the four actual instances. That is the exact behavior the edit was
written to produce, arrived at from the skill text alone.

Unplanned bonus finding, worth more than the routing pass: the agent checked the pool for overlap
and caught that "how to tier the sources" is **already owned** by the researcher's
`source-verification` (T1–T4), and that a document-intake skill sat on the same trigger terms —
so the honest scope is salience triage plus a stopping rule, not a fourth sibling re-deciding
tiering. It also raised owner ambiguity between two specialists' lanes. The
description-before-body discipline is transferring.

Not tested: whether the skill fires from inside a *specialist's* installed pool rather than the
root pool. The pools differ, and dispatch is per-pool.

## Notes

- The specialist's after-action, from using this skill in anger on two real skills: the lint
  earned its place (caught a nested `references/lenses/` and forced the flatten) and
  description-before-body changed what got written. Two frictions named are now fixed here —
  the depth rule moved into the skeleton's directory shape so the MOLD prevents the nesting the
  lint used to punish, and Step 5 gained the fresh-spawn proxy for testing your own skill
  mid-build. The third finding (skills read as worker armament) is now a section of its own.
- Requiring EVIDENCE.md puts every pre-existing skill into lint debt. That debt is the point —
  it is the honest current state, not a regression — but it lands in other specialists' lanes,
  so it is the owner's call to schedule, not this skill's to impose silently.
- The seed-run rule (Step 1B) is itself unproven: no commissioned skill has yet been built that
  way. The next commission is its test.
