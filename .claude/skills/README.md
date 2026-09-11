# .claude/skills/ — ROOT skills

| Skill | Job |
|---|---|
| `agent-author/` | author, review and lint agent defs — workers, scheduled processes, private personas. Never a specialist's own def. |
| `skill-author/` | author, review and improve skills — structure, frontmatter, dispatch craft |
| `action-first/` | an output discipline: lead with the next action, number steps, restate state, never size work in time. **User-only** — invoke with `/action-first` |

Mold for a new one: `~/workspace/.claude/templates/SKILL.tmp.md`.

## The root-skills rule
> A skill lives at root only if its absence would make output **WRONG** rather than merely
> **WORSE**. Everything else nests.

Root skills are not lazy: they load at session start and are paid again by every subagent
spawned. Nested skills (in `projects/*/`, `sketch/*/`, `craft/*/`) are the lazy ones — and
lazy means **on a Read/Edit tool call**, not on a Bash `cat` (measured 2026-09-11; `GUIDE.md`). The
test above is checkable, which is the point — "it's useful everywhere" is not the test;
useful-everywhere is what the nested copy is for.

`action-first` is the deliberate exception: its body is cheap, and the shape it enforces is
the difference between output the reader acts on and output the reader reads. It carries
`disable-model-invocation: true` — an output MODE is turned on by the reader, never picked by
the model on the reader's behalf — which is also what exempts it from the three dispatch rules
in `skill-author/scripts/lint_skill.py`. That flag is a declaration, not a gate: measured
2026-09-11, Claude Code 2.1.268, the model can still invoke a skill carrying it (`GUIDE.md`).

Residency, budgets, frontmatter keys, and how discovery actually works:
`~/workspace/docs/GUIDE.md`.
