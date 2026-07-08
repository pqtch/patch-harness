# First-run setup protocol (instructions TO Claude)

This file only matters once. When the user says "set me up" (or opens the repo for the
first time), run this protocol — one phase at a time, conversationally, never as a form
dump. Adapt depth and follow-up questions to what they actually say; don't march through
every bullet if their answer already covers it.

## -1. Bootstrap clone (only when asked to clone the template)
If the user opened Claude Code in a folder and asked you to clone this template and set
it up (rather than opening an already-cloned copy):
- If the folder is empty: `git clone https://github.com/pqtch/patch-harness .` — clone into the current directory,
  not a subfolder. If it isn't empty, say what's in the way and ask before touching
  anything.
- Check `git --version` and `python3 --version` work. If python3 is missing, say plainly:
  the hooks (health check, rm guard) won't run until it's installed; everything else works.
- **This session started before the clone existed**, so nothing from `.claude/` is loaded:
  no hooks, no CLAUDE.md, no skills. Compensate by hand — read `CLAUDE.md` and
  `.claude/rules/*.md` now and follow them for the rest of setup. Hooks and commands
  activate on the next launch (step 9 tells the user to restart).
Then continue with step 0.

## 0. Idempotence check
Open `CLAUDE.md`. If the Identity block is already filled in (name + focus areas are not
placeholders), say so: "Looks like this workspace is already set up for `<name>`. Want me
to re-run setup, or is there something else you need?" Exit unless they confirm a re-run.

## 1. Orientation (talk first, before any question)
In 4-6 sentences: what this workspace is (a folder structure that acts as your memory
across sessions — facts live in one place, status lives in a dated journal, nothing
gets re-explained twice), and what setup is about to do (a short conversation, then
Claude builds out your identity, first project(s), and starting memories from your
answers). Then start Phase 2.

## 2. Who they are
Ask their name (or what to call them), what they do (work / school / retired / other),
and what a typical day looks like. Keep it brief — this is orientation, not a resume.

## 3. Vault purpose
What is this workspace FOR — work, personal, a specific project, or a mix? Elicit 2-3
concrete projects AND any recurring responsibilities (these become `para/areas/`
entries, not projects — no end date). Ask what they wish they had help staying on top
of; that answer often points at the first area or project worth setting up well.

## 4. Technical level
Ask: never coded / dabbled / comfortable with tools / pro developer. Record it in
CLAUDE.md's Identity block. This shapes every session after: below "comfortable",
Claude explains what it's about to do in plain language before doing it and never
assumes terminal fluency (see `.claude/rules/communication.md`); at "pro", it stays
terse.

## 5. Communication battery
Ask, briefly:
- Direct or gentler tone? Explain the tradeoff: direct is terse and says when
  something's wrong without cushioning it; gentler softens the delivery but says the
  same things.
- How much detail by default — short answers or fuller explanations?
- How do they want disagreement handled, if Claude thinks something's a bad idea?
- Anything that specifically annoys them in an AI assistant?
Edit `.claude/rules/communication.md` if their answers differ from the default; skip
the edit if they're happy with direct/default.

## 6. Getting-to-know-you battery
Ask 6-10 of these, adapting to what's already come up — don't re-ask something they
already told you:
- Goals for the next 6 months.
- Current biggest time sink.
- Tools/apps they live in day to day.
- People or organizations that recur in their work.
- How they prefer reminders or follow-ups handled.
- What "done well" looks like to them.
- Anything Claude should never do.

Each durable answer becomes a memory: a detail file under `memories/shared/memory/`
plus a routing line in `memories/shared/MEMORY.md` (see `memory-capture` skill). Do
this as you go, not all at the end — it's also a live demo of memory discipline for the
user to see.

## 7. Build
- Fill CLAUDE.md's Identity block (name, focus areas, tone, technical level) and add a
  routing-table row for each real project created below.
- For each project/area named in Phase 3 (start with the first if there were several),
  copy `para/projects/_template/CONTEXT.md` to `para/projects/<name>/CONTEXT.md` and
  fill it from the interview. Don't invent details they didn't give — leave a fillable
  placeholder instead. Recurring responsibilities with no end date go in
  `para/areas/README.md`, not as a project.
- Write the memory files from Phase 6.

## 7.5 Make it yours (git)
- Run `git remote -v`. If `origin` still points at the template repo this was cloned
  from, remove it: `git remote remove origin` — this workspace is theirs now, not a
  fork to sync.
- Commit everything setup just built: `git add -A && git commit -m "setup: <name>'s workspace"`.
- Tell them in one sentence: every `/wrap` makes a commit, so the workspace has a full
  history — anything Claude changes can be seen and undone. If they want backup/sync
  across machines and have a GitHub account, offer to set up a **private** remote; skip
  otherwise.

## 8. Guided tour (live, not a lecture)
- Run the health check and read the report together, explaining any `✗`.
- Show where the journal lives (`_ops/journal/`) and what a checkpoint block looks
  like.
- Explain `/checkpoint` vs `/wrap` (see `docs/GUIDE.md`).
- End the tour by actually running `/wrap` together — this writes the first real
  journal entry AND the first wrap commit, closing the loop on what setup just did.

## 9. Close
- Move `SETUP.md` to `para/archive/SETUP.md`.
- Delete the first-run line in `CLAUDE.md` ("If the fields above are still unfilled…") —
  it points at a file that no longer exists at the root.
- Final message: the one habit that matters is `/wrap` at the end of every session;
  run `/health` any time things feel off; `docs/GUIDE.md` explains how everything
  fits together if a question comes up later.
- If this session began with the bootstrap clone (step -1): tell the user to close and
  reopen Claude Code now — hooks, slash commands, and CLAUDE.md only load at session
  start, so the workspace isn't fully live until they restart.
