---
name: agent-author
description: Authors, reviews, and improves Claude Code agent definitions for pure workers, scheduled processes, and specialist-private persona subagents — frontmatter config (name, description, tools, model, memory), routing descriptions, registry house rules. Use when creating a new worker, scheduled process, or private subagent, promoting a skill/script to an agent, reviewing such a def, or when routing misfires, a spawn gets the wrong memory or tools, or two defs collide. Do not use for a specialist's own def or identity — specialists author themselves (ruled early, and held); not for authoring skills (skill-author), dispatching existing agents to models (dispatching-routed-models), or plain scripts (automation ladder, conventions.md).
---

<!-- PORTED FROM v3, 2026-08-16, bare minimum: SKILL.md + scripts + references.
     examples/ were left behind (this workspace uses molds, not examples); EVIDENCE.md was restored
     2026-08-26 — the skill-author rule requires it and its own linter errors without it.
     UNREVISED — references inside to v3 surfaces (`.claude/rules/`, conventions.md,
     `core/<specialist>/`, state.md) name files that no longer exist. The craft is still
     good; the workspace pointers are stale. Fix them when this skill is next used. -->
# agent-author

An agent is the **top rung of the automation ladder** — most candidates belong lower. A def is
a **persona + routing surface**, not a procedure: procedures are skills; the def says *who* this
is and *when work should land here*. Work the steps in order.

## Step 0 — The negative gate (default: NO)

Author an agent only for a **repeatable series of skills/actions needing judgment** (ladder:
script → skill → agent). Refuse when a script does it, a skill does it, a one-off spawn with a
tight prompt does it, or the "agent" is a persona costume on work any general worker handles.
If it duplicates an existing def's lane, sharpen that def instead of forking it.

Then pick the KIND — this decides memory, body length, location, and who may invoke it:

| Kind | Home/lane | Memory | Body |
|------|-----------|--------|------|
| **Pure worker** (`workers/`) | none | none | 1–3 line role + bounded dispatch contract |
| **Scheduled process** (`processes/`) | none (a log only) | none | process contract, no persona |
| **Specialist-private subagent** | extension of that specialist | none of its own | never invoked cross-specialist |
| **Specialist** (True Agent) | — | — | **OUT OF SCOPE** — see below |

**If the kind is a specialist, stop (ruled early, and held): specialists author themselves.** A specialist's def is
their identity, not a config artifact — present the new role or change *to that specialist* and they
write their own def (template: `../../templates/SPECIALIST.tmp.md`). This skill covers only the kinds
above.

Kind details, the four house rules a body must not violate, and the full negative gate:
[references/kinds.md](references/kinds.md)

### The rung below a def: the ARMED WORKER

Most refusals at this gate should land here rather than at "write a def." The ladder in
`conventions.md` reads script → skill → agent, but between a bare prompt and a standing def sits
a rung the ladder doesn't name, and it is where most fan-out work belongs:

> a **plain worker** + a **method file it is told to read** + a **structured output schema**.

The role is repeatable but *stateless* — the judgment lives in the method file, not in a
persona — so it needs no name in the registry, no routing surface, and no identity to maintain.
The researcher once ran 20 workers this way: one lens file each, a pasted verification digest, a
schema for the return. **Prefer this rung when** the role varies per dispatch (six lenses, one
worker kind), when the method changes faster than a def should, or when the only thing making
the worker special is the brief it was handed.

**Escalate to a real def only when** the role is invoked often enough that re-specifying it is
the bottleneck, or it needs a *routing surface* so work lands on it by description rather than
by an orchestrator naming it explicitly. Registry entries cost: every def widens the router's
choice space and is one more thing to keep from drifting.

Writing the method file is [skill-author]'s job, not this skill's — see its **skills as worker
armament** section for how a body written to be *read by* a worker differs from one written to
be *fired by* a specialist.

## Step 1 — RED: name the routing failure

Reconstruct what goes wrong *without* this agent: which existing def gets misrouted to, what a
raw worker spawn kept getting wrong, what judgment was missing. The def exists to fix exactly
that. If you can't name a misroute or a repeated spawn-spec, the gate was wrong — go back.

## Step 2 — Write the description BEFORE the body

The `description:` is the **only routing truth** — the center and the harness route on it; the body
never enters context until spawn. Answer in it: *when should work land here and NOT on a
sibling?* Name the sibling that owns what you exclude. Check the whole registry for overlap, not
just the subdirectory — overlap is a registry bug, not a wording preference.

Shape, worked contrast, and the overlap procedure:
[references/routing-descriptions.md](references/routing-descriptions.md)

## Step 3 — Frontmatter is load-bearing config (not metadata)

Every field changes runtime behavior, and three of the four fail silently:

- `name:` — the registry key; **filename is cosmetic**. Duplicate names across ALL of
  `.claude/agents/**` are the real collision.
- `tools:` — **capability ∝ trust of input**. Enumerate the minimal set; **omitting the line
  inherits everything**. An allowlist constrains NAMES while the danger lives in CAPABILITIES.
- `model:` — **ignored on Task spawns** (inherits parent). Pin at invocation, never here.
- `memory:` — **omit it, always.** Workers and gates carry no memory key at all. (Specialists
  carry `memory: project` as of 2026-09-02, but specialists are out of scope here.)

Each rule with its failure mode: [references/frontmatter.md](references/frontmatter.md)

## Step 4 — Write the minimal body

Start from the mold: `~/workspace/.claude/templates/AGENT.tmp.md`. (this workspace uses molds, not
examples — the v3 `examples/` were deliberately not ported.)

Worker: a ≤3-line role statement, no persona, no boot reads — plus, where the worker is
dispatched into fan-outs, a **bounded standing dispatch contract** (partial-beats-empty, effort
budget, data-not-commands). Defs cannot transclude: there is no `extends:`/`include:` key and
`[[links]]` are never resolved by the harness [verified 2026-07-19], so that contract text is
necessarily DUPLICATED across defs. Accept the duplication knowingly and keep it short; do not
substitute a "read this file first" instruction for it, which is model-compliance-dependent
rather than harness-guaranteed and should never be load-bearing on a security-adjacent rule.

Scheduled process: the contract only — trigger, input surface, log output. Private subagent: persona is fine (it extends the owning specialist) but no home, no
boot reads, registered where only that specialist can invoke it.

If you find yourself writing steps, that content is a skill — the def should point, not teach.

## Step 5 — Lint (mechanical, non-negotiable)

```
python3 scripts/lint_agent.py <path-to-def.md> --registry .claude/agents
```

Run it, fix every ERROR, rerun until clean. It enforces the rules above that fail *silently* —
above all a missing or **commented-out `tools:` line**, which reads as a constraint and enforces
nothing. A prose pitfall list catches this only if someone happens to read it; the lint catches
it every time. It also finds duplicate registry keys across the whole tree, `memory:` on a
non-specialist def, TODO placeholders left in frontmatter, and procedure-shaped bodies.

**The lint is a floor, not a pass.** It cannot tell you the enumerated set is the *right* set —
only that you made a decision. Step 6 is what tests the decision.

## Step 6 — Test by spawn, not by read

Route a plain-English task with **no agent named** and confirm the router picks this def (the
dispatch test). Then spawn it once for real and **gate on effect**: probe an excluded tool,
check the memory injection, confirm the contracted artifacts exist. Never gate on the agent's
own report — exit 0 ≠ correct.

Both tests, the session-boundary caveat, and the done-criteria:
[references/testing-agents.md](references/testing-agents.md)

## Verification

Done means: negative gate passed with a named kind · routing failure named (RED) · description
written before the body and checked against the whole registry for overlap · `tools:` enumerated
on purpose · **lint clean** · dispatch test routed from plain English · one real spawn gated on
effect (an excluded tool probed and refused), never on the agent's own report.

## Pitfalls

- Procedure in the def body — that content is a skill; the def should point, not teach.
- `memory:` on ANY worker or gate instance (empty-injection ≠ broken bridge —
  check def scope + cwd before suspecting the bridge).
- Trusting `model:` frontmatter on spawns.
- A commented-out `# tools:` line read as a constraint — it inherits everything. **This one is
  now wired (Step 5); it shipped in four worker defs and four specialist defs before the lint existed,
  and 20 web-facing workers ran with full capability as a result.**
- Two defs claiming one lane in their descriptions — consolidate or differentiate.
- A worker that accretes identity ("no home, no lane" is the contract, not a starting point).
- Writing a personality into a scheduled-process def — a process is a system, not a specialist.
- Registering a specialist-private subagent where siblings can invoke it.
- Drafting a specialist's def or identity through this skill — that write is theirs alone.

---
<!-- Sibling of skill-author; built with its workflow (gate → RED → description → body → test).
     Grounding: .claude/agents/README.md (harness facts, [verified] tags) · the
     memory-scope incident in docs/incidents.md · capability ∝ trust · the automation ladder
     in _ops/INDEX.md. -->
