---
name: memory-capture
description: Use when deciding whether and how to persist a fact — durable fact vs dated status, memory vs journal, which agent folder.
---

# Memory capture

## Route first
- Will this still be true in a month, independent of a date? → **memory**.
- Is it tied to "as of" a point in time, or will it be stale within a week? →
  **journal** (`_ops/journal/YYYY-MM/YYYY-MM-DD.md`), not memory.
- Is it project-specific payload (what the project is, current state)? →
  that project's `CONTEXT.md`, not memory.

## Which folder
- True for the whole workspace, not tied to one domain agent → `memories/shared/`.
- Specific to one agent's domain or a technique it's learned → that agent's own
  folder at `memories/agents/<name>/`.
- Unsure, and you're a domain agent → propose it to the user rather than writing to
  shared yourself.

## How
1. Write (or update) a detail file (shared detail files live under
   `memories/shared/memory/`; agent detail files live alongside that agent's
   `MEMORY.md` at `memories/agents/<name>/`).
2. Add or update the one-line routing entry in that folder's `MEMORY.md` — index
   only, never the fact content itself.
3. If the fact contradicts an existing entry, update or remove the stale one; don't
   leave both.
