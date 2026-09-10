# Testing a def — by spawn, not by read

A def that reads well and spawns wrong is wrong. Reading it proves only that it is coherent
prose. Two tests, in order.

## Test 1 — the dispatch test (does routing find it?)

Route a **plain-English task with the agent never named** and confirm the router picks this def
over its siblings. If you have to name the agent, you have tested nothing — you bypassed the
exact mechanism under test.

Failure here is always a `description:` problem, never a body problem
([routing-descriptions.md](routing-descriptions.md)).

**Skills have a session-boundary caveat that applies to defs too:** only `name` + `description`
load at session start, so a def created mid-session may not be dispatchable until a fresh
session. If a cold dispatch fails, confirm the session actually knows the def exists before
concluding the description is bad.

## Test 2 — spawn once for real, and gate on EFFECT

Never gate on the agent's own report. Exit 0 ≠ correct; a permission-blocked agent that says
"done" still exits 0, and a report is data, not a verdict.

Check three things against substrate:

- **Tools.** Probe an *excluded* tool and confirm it actually fails. An agent listing its tools
  accurately proves nothing about what the harness enforces.
- **Memory injection.** Specialists: `MEMORY.md` visible. Everything else: nothing. An empty
  injection where you expected one usually means the def asked for the wrong scope, not that
  the bridge broke.
- **Finish artifacts.** Did it produce what the contract says it produces?

## Gate on effect — the general rule

Verify the substrate did what the claim says: wired ≠ built, import ≠ compile, green tests ≠
correct behavior. When an agent's report and the substrate disagree, the substrate wins and the
report gets re-read for *why* it was confident.

Be equally suspicious of your own probe harness. A check that reports what you expected can be
a broken check — if a result contradicts several independent reports, re-run it printing raw
output before believing it over them.

## Done means

Gate passed with a named routing failure · kind chosen deliberately · description overlap-checked
against the FULL registry · frontmatter follows all four rules · live spawn gated on effect ·
health_check clean.
</content>
