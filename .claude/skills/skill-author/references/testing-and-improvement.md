# Testing + improvement — proving a skill works, fixing one that doesn't

<!-- One level deep from SKILL.md. Covers: dispatch testing, the TDD loop, and the audit
     checklist for improving/adapting existing skills. -->

## Dispatch testing (the honest way)

1. Open a session **as the owning specialist**, with her **real installed pool** — not a clean
   sandbox. Sibling interference only shows up against real siblings.
2. Issue a plain-English request with **no slash command, no mention of the skill's name**
   ("can you review this PR?", "turn these notes into flashcards").
3. Outcomes:
   - **Fires** → pass. Also try one adjacent-but-out-of-scope request and confirm it does NOT fire.
   - **Doesn't fire** → the description is the problem, not the body. Add trigger terms, make
     it pushier, re-test.
   - **Wrong sibling fires / both load** → overlapping descriptions. Sharpen both
     differentiators + "do not use for" clauses, or consolidate into one skill.

### Running it on yourself — the spawn proxy

Step 5 says "in the owner's session," which is awkward when *you* are the owner: you cannot
un-know the skill's name, and a specialist mid-build has the whole design in context. The proxy that
works, and costs about thirty seconds on sonnet (used to test both authoring skills,
2026-07-19):

1. Spawn a **fresh general-purpose agent** rooted in the same repo — cold context, real pool,
   no authoring history.
2. Give it the request the way a person would say it, **naming no skill**, describing the
   *situation* rather than the artifact ("we keep redoing this by hand and it goes badly
   differently each time"), not "write a skill that…".
3. Add a hard **dry-run constraint**: do not create, write, or edit any file; work until you
   know what you'd do, then stop and report.
4. Ask it to state (a) which skills it consulted, by name, (b) the first two things that skill
   told it to do, (c) a reason not to proceed.

(b) is the part that earns the spawn. A skill can fire and still be ignored; quoting its early
steps back proves the body reached the work, not just the router. (c) surfaces whether the
negative gate is alive — for authoring skills the correct output is often "don't build this."

Caveats worth stating rather than hiding: a general-purpose agent's pool is the ROOT pool, not
a specialist's installed pool, so this proves root-pool dispatch only — sibling interference inside
a specialist's own pool still needs her session. And a session that booted before the skill was
written may hold a stale registry; test from a fresh one.

## The TDD loop (writer/tester split)

- **RED**: watch an agent attempt the task WITHOUT the skill. Capture exact missteps and
  rationalizations. This is the eval set.
- **GREEN**: write the minimal skill that corrects those specific failures. Nothing speculative.
- **REFACTOR**: rerun the task with the skill. Close the loopholes the agent found; cut what it
  never needed.
- Use two agents where it matters: Claude-A authors, Claude-B (fresh context, no authoring
  history) executes the task. The author always over-estimates clarity; the fresh reader is
  the test.

## Audit checklist (improving or adapting an existing skill)

Run this over any skill being ported, adapted, or debugged — every claudeV2/outside skill
passes through it at the door:

- [ ] **Negative gate re-check**: would we author this today? (One-off? Converged into the
      weights? Actually a script or a CLAUDE.md convention?) If it fails the gate, cut — don't adapt.
- [ ] **Description**: third person · ≤1024 · trigger terms present · "use when" present ·
      "do not use for" present · differentiates from every sibling in the target pool.
- [ ] **Lint clean**: `python3 scripts/lint_skill.py <dir> --pool <target-pool>`.
- [ ] **Paths + tools repointed**: no source-repo paths (claudeV2, old bin locations), no
      dead tool invocations. Pinned versions still correct — verify, don't trust.
- [ ] **Body diet**: cut everything the model already knows; body <500 lines; refs one level deep.
- [ ] **License/attribution**: preserved for outside-sourced material (Apache-2.0/MIT headers).
- [ ] **Dispatch test in the target specialist's real pool** (above) — the only proof that matters.

## When a live skill misbehaves

| Symptom | First suspect | Fix |
|---|---|---|
| Never fires | description too vague/narrow | trigger terms + pushy "use when" |
| Fires on wrong tasks | description too broad | scope + "do not use for" |
| Sibling steals dispatch | overlapping descriptions | differentiate both, or consolidate |
| Fires but performs badly | body (rare case) | RED-loop the failure; teach that correction only |
| Worked, then degraded | pool changed around it | re-run dispatch test against current pool |
