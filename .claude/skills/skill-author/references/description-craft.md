# Description craft — the dispatch surface

<!-- One level deep from SKILL.md. Everything here is about the frontmatter description;
     body craft lives in anatomy.md. -->

## Why this file exists

Claude preloads ONLY `name` + `description` of every installed skill into the system prompt.
The body cannot help Claude decide to fire the skill — it hasn't been read yet. Practitioners
report ~70% of skill iteration time goes to the description. When a skill misbehaves, suspect
the description first, always.

## The four components

Every strong description carries:

1. **Verb** — what it does (reviews / extracts / generates / audits). Third person.
2. **Object** — what it operates on (pull requests, PDF forms, SKILL.md files).
3. **Scope** — where/when it applies (staging vs prod, which repo, which file types).
4. **Differentiator** — why this and not its sibling ("security-focused, not style-focused").

Formula:

```
[Verb] [object] for [goal]. Use when [triggers]. Do not use for [neighbors].
```

## Hard rules

| Field | Rule |
|---|---|
| name | ≤64 chars; lowercase/numbers/hyphens; no XML; no "anthropic"/"claude"; never vague (`helper`, `utils`, `tools`, `data`) |
| description | non-empty; ≤1024 chars; no XML tags; third person ALWAYS |

POV drift kills dispatch: "I can help you…" / "You can use this…" degrade matching. Write
"Extracts text from…".

## Pushy + fenced (the house rule)

Claude measurably under-triggers skills, so write descriptions pushy: enumerate triggers
explicitly — "use when the user mentions X, Y, or Z, even if they don't explicitly ask."

**But in this workspace the exclusion clause is mandatory, not advice.** Seven specialists carry
sibling pools; pushy descriptions without "do not use for…" compound into dispatch-stealing.
The lint warns when either clause is missing.

## Good / bad

```yaml
# good — verbs, objects, triggers, file types
description: Extracts text and tables from PDF files, fills forms, merges documents. Use
  when working with PDF files or when the user mentions PDFs, forms, or document extraction.
  Do not use for OCR of scanned images (see ocr-and-documents).

# good — scope + differentiator carry the weight
description: Audits frontend designs against the anti-slop doctrine — spacing, hierarchy,
  motion. Use when reviewing or critiquing a UI, page, or component. Do not use for
  building new UI from scratch (see design-taste-frontend).

# bad — never fires
description: Helps with documents
description: Processes data
description: A useful skill for design work
```

## Trigger-term packing

Name the things a user would actually type: file extensions (".xlsx", ".excalidraw"),
tool names ("playwright", "manim"), task words ("flashcards", "commit message"), context
words ("staging", "fMRI"). The match is semantic but concrete anchors dominate.
