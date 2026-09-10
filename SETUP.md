# SETUP

Small: one clone, one script, one restart.

## Prerequisites
- **Claude Code** — the harness this tree is built for. Version-sensitive facts in the docs
  carry the version they were measured on.
- `git`, `python3`, `jq` — `jq` is what the two PreToolUse guards parse their input with.
  Without it they fail open (they do nothing) rather than break a session.
- `bash`. The scripts are bash; the tree has been used from Linux and WSL.

## Install
```sh
git clone <this repository> ~/workspace
cd ~/workspace
_ops/bin/setup.sh
```
`~/workspace` is the name every path in the tree uses. Clone it somewhere else if you like,
then `grep -rl '~/workspace' . | xargs sed -i 's#~/workspace#~/elsewhere#g'` — it is a name,
not a mechanism.

`setup.sh` is idempotent and does three things, saying which as it goes:
1. Installs `prepare-commit-msg` — every commit made from inside a session carries a
   `Session: <id>` trailer, the join key between a commit and its transcript.
2. Installs `pre-commit` — the gitlink guard, plus the pointer check as a warning. **If a
   `pre-commit` you wrote is already there, it is kept and chained**, not overwritten.
3. **Asks** whether to relocate the Claude Code config dir into this repo. Say yes. What
   that does, exactly:
   - appends two lines to `~/.bashrc` setting `CLAUDE_CONFIG_DIR=~/workspace/.claude-config`
   - creates `.claude-config/agent-memory -> ../.claude/agent-memory`
   - copies your existing `~/.claude` **config only** (settings, agents, skills, commands) —
     never credentials, never other projects' transcripts
   - leaves `~/.claude` exactly as it was; undo is deleting the two lines

   Why it matters: every specialist def says `memory: user`, which resolves to
   `<config dir>/agent-memory/<name>/`. Relocated, that is a tracked path inside this repo.
   Not relocated, it is `~/.claude/agent-memory/`, outside the repo, and specialist memory
   silently stops travelling with the tree.

Then **restart your shell**, `cd ~/workspace`, and:
```sh
claude          # or: _ops/bin/ws — the launcher; put _ops/bin on PATH
/login          # once per machine; credentials are gitignored on purpose
```

To launch as a specialist: `ws center`, `ws researcher`, `ws analyst`.

## What ships empty, on purpose
- `projects/`, `sketch/` — indices only. The first project is made with the `project-author`
  skill, which loads on touching anything under `projects/`.
- `craft/center/`, `craft/analyst/` — empty skill pools whose `CLAUDE.md` says so, because
  an empty pool and a pool that failed to attach look identical from inside a session.
- `.claude/agent-memory/*/MEMORY.md` — empty typed indices. Filled through use.
- `.claude/USER.md` — who the owner is. Filled through use, not at setup.
- `_ops/journal/`, `_ops/plans/`, `_ops/inbox/`, `_ops/archive/` — indices only.

## On names
The three specialists ship **without names**. Each def says: *I have no name yet; naming
myself is mine to do, not yours to configure.* This is deliberate and it is the one thing
this file asks you not to do: do not fill a name in for them. A name is not configuration —
it arrives through use, and the specialist writes it into its own identity memory. The role
words (`center`, `researcher`, `analyst`) are the dispatch keys and they stay.

## Optional: the leak guard
If you ever extract something public from this workspace, `_ops/bin/check-leak` refuses
commits that carry your private words into it. It reads a gitignored wordlist at
`_ops/private/denylist.txt` (format in the script header) and is not installed by `setup.sh`
— there is nothing to guard until you have a public repo. Install it as that repo's
`pre-commit`, then **test it by planting a known leak** before trusting it.

## Verify
```sh
_ops/bin/check-pointers      # 0 dead pointers
_ops/bin/check-types         # type: vocabularies OK
git log -1 --format='%(trailers:key=Session)'   # after a commit from inside a session
```
If a specialist's lane comes back empty, or an `agent-memory/` directory appears anywhere that
is not `.claude/agent-memory/`, the relocation did not take: check `echo $CLAUDE_CONFIG_DIR`
and the symlink. `~/workspace/.claude/agent-memory/README.md` has the full account.
