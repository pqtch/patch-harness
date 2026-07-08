# patch-harness

A starter kit for running Claude Code (or any coding agent) against a personal or work
repo without losing context between sessions, and without re-explaining yourself every time.

## Philosophy

The folder structure IS the memory. Facts live in exactly one file. Status and history
live in a dated journal, not in files the agent loads every session. The agent onboards
itself — you don't need to read the internals before it's useful to you. Verify before
claiming done; honesty over comfort; memory is maintained with care, not left to rot.
Fewer words, everywhere, is a feature.

## Quickstart

1. Create a folder, named whatever you want. This becomes your workspace.
2. Open Claude Code in that folder.
3. Paste: **"Clone `https://github.com/pqtch/patch-harness` into this folder and follow its SETUP.md."** Claude
   clones the template, then interviews you (name, what you're using this for, tone
   preference) and personalizes `CLAUDE.md` and your first project.
4. Continue setup from there — Claude drives; it ends by telling you to restart
   Claude Code so everything loads natively.
5. Work normally. At the end of a session, run `/wrap` — Claude journals what happened and
   what's next, so the following session picks up cold with full context.

Prerequisites: `git` and `python3` on your PATH (Claude checks during setup and says so
if either is missing — the workspace still works, minus the automated checks).

## What's in here

| Path | Job |
|---|---|
| `CLAUDE.md` | Entry point — routing table + session startup |
| `docs/GUIDE.md` | The full reference — how every part works, decision trees |
| `.claude/rules/` | The working rules every agent obeys |
| `.claude/scripts/` | A health check and an rm guard — the only automation |
| `.claude/skills/` | Reusable procedures, auto-discovered |
| `.claude/agents/` | Domain-specialist subagents |
| `para/` | Where work actually lives — `projects/`, `areas/`, `resources/`, `archive/` |
| `memories/` | Durable facts, shared + per-agent |
| `_ops/journal/`, `_ops/plans/` | Session history and plan documents |

MIT licensed. Fork it, personalize it, keep it small.
