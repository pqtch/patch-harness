---
name: project-author
description: Creates a new project folder under `~/workspace/projects/` to the shape this workspace expects — `CLAUDE.md` routing brief, `.claude/STICKY.md`, an `INDEX.md` row — and, for an external repo, the shell-plus-clone layout with its `.gitignore` line written BEFORE the clone. Use when starting a new piece of persistent work, cloning an existing repo into this workspace, promoting a sketch to a project, or when a project folder is missing its brief or its ignore line. Do not use for a throwaway investigation — that is a `sketch/` directory, which needs no scaffolding — or for authoring skills or agent defs (skill-author, agent-author).
---
# project-author
Use this skill to create a new project under `~/workspace/projects/`.
Templates live beside this skill at `templates/` (symlinks to `~/workspace/.claude/templates/`).

## General Project Structure
```
~/workspace/projects/<project-name>/
|_ CLAUDE.md          <— Canonical project state + routing table *required*
|_ .claude/
|   |_ STICKY.md      <— Project to-dos + one-liner ideas *required*
|   |_ agents/        <— Project specific agents *optional*
|   |_ skills/        <— Project specific skills *optional*
|   |_ templates/     <— Project specific file templates *optional*
|   |_ rules/         <— Project rules *optional*
|_ <sub-project>/     <— Sub-project dir *optional*
    |_ CLAUDE.md      <— Canonical sub-project state + routing table *required*
    |_ <working-dirs>/  <— Content dirs for sub-project *optional*
    |_ docs/
        |_ refs/      <— Project reference docs *optional*
        |_ archive/   <— Project archive *optional*
```

## Which templates to use
| Template | Purpose |
|---|---|
| `templates/CLAUDE.tmp.md` | Canonical project state + routing table |
| `templates/STICKY.tmp.md` | Project to-dos + one-liner ideas |

## Also
- A project with its OWN `.git` gets ONE wholesale ignore line in the root `.gitignore`
  (`projects/<name>/<name>-repo/`), written BEFORE the clone. Reasoning is inline there.
  The negation pair (`<repo>/*` + `!<repo>/.claude/`) does not work: it leaves the directory visible to git, which
  is how `git add -A` turned a clone into a gitlink.
- **The clone's own `.claude/` will not load** — a gitignored directory is invisible to skill
  discovery. The two `.claude/` directories have two owners. The **shell's**
  is this workspace's — our skills, agents and settings for working this repo, and it loads. The
  **clone's** holds only what is true for that repo regardless of this workspace, aimed at whoever
  clones it. If something in the clone's is worth having on our side, COPY it up into the
  shell; copy, not move, so the repo keeps its own and the two may diverge.
- `.claude/agents/` inside a project does NOT load: the agent namespace is frozen at session
  start. For agent-shaped capability that arrives lazily, use a skill with `context: fork`.
