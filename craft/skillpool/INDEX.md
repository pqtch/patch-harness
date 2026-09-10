# craft/skillpool/ — staging

Skills that are built but not yet assigned to a specialist, or that more than one specialist
wants. A skill sitting here is **not loaded by anyone** — nothing walks in here on its own.
It is a holding pen, not a scope.

## Index
*(empty)*

A skill with an obvious owner goes to `craft/<name>/.claude/skills/` directly and never
passes through here. **If this stays empty, cut it.** A staging area nothing moves through is
a routing failure, the same shape as `_ops/inbox/`.
