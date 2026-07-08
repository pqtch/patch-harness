# Claude Code — start here

## Identity
- Name: *(unfilled — run `/setup` or say "set me up")*
- Focus areas: *(unfilled)*
- Technical level: *(unfilled)*
- Tone: direct (default; tune in `.claude/rules/communication.md`)

If the fields above are still unfilled, this is a first run. Stop and read `SETUP.md`.

## Workspace map
| Path | What lives there |
|---|---|
| `.claude/rules/` | Working rules — principles, communication, conventions, security |
| `.claude/commands/` | Slash commands (`/setup`, `/wrap`, `/checkpoint`, `/health`, `/curate`) |
| `.claude/scripts/` | The only automation: a health check and an rm guard |
| `.claude/skills/` | Reusable procedures, auto-discovered |
| `.claude/agents/_meta/` | Template + guide for adding a persona agent |
| `para/projects/` | Active work — one folder per project, each with a `CONTEXT.md` |
| `para/areas/` | Ongoing responsibilities + `para/areas/ideas/` capture |
| `para/resources/icm/ICM.md` | The ICM paper — the methodology this workspace runs on |
| `para/archive/` | Closed work — archive is default, delete is never |
| `memories/shared/` | Durable facts true across the whole workspace |
| `_ops/journal/` | Dated session logs |
| `_ops/plans/` | Plan documents |

## Routing table
| If you need... | Go to... |
|---|---|
| How is this workspace supposed to work? | `docs/GUIDE.md` |
| The rules you must follow | `.claude/rules/conventions.md` |
| How to talk to this user | `.claude/rules/communication.md` |
| The relational stance | `.claude/rules/principles.md` |
| Security floor | `.claude/rules/security.md` |
| What happened last session | newest file in `_ops/journal/` |
| What a project is about | `para/projects/<name>/CONTEXT.md` |
| A durable fact | `memories/shared/MEMORY.md` (routing index) |
| To add an agent persona | `.claude/agents/_meta/NEW-AGENT.md` |

## Session startup
1. Read the health report (the SessionStart hook already printed it — don't re-run it;
   `/health` exists for mid-session re-checks). Act on any ✗.
2. Read the newest file in `_ops/journal/`.
3. Check open `para/projects/*/CONTEXT.md` files for current state and priorities.

End every session with `/wrap`: it journals what happened and persists any durable facts.
Use `/checkpoint` mid-session when context feels heavy or you're switching tasks.
