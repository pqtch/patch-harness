---
description: Mid-session state save — append a timestamped checkpoint to today's journal before compaction, a task switch, or when context feels heavy
---

Append a timestamped block to today's `_ops/journal/YYYY-MM/YYYY-MM-DD.md`: what's done,
what's in flight, next step. Lighter than `/wrap` — no memory persistence, no scratch
cleanup, no CONTEXT.md updates. Confirm to the user in one line where it landed.
