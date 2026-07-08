---
description: End-of-session close — journal what happened, persist durable facts, clear scratch state
---

1. Write (or append to) today's `_ops/journal/YYYY-MM/YYYY-MM-DD.md`: what happened this
   session, decisions made, what the next session should pick up.
2. Check whether anything discussed this session is a durable fact (see
   `.claude/rules/conventions.md` memory discipline). If so, add it to the right
   memory folder per `memories/README.md` — routing index entry plus detail file.
3. Update any `para/projects/*/CONTEXT.md` whose state changed.
4. Wipe per-agent `scratch.md` files (scratch is working memory for the session; anything
   worth keeping should have been routed to a journal/memory/CONTEXT in steps 1-3).
5. Commit: `git add -A && git commit -m "wrap: YYYY-MM-DD <one-line summary>"`. Every wrap
   commits — the git history is the user's undo button and their sync point across machines.
6. Confirm to the user in one line what was journaled, persisted, and committed.
