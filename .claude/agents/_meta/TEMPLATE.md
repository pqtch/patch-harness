---
name: agent-name
description: One line — what this agent is for and when to invoke it. This is a dispatch trigger, not a bio.
tools: Read, Write, Edit, Grep, Glob
---
<!-- Write/Edit are for the agent's OWN memory folder (see Write rule). Add Bash or web
     tools only if the domain needs them — a web-facing agent doesn't get Bash. -->

# Persona

Two or three sentences: what this agent's domain is, what perspective it brings, what
it explicitly does not do.

## Memory

Reads `memories/shared/MEMORY.md` (and shared detail files) plus its own folder at
`memories/agents/<agent-name>/`. Never reads another agent's folder.

## Write rule

Writes only to its own folder: `memories/agents/<agent-name>/MEMORY.md`, `craft.md`,
`scratch.md`. Never writes to `memories/shared/` or another agent's folder. If a fact
belongs in shared memory, propose it to the user instead of writing it directly.
