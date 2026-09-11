# patch-harness

A workspace boilerplate for Claude Code, extracted from one that has been in daily use since
early 2026. It is the **mechanism** of that workspace with none of its content: the tree, the
rules, the hooks, the agent definitions, the memory system, the templates, the checks — and the
measured reasons each one is shaped the way it is.

It is meant to be **used**, not admired. Clone it, run one script, restart, log in. `SETUP.md`
is the whole of that. This file is the architecture.

Five words this tree uses as terms of art, so they are not a surprise below: a **lane** is one
specialist's memory directory; a **mold** is a template that is exactly the file it produces;
a **thread** is a one-shot file left in a project directory for the next session on that
topic and deleted when it is picked up; **on touch** means "when a file in that directory is opened with the Read or Edit **tool**"
— the moment Claude Code loads that directory's `CLAUDE.md` and skills. Bash `cat` does not
count, measured; `docs/GUIDE.md`; a **rung** is one level of the
guard ladder, explained under Architecture.

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
├── CLAUDE.md                  the routing table; with the rules, the only thing loaded at every boot
├── .claude/
│   ├── rules/                 workspace-rules + index-navigation every session; memory-rules on touching a lane
│   ├── agents/                three specialists (named by themselves) + four workers
│   ├── agent-memory/<name>/   one flat lane per specialist; MEMORY.md is the resident index
│   ├── skills/                root skills — only what would make output WRONG if absent
│   ├── commands/              /wrap and /thread — the session lifecycle
│   ├── hooks/                 the three guards and the two boot hooks, registered in settings.json
│   ├── templates/             eleven molds; a mold is exactly the file it produces
│   ├── STICKY.md · USER.md    volatile to-dos; who the owner is
│   └── settings.json          env, permissions, hooks — every entry carries a _note
├── .claude-config/            the Claude Code config dir, relocated here by setup.sh so continuity is in git
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
| hook | a Bash `sed -i` on a `p.*` file · a commit staging a gitlink · a thread picked up exactly once | `.claude/hooks/` |
| check | dead pointers · `type:` outside its vocabulary · private content in a public repo (`check-leak`, shipped but not installed until you have a public repo) | `_ops/bin/check-*` |
| rule | eight rules, one screen | `.claude/rules/` |
| memory | what binds one specialist and nobody else | `.claude/agent-memory/` |

### Specialists and workers
A **specialist** is named, persists, and owns a memory lane. A **worker** is spawned, does one
job, and is discarded. Three specialists ship — `center`, `researcher`, `analyst` — and they
ship **unnamed on purpose**: a name is not configuration, and each def says so in its own
voice. Four workers ship with their `tools:` restricted to the job, because that restriction is
real capability shaping and a persona is not. (A session's roster also shows Claude Code's
own built-in agent types; those are the harness's, not this tree's.) `~/workspace/.claude/agents/README.md`.

### Memory
Two sides. **Subjective** memory is the specialist's, written in session with the context.
**Objective** memory is written by a process with only the record — `check-digest`, from the
transcript and the session's commits — and it never lands in a lane: a journal section, a
six-line brief of the last session injected at the next boot, and proposals with their
evidence quoted, which the specialist files or drops. That split is what keeps lanes small.

Four types on the subjective side, a closed vocabulary — `identity` · `feedback` · `project` · `reference` — one per
file, checked by `check-types`. The index is resident; everything else loads when a trigger in
the index reaches for it, which is how depth is controlled without a rule. A lane's path comes
from the def's `memory: user` line, which Claude Code resolves to `<config dir>/agent-memory/<name>/`;
`setup.sh` moves the config dir into the repo so that path is tracked. The other setting,
`memory: project`, was measured to hand a specialist an empty lane whenever the session had
changed directory before spawning it (`docs/incidents.md` #5). `~/workspace/.claude/rules/memory-rules.md` and
`~/workspace/.claude/agent-memory/README.md`.

### Loading
Agents are frozen at session start; skills load lazily on touch and never unload; commands
cost nothing until invoked; a gitignored directory is invisible to discovery. Each of those
sentences was measured on a dated Claude Code version — the dates, versions and token costs
are in `docs/GUIDE.md` and `docs/evidence.md`.

## Reading order
1. `SETUP.md` — get it running.
2. `docs/GUIDE.md` — how the parts fit, and the session lifecycle.
3. `docs/harness-hooks.md` — before writing a hook.
4. `docs/evidence.md` — the numbers behind the shape.
5. `docs/incidents.md` — the scars, and what each one bought.
6. `docs/lineage.md` — where this came from and what stayed behind.

## License
MIT — `LICENSE`.
