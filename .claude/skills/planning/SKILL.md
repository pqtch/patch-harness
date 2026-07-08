---
name: planning
description: Use when a task needs a written plan before starting — multi-step work, ambiguous scope, or anything the user should approve before execution begins.
---

# Planning

## Schema
- **Goal** — one sentence, what done looks like.
- **Ordered tasks** — the steps, in the order they'll actually happen, each concrete
  enough to verify when it's done.
- **STOP conditions** — what would make you halt and check with the user instead of
  continuing (ambiguity discovered mid-task, a destructive action needed, scope
  creeping past what was agreed).
- **Out of scope** — explicitly named, so "did you also do X" has a clear answer.

## Rule
When scope is ambiguous, choose the smaller interpretation and note the choice in the
plan rather than guessing bigger and surprising the user.
