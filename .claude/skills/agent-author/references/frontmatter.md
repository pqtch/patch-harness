# Frontmatter — load-bearing config, not metadata

Every field here changes runtime behavior. Three of the four have a failure mode that is silent.

## `name:` — the registry key

The **filename is cosmetic**; `name:` is what the harness registers and routes on. The real
collision is a duplicate `name:` anywhere under `.claude/agents/**`, including across
subdirectories — `workers/audit.md` and `processes/audit.md` collide even though the paths differ.

health_check guards this (`names: N agent def name(s) unique`). Verify anyway: a guard that
happens to be passing is not the same as having checked.

## `tools:` — capability ∝ trust of input

The governing rule is `.claude/rules/security.md`: capability scales *inversely* with
untrusted-input volume. Enumerate the minimal set. A lane ingesting web pages or foreign repos
gets no unbounded Bash and no unbounded egress by default.

- **Omitting `tools:` inherits EVERYTHING.** That is the single most consequential silent
  default in a def. Omission is a decision — make it deliberately or not at all. Several shipped
  worker stubs carry a commented-out `# tools: TODO`, which means they currently inherit all
  tools; a comment is not a constraint.
- **Exclusion is honored** by the harness, so the enumerated list is a real boundary.
- **Never trust an agent's self-report of its own tools.** Probe an excluded tool and confirm it
  fails (see [testing-agents.md](testing-agents.md)).
- **Scoped-over-general** (ruled early, and held): the constraint is a reviewable allowlist, not the
  absence of a tool. A capability genuinely needed gets a narrow wrapper, never a widened glob.
- **An allowlist constrains NAMES; the danger lives in CAPABILITIES.** `Bash(find:*)` reads as a
  search tool and is arbitrary command execution — `find . -exec sh -c '…'` satisfies the glob.
  Before granting `Bash(x:*)`, ask what `x` can be made to *do*, not what it is called. Note the
  converse too: argument ORDER can pin a grant safe (`Bash(git log:*)` does not admit
  `git -c alias.z='!cmd' z`, because `-c` must precede the subcommand). The prefix is part of the
  boundary — verify the actual grant string, never reason from the tool's reputation alone.

## `model:` — documented but ignored on spawns

A `model:` line in frontmatter is **not honored on Task spawns** — the spawn inherits the
parent's model. Pin the model at invocation (CLI flag or the Agent tool's `model` param).
Trusting the frontmatter line is a live source of "why is this cheap worker running on opus."

## `memory:` — omit it

**Nothing authored through this skill gets a `memory:` line, ever.** A `memory:` key is
specialist-only, and specialists are out of scope here.

**Specialists carry `memory: user`, and the reason is measured, not stylistic.** `memory:
project` resolves against the session's *live cwd at spawn time*, not the launch root
(measured 2026-09-09, Claude Code 2.1.267). A specialist spawned after the main session
`cd`s gets an empty lane, silently. `memory: user` resolves to `<config dir>/agent-memory/`
— absolute — and `setup.sh` relocates the config dir into the repo with a symlink back to
`.claude/agent-memory/`, so the lane is both cwd-proof and tracked. Full account:
`.claude/agent-memory/README.md`. The lint marks `memory: project` an error for this reason.

Gate and review instances carry **no** memory config and root at a neutral cwd — a reviewer
carrying a lane's memory is not reviewing, it is agreeing with itself.

## Diagnostic note

Empty memory injection ≠ broken bridge. Check the def's scope and the instance's cwd before
suspecting the bridge; the bridge failing is rarer than a def asking for the wrong thing.
</content>
