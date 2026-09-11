# SETUP

Small: one clone, one script, one restart, one login.

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
bash _ops/bin/setup.sh
```
`~/workspace` is the name every path in the tree uses. Clone it somewhere else if you like —
it is a name, not a mechanism — then rewrite the name everywhere, substituting your path:
```sh
grep -rl '~/workspace' --exclude-dir=.git . | xargs sed -i 's#~/workspace#~/YOUR-PATH#g'   # GNU sed; on macOS: sed -i ''
```

`setup.sh` is idempotent and does three things, saying which as it goes:
1. Installs `prepare-commit-msg` — every commit made from inside a session carries a
   `Session: <id>` trailer, the join key between a commit and its transcript.
2. Installs `pre-commit` — the gitlink guard, plus the pointer check as a warning. **If a
   `pre-commit` you wrote is already there, it is kept and chained**, not overwritten.
3. **Asks** whether to relocate the Claude Code config dir into this repo. Say yes. What
   that does, exactly:
   - appends two lines to `~/.bashrc` setting `CLAUDE_CONFIG_DIR=~/workspace/.claude-config` <!-- may-be-absent -->
     (zsh users: copy those two lines into `~/.zshrc`; the script only knows bash)
   - creates `.claude-config/agent-memory -> ../.claude/agent-memory`
   - copies your existing `~/.claude` **config only** (settings, agents, skills, commands) —
     never credentials, never other projects' transcripts
   - leaves `~/.claude` exactly as it was; undo is deleting the two lines

   Why it matters: every specialist def says `memory: user`, which resolves to
   `<config dir>/agent-memory/<name>/`. Relocated, that is a tracked path inside this repo.
   Not relocated, it is `~/.claude/agent-memory/`, outside the repo, and specialist memory
   silently stops travelling with the tree.

Then open a new terminal (or `exec bash`), and:
```sh
echo 'export PATH="$HOME/workspace/_ops/bin:$PATH"' >> ~/.bashrc && exec bash   # optional: puts `ws` on PATH
cd ~/workspace
claude          # or: ws
/login          # once per machine — credentials are gitignored on purpose, so they never travel with the repo
```

`ws` is the launcher: `ws` alone is a blank session at the root; `ws center`, `ws researcher`,
`ws analyst` launch as that specialist. Without the PATH line, write `_ops/bin/ws`.

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
commits that carry your private words into it. It is not installed by `setup.sh` — there is
nothing to guard until you have a public repo. When you do:
```sh
mkdir -p _ops/private && printf 'CS:\\bYourName\\b:the owner by name\n' > _ops/private/denylist.txt   # one pattern:reason per line; gitignored
printf '#!/usr/bin/env bash\nexec ~/workspace/_ops/bin/check-leak --repo "$(git rev-parse --show-toplevel)"\n' > /path/to/public-repo/.git/hooks/pre-commit
chmod +x /path/to/public-repo/.git/hooks/pre-commit
```
Then **plant a known leak** — stage a file containing your name in the public repo and
confirm the commit is refused — before trusting it. A guard that has only ever passed has
not been tested.

## Verify
From inside a session (so the trailer hook has a session id to stamp):
```sh
_ops/bin/check-selftest     # plants every guard's failure; 0 failed
_ops/bin/check-pointers      # 0 dead pointers
_ops/bin/check-types         # type: vocabularies OK
git add .claude-config && git commit -m 'setup' && git log -1 --format='%(trailers:key=Session)'   # prints Session: <id>
```
If a specialist's lane comes back empty, or an `agent-memory/` directory appears anywhere that
is not `.claude/agent-memory/`, the relocation did not take: check `echo $CLAUDE_CONFIG_DIR`
and the symlink. `~/workspace/.claude/agent-memory/README.md` has the full account.
