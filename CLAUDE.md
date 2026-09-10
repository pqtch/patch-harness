# WORKSPACE

The workspace (`~/workspace`) — everything reachable by walking down. One tree, one launch
point; every path in this tree is written in full from here. If you clone it somewhere else,
that name changes everywhere in one `sed` — it is a name, not a mechanism.

## Routing
| Path | Contents |
|---|---|
| `~/workspace/.claude/STICKY.md` | to-dos + one-liner ideas; *volatile* |
| `~/workspace/.claude/USER.md` | who the owner is — shared across every specialist; user-shaped knowledge routes here |
| `~/workspace/projects/` | persistent work (`~/workspace/projects/INDEX.md`) |
| `~/workspace/craft/` | on-demand personal skills — **a specialist reads `~/workspace/craft/<its-own-name>/CLAUDE.md` before starting; its skills load only once a file there is touched, and skipping it raises no error** — plus the shared skillpool (`~/workspace/craft/skillpool/INDEX.md`) |
| `~/workspace/sketch/` | pre-projects (`~/workspace/sketch/INDEX.md`) |
| `~/workspace/_ops/inbox/` | accepted-but-unfiled durable lessons; staging, never a destination |
| `~/workspace/_ops/` | bin, scripts, docs, journal, plans, archive (`~/workspace/_ops/INDEX.md`) |
| `~/workspace/.claude/agents/` | agent defs — specialists and workers |
| `~/workspace/.claude/agent-memory/` | specialist memory, one dir per specialist |
| `~/workspace/.claude-config/` | the relocated Claude Code config dir — transcripts, history, tasks. Carries continuity across machines; secrets and machine-local state are gitignored. Created by `setup.sh` <!-- may-be-absent --> |
| `~/workspace/.claude/skills/` | ROOT skills — available to every session |
| `~/workspace/.claude/templates/` | canonical formats for new files |
| `~/workspace/.claude/commands/` | slash commands |
| `~/workspace/.claude/hooks/` | hooks |

## Rules
`~/workspace/.claude/rules/workspace-rules.md` — loaded into every session; the rules live
there, not here. `~/workspace/.claude/rules/index-navigation.md` covers how to read an index.
