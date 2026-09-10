# The description is the routing truth

Write it BEFORE the body. The body never enters context until the agent spawns — the
`description:` is the *only* thing the center and the harness see when deciding where work lands. A
perfect body behind a vague description is an agent that never gets called, or gets called for
the wrong thing.

## What it must answer

**When should work land here, and NOT on a sibling?**

Both halves are required. Most weak descriptions state the positive case well and omit the
negative entirely, which is what produces overlap — and overlap is a *registry* bug, not a
wording preference. Two descriptions claiming one lane means the router picks by accident.

## Shape

1. **Kind prefix.** Workers open literally with `Pure worker:`. Process defs open with the process
   contract. A specialist-private subagent names the specialist it extends.
2. **The positive case** — concrete triggers, in the vocabulary someone would actually use when
   the need arises, not internal jargon.
3. **The negative case** — what does *not* land here, naming the sibling that owns it instead.
   Naming the sibling is what makes the boundary enforceable.
4. **Third person, present tense.** "Resolves markdown links…", never "I can help you check…".

## Worked contrast

**Weak:** `Pure worker: checks links.`
Nothing about scope, no negative case, collides with anything that touches a file.

**Strong:** `Pure worker: resolves relative markdown links across a given file set and reports
which targets do not exist… Not for editing the files it audits, not for checking live URLs
(collector), and not for judging whether the prose is any good (a writing specialist).`

Three named exclusions, each pointing at the def that owns that work. See
[../examples/pure-worker.md](../examples/pure-worker.md).

## Overlap check — the whole registry, not the folder

Check the new description against **every** def under `.claude/agents/**`, including specialists,
scheduled processes, and other subdirectories. Overlap does not respect folders. The most common
misroute is a new worker quietly shadowing a specialist's lane, because the author compared it only
against the other workers.

When you find overlap, the fix is usually to **sharpen the existing def**, not to differentiate
the new one — the older description was probably over-broad, and forking around it leaves the
ambiguity in place for the next author.
</content>
