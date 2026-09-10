# patch-harness

A workspace boilerplate for Claude Code, extracted from one that has been in daily use since
early 2026. It is the **mechanism** of that workspace with none of its content: the tree, the
rules, the hooks, the agent definitions, the memory system, the templates, the checks — and the
measured reasons each one is shaped the way it is.

It is meant to be **used**, not admired. Clone it, run one script, launch. `SETUP.md` is the
whole of that. This file is the architecture.

## The idea in one paragraph

A coding agent forgets everything between sessions, loads whatever it is pointed at, and
believes what it reads. Every part of this tree answers one of those three. **Forgetting:**
the folder structure is the memory — facts live in exactly one file, indices point rather
than answer, and a named specialist keeps a typed memory lane that survives sessions.
**Loading:** the root routing file is short and every directory below it carries its own
`CLAUDE.md` that loads only on touch, so context is paid for as it is walked into. **Belief:**
constraints are enforced at the highest rung that can reach them — a permission over a hook,
a hook over a rule, a rule over a memory — and every guard is written after the failure it
refuses actually happened, with its blind spot named in its header.

## Architecture

```
~/workspace/
├── CLAUDE.md                  the routing table; the only thing resident at boot besides the rules
├── .claude/
│   ├── rules/                 loaded every session: workspace-rules, index-navigation, memory-rules
│   ├── agents/                three specialists (named by themselves) + four workers
│   ├── agent-memory/<name>/   one flat lane per specialist; MEMORY.md is the resident index
│   ├── skills/                root skills — only what would make output WRONG if absent
│   ├── commands/              /wrap and /thread — the session lifecycle
│   ├── hooks/                 the two guards and the baton hook, registered in settings.json
│   ├── templates/             twelve molds; a mold is exactly the file it produces
│   ├── STICKY.md · USER.md    volatile to-dos; who the owner is
│   └── settings.json          env, permissions, hooks — every entry carries a _note
├── .claude-config/            the relocated Claude Code config dir, so continuity is in git
├── projects/  sketch/  craft/ the work, the pre-work, and each specialist's own skills
├── _ops/                      bin (launcher, setup, checks) · journal · plans · inbox · archive
└── docs/                      this boilerplate's own docs — GUIDE, hooks, evidence, incidents, lineage
```

### The guard ladder
`~/workspace/.claude/rules/workspace-rules.md`, rule 6: **permission > hook > rule > memory.**
A constraint is enforced at the highest rung it can actually reach. A constraint living below
the rung it could occupy is a bug, because every rung down trades enforcement for a reader who
might not read. What ships at each rung:

| Rung | What | Where |
|---|---|---|
| permission | `p.*` files are read-only to every editing tool | `settings.json` |
| hook | a Bash `sed -i` on a `p.*` file · a commit staging a gitlink · a baton delivered exactly once | `.claude/hooks/` |
| check | dead pointers · `type:` outside its vocabulary · private content in a public repo | `_ops/bin/check-*` |
| rule | eight rules, one screen | `.claude/rules/` |
| memory | what binds one specialist and nobody else | `.claude/agent-memory/` |

### Specialists and workers
A **specialist** is named, persists, and owns a memory lane. A **worker** is spawned, does one
job, and is discarded. Three specialists ship — `center`, `researcher`, `analyst` — and they
ship **unnamed on purpose**: a name is not configuration, and each def says so in its own
voice. Four workers ship with their `tools:` restricted to the job, because that restriction is
real capability shaping and a persona is not. `~/workspace/.claude/agents/README.md`.

### Memory
Four types, a closed vocabulary — `identity` · `feedback` · `project` · `reference` — one per
file, checked by `check-types`. The index is resident; everything else loads when a trigger in
the index reaches for it, which is how depth is controlled without a rule. Lanes resolve
through `memory: user` into a config dir that `setup.sh` relocates into the repo: the
measured alternative hands a specialist an empty lane when the session has changed
directory. `~/workspace/.claude/rules/memory-rules.md` and
`~/workspace/.claude/agent-memory/README.md`.

### Loading
Agents are frozen at session start; skills discover lazily on touch and never unload;
commands cost nothing until invoked; a gitignored directory is invisible to discovery. Each of
those sentences is a measurement with a date, and the costs are in `docs/GUIDE.md`.

## Reading order
1. `SETUP.md` — get it running.
2. `docs/GUIDE.md` — how the parts fit, and the session lifecycle.
3. `docs/harness-hooks.md` — before writing a hook.
4. `docs/evidence.md` — the numbers behind the shape.
5. `docs/incidents.md` — the scars, and what each one bought.
6. `docs/lineage.md` — where this came from and what stayed behind.

## License
MIT — `LICENSE`.
