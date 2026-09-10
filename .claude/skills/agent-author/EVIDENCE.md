# EVIDENCE — agent-author

## RED

Branch: DISCOVERED — the failure was found in production, on 2026-07-19, reviewing a
specialist's fan-out run.

All four shipped pure-worker defs carried a **commented-out** frontmatter line:

```
# tools: TODO — minimal set for the task shape
```

A commented `tools:` line constrains nothing; the def inherits every tool. Substrate proof, not
inference: the harness's own agent listing that session reported `(Tools: All tools)` for all
four. The specialist's fan-out then dispatched 20 of these workers against political news
media — the highest-injection-risk intake in the workspace — each holding Write, Edit, Bash and
unbounded WebFetch, while the specialist's own grant had been hardened to 15 reviewed entries.
Capability inverted exactly where trust of input was lowest.

The skill already named this pitfall in prose ("A commented-out `# tools:` line read as a
constraint — it inherits everything"). It changed nothing, because prose only fires if someone
reads it at the right moment. That is the rationalization worth recording: the pitfall list felt
like a control and was documentation.

First run of the new lint widened the finding beyond the worker pool: four specialist defs
carried the same commented line, and five dormant process defs had no `tools:` line at all.
One missing mechanical check, nine defs.

## Dispatch test

RUN 2026-07-19, fired correctly, and the negative gate held.

Request issued verbatim to a fresh agent with no skill named, no slash command, in the source
tree: "We keep needing a small helper agent that takes a CSV file and returns it as a markdown
table — same job every time, no judgment involved, and lately two different spawns have done it
inconsistently. I want it set up properly in this repo, the way we set these up."

Result: `agent-author` fired via the Skill tool, unprompted. `skill-author` did not steal the
dispatch (the agent named why: the candidate is not a skill). Better than a routing pass — the
skill's Step 0 negative gate then **refused to build the agent**, citing the automation ladder,
and recommended a plain script instead, with the reasoning that inconsistency across spawns is
a symptom of putting a model in a loop that has one correct mechanical answer. An
agent-authoring skill whose most common correct output is "do not author an agent" is working.

Lint (Step 5) verified separately against the real registry: 19 defs walked; the four workers
and four specialist defs raised the `tools:` ERROR; two specialist defs clean. Two false
positives from that first walk were fixed — an inline `# comment` on a legal `memory: user`
line, and README files being parsed as defs.

Still untested: the Step 6 spawn probe (an agent spawned against an enumerated `tools:` list and
refused an excluded tool). The lint proves a decision was recorded; only that probe proves it
binds at runtime.

## Notes

- The specialist's after-action reports it did NOT fire this skill for the fan-out, and that
  this was correct: the roles were repeatable but stateless, so the negative gate points at
  armed workers rather than standing defs. It named the missing rung; it is now written into
  Step 0 as THE RUNG BELOW A DEF. A skill declining to be used is data about the gate working.
- The lint is a floor: it proves a decision was made about `tools:`, never that the enumerated
  set is correct. Only a spawn that probes an excluded tool tests that.
- Specialist defs are linted but never authored through this skill — specialists author
  themselves. Flagged specialist defs are their owners' to fix: reported, not edited.
