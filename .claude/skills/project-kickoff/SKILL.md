---
name: project-kickoff
description: Use when starting a new project — creating its CONTEXT.md, wiring it into CLAUDE.md, and giving it a first journal mention.
---

# Project kickoff

1. Interview briefly: what the project is, why it exists, what's already known about
   current state, and any pointers (repo, docs, tracker) worth recording now. Don't
   invent details — leave a fillable placeholder for anything unclear.
2. Copy `para/projects/_template/CONTEXT.md` to `para/projects/<kebab-case-name>/CONTEXT.md`
   and fill it: What it is, Current state, Pointers.
3. Add a row to `CLAUDE.md`'s routing table pointing at the new CONTEXT.md.
4. Note the kickoff in today's `_ops/journal/YYYY-MM/YYYY-MM-DD.md`.
