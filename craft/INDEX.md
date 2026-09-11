# craft/ — specialist skills

One directory per specialist. A specialist's skills live at `craft/<name>/.claude/skills/`
and are **discovered by walking** — they attach the first time a file under that directory is
opened with the **Read or Edit tool**, which is why every specialist def instructs it to read
`craft/<name>/CLAUDE.md` before beginning. Skip that and the specialist silently has no skills.

**Bash does not count.** MEASURED 2026-09-11, Claude Code 2.1.268: `cat craft/<name>/CLAUDE.md`
attaches nothing; the Read tool on the same file attaches the pool. A bash-first session that
follows the instruction with `cat` has followed it and gained nothing, with no error either
way. `~/workspace/docs/GUIDE.md`, "Skills".

## Scope
| scope | lives at | who gets it |
|---|---|---|
| global | `~/workspace/.claude/skills/` | every agent, every session |
| **specialist** | `~/workspace/craft/<name>/.claude/skills/` | that specialist, on walking in |
| project | `<project>/.claude/skills/` | anyone working that repo |

**Depth rule.** A shallow version of a capability is global; the deep version is a
specialist's. Every session may need a web search; only the researcher runs a sourced
investigation with a trust gate.

## Index
| Path | Contents |
|---|---|
| `~/workspace/craft/center/` | empty |
| `~/workspace/craft/researcher/` | source-verification |
| `~/workspace/craft/analyst/` | empty |
| `~/workspace/craft/skillpool/` | staging |
