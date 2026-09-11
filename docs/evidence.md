# Evidence — the numbers behind the shape

Measured on the private tree this boilerplate was extracted from, 2026-08-22 unless noted,
on Claude Code 2.1.2xx. Each number is given with what it argued for. None of them is a
benchmark; they are the readings that decided the shape, and they carry their own caveats.

| Measurement | Reading | What it decided |
|---|---|---|
| **Resident set at boot** — root `CLAUDE.md` + the three rules files | **1,002 tokens** | The root routing file stays a table; explanation moved to docs read on purpose. Every line at boot is paid by every session and every subagent |
| **Per-turn injection** — re-injecting the same guidance each turn vs stating it once | loses its effect after **~5 turns** | Rules are stated once, at boot; the durable form of a constraint is a hook or a check, not repetition |
| **Session length**, in user turns | median **1** · mean **4.4** · p90 **14** | Most sessions are one question. A boot cost is paid ~once per question, so it must be small; a pickup mechanism (the thread) matters more than in-session memory |
| **Dead pointers**, raw — every `~/<root>/…` path in prose that did not resolve | **2,893** | Alarming, and wrong: most were quotes of history |
| **Dead pointers**, once sorted by whether the file makes a *live claim* | **11** | `check-pointers` skips archives, journals, fenced code, and files declaring `pointers: mixed`. A check that counts history as failure trains its reader to ignore it |
| **Asserted paths in transcripts** — paths an agent stated as fact across 122 sessions | **329**, of which **128 unresolved** | Agents assert paths from memory. The pointer check exists because a stated path is a claim, and 39% of them were false |
| **Frontmatter** — files carrying any at all / carrying a typed `type:` | **34% / 5%** | Frontmatter was never a convention, it was decoration — except in two places where something *read* the value. Those two are the closed vocabularies `check-types` enforces; everything else is free text on purpose |
| **The rules sort** — 38 rules in the old rules file, sorted by what could enforce each | **1 hook · 7 rules · 19 checks · 4 queue · 7 dropped** | The guard ladder. 19 of 38 "rules" were things a script could check; 7 were unenforceable and cut. **Caveat, the author's own:** this is *avoided* cost, not recovered — nothing measures what those rules were costing before |

## Later measurements that changed the shape
| Date · version | Measurement | Consequence |
|---|---|---|
| 2026-08-02 · 2.1.220 | Agent namespace frozen at session start; skills discover lazily and never unload; a gitignored directory is invisible to discovery | `GUIDE.md`, "What loads, when" |
| 2026-08-16 · 2.1.233 | `SessionStart` receives `agent_type` on stdin (harness-set) *and* `CLAUDE_CODE_AGENT` in env (inherited); trusting the env var destroyed a thread in testing | The thread hook trusts stdin only; the launcher exports no identity var |
| 2026-08-16 · 2.1.233 | `prepare-commit-msg` fires before the editor; a trailer on an empty message becomes the subject | Empty messages skipped; interactive commits with no `-m` get no trailer, accepted |
| 2026-08-16 · 2.1.233 | Memory injection is trust-gated and fails silently | "Amnesiac but in character" is a trust problem, not a symlink problem |
| 2026-09-02 | `dir/*` in `.gitignore` (with or without a `!dir/.claude/` negation) leaves the directory visible; `git add -A` records a gitlink | Nested repos ignored wholesale; gitlink guard kept |
| 2026-09-09 · 2.1.267 | `memory: project` resolves against live cwd at spawn time | `memory: user` + relocated config dir; `setup.sh` section 3 |
| 2026-09-11 · 2.1.268 | `disable-model-invocation: true` did not prevent model invocation — the skill was invoked on request, no error | The key is treated as a declaration of intent (which `lint_skill.py` reads), never as a gate; `GUIDE.md`'s frontmatter table now says so |
| 2026-09-11 · 2.1.268 | Lazy skill discovery fires on the **Read/Edit tool**, not on Bash `cat`/`sed`. Four runs: Read attached the nested skill, Bash did not | A bash-first session silently gets no craft or project skills. `GUIDE.md`, "Skills"; the craft indices and every specialist def now say Read tool explicitly |
| 2026-09-11 | `check-types` enforced its NOTE vocabulary with a branch that could not fire — it filtered to the four legal values and then tested membership in the same four | The branch was replaced with two checks that can fail (unfilled mold placeholder; `## Measured` on a non-`finding`), and rule 7 now states which of the two vocabularies is actually enforceable |
| 2026-09-10 | Two checks reported clean without exercising their mechanism (leak guard's `CS:` prefix; pointer check's root prune) | Every guard needs a positive test — `hooks/README.md` |

## How to read these
A dated number is a claim about that day and that version. The harness moves; the tree
moves. The value of the table is not the numbers but the habit: **measure before ruling,
write the number next to the rule, and date it** so the next reader can tell whether it is
still true.
