# Skill anatomy — structure, body, scripts

<!-- One level deep from SKILL.md. Description craft lives in description-craft.md. -->

## The progressive-disclosure ladder

1. **Metadata** (name + description) — always in context, every session, every skill. This is
   a standing token cost; an unused skill is a drop candidate.
2. **SKILL.md body** — enters context when the skill fires.
3. **Bundled files** — references read as needed; scripts executed (their code never enters
   context, only stdout). Effectively unbounded in size — cost is paid only on access.

## Directory shape

```
skill-name/
├── SKILL.md          # overview + workflow; a table of contents, not the depth
├── references/*.md   # depth, split by domain so unrelated domains never load
├── scripts/*         # executed, not read; deterministic work goes here
├── examples/         # exemplar inputs/outputs, skeleton files to copy
└── assets/           # templates, fonts, icons consumed by output (optional)
```

## Body rules

- **<500 lines hard ceiling; lean is the norm** — exemplary skills run well under 100 lines of
  substance and delegate depth to bundled files.
- **Concise is a principle, not a nicety**: the context window is a public good. Challenge
  every paragraph — does it justify its token cost? Never explain what a PDF is.
- **Consistent terminology** — pick one term per concept ("extract", "endpoint") and never vary.
- **Imperative voice** for instructions. Numbered steps for workflows; add a copyable checklist
  for multi-step tasks; bake in validate→fix→repeat loops (run validator, fix, only proceed clean).
- **Pitfalls and Verification are first-class sections** — what goes wrong, and what "done
  correctly" observably looks like.
- **No time-sensitive info** in the body. Park deprecated material in a collapsed
  `<details>` block if it must stay.

## Degrees of freedom

Match instruction rigidity to task fragility:

| Freedom | Form | When |
|---|---|---|
| High | prose guidance | many approaches work (code review, writing) |
| Medium | pseudocode / parameterized script | a preferred pattern exists |
| Low | exact commands, "do not modify" | fragile/sequenced ops (migrations, releases) |

Narrow bridge with guardrails vs. open field — decide which one the task is.

## References

- **Exactly one level deep from SKILL.md.** Nested refs (SKILL → advanced → details) get
  partial-read (`head -100`) and silently missed. Link every reference file directly.
- **>100 lines → table of contents at top**, so partial reads still see full scope.
- Split by domain (finance.md / sales.md), never by "advanced vs basic".

## Scripts

- **State execute-vs-read intent explicitly**: "Run `analyze.py`" (execute, token-free) vs
  "See `analyze.py` for the algorithm" (read as reference).
- **Solve, don't punt** — handle errors inside the script rather than failing back to Claude.
- **No voodoo constants** — justify every magic number in a comment.
- **Verifiable intermediates** for batch/destructive ops: plan → validate → execute
  (write changes.json, validate, then apply). Verbose validators, specific error messages.
- **No network/install assumptions**; list deps explicitly. Forward slashes in paths, always.
