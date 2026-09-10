---
description: Write a handoff baton for the next session on this topic — volatile in-session context, pointers, and open goals — to thread.<agent>.md in the current project dir.
---

# /thread

Write a baton for the next session on this topic, from the mold at
`~/workspace/.claude/templates/THREAD.tmp.md`, to `<current project dir>/thread.<agent-name>.md`
— the project or sketch directory the session has been working in, not the launch root.

## Focus
The major context from in-session that is not written down anywhere: ideas, thoughts,
half-formed concepts, and anything volatile.
*Non-volatile information goes in the project's or sub-project's `CLAUDE.md`.*

## Pointers
Files that matter on pickup, one line each on why.
*Optional.*

## To do
In-session goals only, as task lines — an outcome plus its status, checkable against the
substrate so it can retire itself.
*Goals that outlive the session go in `<current project dir>/.claude/STICKY.md`.*

## Rules
- One baton per agent per project. Overwrite an existing one rather than adding a second.
- The baton is deleted by whoever reads it. Its existence means a handoff is pending, so a
  consumed baton left behind lies. Nothing is lost — the work itself is in git.
