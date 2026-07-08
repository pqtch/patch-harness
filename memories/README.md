# Memories

Durable facts, split by scope: `shared/` (anything true across the whole workspace)
and `agents/<name>/` (facts specific to that domain agent — see
`.claude/agents/_meta/NEW-AGENT.md`).

## Protocol
- **Read** shared + your own folder if you're a domain agent. Don't read another
  agent's folder — it's not yours to reason from.
- **Write** only your own folder (or `shared/` if you're the default Claude agent
  acting on the user's behalf, not a domain agent).
- `MEMORY.md` in each folder is a **routing index** — one line per fact, pointing to a
  detail file. Never write fact content directly into `MEMORY.md`.
- **Persist before finishing** — if something durable came up this session, write it
  before `/wrap` ends, don't rely on remembering to later.
- `scratch.md` (agent folders only) is working memory for the current thread of work —
  wipe it at `/wrap`, don't let it accumulate.

See `.claude/rules/conventions.md` for the memory-vs-journal routing rule (durable →
memory, dated/status → journal).
