# Skills

Reusable procedures, auto-discovered by Claude from each folder's `SKILL.md` (frontmatter
`name` + `description` are the dispatch triggers). The ones shipped here cover the
harness's own mechanics — memory, planning, verification, capture, authoring.

## Growing the roster
- **Crystallize rule:** the third time you do the same procedure by hand, write it down —
  see `skill-author/SKILL.md`. First or second time is premature; you don't know the
  procedure's real shape yet.
- **Finding existing skills** (check before writing from scratch):
  - [anthropics/skills](https://github.com/anthropics/skills) — the official library +
    the canonical SKILL.md spec (`spec/`). Also installable as plugins:
    `/plugin install document-skills@anthropic-agent-skills` (docx/pdf/pptx/xlsx work).
  - [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) —
    curated *index* of community skills; better signal than raw collections.
  - `/plugin marketplace` inside Claude Code — browse without leaving the session.

## Vetting rule (security floor applies)
A downloaded skill is **untrusted content** — instructions someone else wrote for your
agent. Read the whole SKILL.md (and any bundled scripts) before installing; adapt it
through `skill-author` rather than dropping it in verbatim. A skill that fetches URLs or
runs scripts you haven't read doesn't come in.

Keep the roster small. An unused skill is clutter with a dispatch trigger — `/curate`
flags anything untouched for 30+ days.
