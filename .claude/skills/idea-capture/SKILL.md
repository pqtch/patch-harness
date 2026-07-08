---
name: idea-capture
description: Use when the user floats a loose thought that isn't a task yet — capture it into para/areas/ideas/ instead of losing it or prematurely making it a project.
---

# Idea capture

## Tiers (see `para/areas/ideas/README.md`)
- **seed** — a one-line thought, not yet worth more.
- **scaffold** — a seed someone came back to: rough shape, open questions listed.
- **ready** — scaffolded enough to become a project.

## Steps
1. Add the thought as a flat line under the right tier heading in
   `para/areas/ideas/README.md` (or a dedicated ideas file if the README is getting
   long). Don't create a project folder yet.
2. On a return visit, if the idea has grown, move it up a tier in place — don't
   duplicate the line.
3. Only at **ready** do you promote it: run `project-kickoff` to create the
   `para/projects/<name>/CONTEXT.md`, then remove the idea's line from here.
