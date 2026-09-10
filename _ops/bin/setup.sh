#!/usr/bin/env bash
# setup.sh — install this workspace's git hooks, and (on request) relocate the Claude Code
# config dir into the repo. Idempotent: run it again after any pull that touches it.
#
# Three jobs:
#   1. `prepare-commit-msg` — stamps `Session: <id>` on every commit made from inside a
#      Claude Code session. The trailer is the join key between a commit and its transcript.
#   2. `pre-commit` — the gitlink guard (layer 1 of two; layer 2 is the settings-level
#      PreToolUse hook, which is the only layer that survives `core.hooksPath`), plus the
#      pointer check as a warning. If a pre-commit hook this script did not write is already
#      there, it is KEPT and CHAINED, never overwritten — see install_precommit_hook.
#   3. The relocated config dir — asked, never assumed. See install_config_dir.
#
# ROOT is derived from this script's location, never hardcoded, so the tree can live anywhere.
# The git hooks dir is resolved with `git rev-parse --git-path hooks`, not hardcoded to
# $ROOT/.git/hooks, so a worktree or a nested launch point resolves correctly.
#
# NOT here, deliberately: no PreToolUse guards (those are registered in .claude/settings.json
# and need no install), no PATH edits beyond the one line the config dir needs.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WARNINGS=0

say()  { printf '%s\n' "ws setup: $*"; }
warn() { printf '%s\n' "ws setup: WARN $*" >&2; WARNINGS=$((WARNINGS + 1)); }

hooks_dir_of_root() {
  local d
  d="$(git -C "$ROOT" rev-parse --git-path hooks 2>/dev/null)" || return 1
  # `--git-path hooks` answers RELATIVE to the queried dir when the repo root is above it.
  # Absolutise, then normalise, so the path printed is one a human can paste.
  case "$d" in /*) ;; *) d="$ROOT/$d" ;; esac
  mkdir -p "$d"
  cd "$d" && pwd
}

# Write $2 (a temp file) to $1 only if it differs; report installed/updated/unchanged.
place_hook() {
  local hook="$1" tmp="$2"
  chmod +x "$tmp"
  if [ -e "$hook" ] && cmp -s "$tmp" "$hook"; then rm -f "$tmp"; return 0; fi
  local verb="installed"; [ -e "$hook" ] && verb="updated"
  mv -f "$tmp" "$hook"
  say "$verb $hook"
}

# ── 1. prepare-commit-msg: the Session: trailer ───────────────────────────────
MARKER="# ws-managed: Session trailer hook"

install_commit_hook() {
  local hooks_dir hook tmp
  hooks_dir="$(hooks_dir_of_root)" || { warn "$ROOT is not inside a git repo — skipping prepare-commit-msg"; return 0; }
  hook="$hooks_dir/prepare-commit-msg"

  if [ -e "$hook" ] && ! grep -qF "$MARKER" "$hook" 2>/dev/null; then
    warn "a foreign prepare-commit-msg already exists at $hook — left untouched"
    return 0
  fi

  tmp="$hook.ws.tmp"
  cat > "$tmp" <<HOOK
#!/usr/bin/env bash
$MARKER
# Appends 'Session: <CLAUDE_CODE_SESSION_ID>' so a commit can be joined to its transcript.
# Installed by $ROOT/_ops/bin/setup.sh — edit there, not here; setup.sh overwrites this file.
#
# MEASURED 2026-08-16, Claude Code 2.1.233: git hooks inherit the environment of the process
# that ran git, and a Claude Code session has CLAUDE_CODE_SESSION_ID=<uuid> in its Bash env.
# So a commit made by a session is stamped automatically and a commit made by hand is not —
# which is the intended discrimination, not a gap.
#
# \$2 (the message source) decides whether appending is right. Skipped:
#   merge    — the message is generated and about the merge, not this session
#   squash   — a scratch message the user is about to rewrite wholesale
#   template — a -t template; the trailer would land inside someone else's scaffold
# Allowed: 'message' (-m/-F), 'commit' (--amend, -c/-C), and '' (bare editor) only when the
# message is already non-empty.
#
# MEASURED 2026-08-16: prepare-commit-msg fires BEFORE the editor opens, so on a bare
# \`git commit\` the message file holds nothing but comments at hook time. Trailering an empty
# message puts 'Session: …' on line 1, where it becomes the SUBJECT — git then does not read
# it as a trailer at all, and the real subject lands underneath it. CONSEQUENCE: an empty
# message is skipped, so an interactive \`git commit\` with no -m gets NO trailer. That is a
# deliberate loss, not an oversight: the only event late enough to stamp it is commit-msg,
# which receives no \$2 and so cannot tell a merge from a normal commit. Sessions commit
# with -m, which is stamped correctly.
set -euo pipefail

MSG_FILE="\$1"
SOURCE="\${2:-}"

case "\$SOURCE" in
  merge|squash|template) exit 0 ;;
esac

[ -n "\${CLAUDE_CODE_SESSION_ID:-}" ] || exit 0
[ -f "\$MSG_FILE" ] || exit 0

# Nothing but comments/blank lines yet — see the note above. stripspace honours a custom
# core.commentChar, which a hardcoded '#' would not.
if [ -z "\$(git stripspace --strip-comments < "\$MSG_FILE")" ]; then
  exit 0
fi

# Already stamped (re-amend, rebase reword) — leave it alone.
if grep -qiE '^Session:[[:space:]]' "\$MSG_FILE"; then
  exit 0
fi

git interpret-trailers --in-place \\
  --trailer "Session: \$CLAUDE_CODE_SESSION_ID" "\$MSG_FILE" || exit 0
HOOK
  place_hook "$hook" "$tmp"
}

install_commit_hook

# ── 2. pre-commit: the gitlink guard (layer 1) + pointer check, CHAINED ───────
# Reads the staged DELTA (git diff --cached --raw against HEAD, or the empty tree on the
# first commit), never `git ls-files -s` — the latter reports whole-index state and wedges
# permanently once a gitlink reaches HEAD. Fails open: any internal error exits 0.
# `core.hooksPath /dev/null` defeats this layer entirely — that is why layer 2 exists.
#
# CHAINING, and why. A repo may already carry a pre-commit hook this script did not write —
# the case that produced this section was an extracted repo whose pre-commit was a content
# leak guard living in another tree. The previous behaviour was "warn: foreign hook, left
# untouched" — which meant the gitlink guard was silently installed NOWHERE, and the warning
# was the only trace. Now: a foreign hook is moved ONCE to `pre-commit.local` (announced,
# never silent), and the hook written here runs it FIRST, then the gitlink guard. Either
# refusing refuses the commit. The foreign hook is never edited.
PRECOMMIT_MARKER="# ws-managed: gitlink guard"

install_precommit_hook() {
  local hooks_dir hook tmp local_hook
  hooks_dir="$(hooks_dir_of_root)" || { warn "$ROOT is not inside a git repo — skipping pre-commit"; return 0; }
  hook="$hooks_dir/pre-commit"
  local_hook="$hooks_dir/pre-commit.local"

  if [ -e "$hook" ] && ! grep -qF "$PRECOMMIT_MARKER" "$hook" 2>/dev/null; then
    if [ -e "$local_hook" ]; then
      warn "a foreign pre-commit exists at $hook AND $local_hook is taken — left untouched; the gitlink guard is NOT installed"
      return 0
    fi
    mv "$hook" "$local_hook"
    say "moved foreign pre-commit to $local_hook — it will run FIRST, chained from the managed hook"
  fi

  tmp="$hook.ws.tmp"
  cat > "$tmp" <<HOOK
#!/usr/bin/env bash
$PRECOMMIT_MARKER
# Installed by $ROOT/_ops/bin/setup.sh — edit there, not here; setup.sh overwrites this file.
# Runs, in order: (a) pre-commit.local if present — a hook that was here before setup.sh,
# kept and chained, never overwritten; (b) the gitlink guard — refuses a commit that would
# stage a gitlink (mode 160000); (c) the pointer check — a WARNING that never blocks.
# (a) and (b) each refuse independently. Fails open on internal error.

HOOKS_DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
if [ -x "\$HOOKS_DIR/pre-commit.local" ]; then
  "\$HOOKS_DIR/pre-commit.local" "\$@" || exit \$?
fi

EMPTY_TREE=4b825dc642cb6eb9a060e54bf8d69288fbee4904
BASE="\$(git rev-parse --verify -q HEAD || echo \$EMPTY_TREE)"

GITLINKS="\$(git diff --cached --raw "\$BASE" 2>/dev/null | awk '\$2=="160000" {print \$NF}')" || exit 0

if [ -n "\$GITLINKS" ]; then
  {
    echo "ws: gitlink guard — refusing commit"
    echo "The following would be staged as submodule entries (mode 160000):"
    echo "\$GITLINKS" | sed 's/^/  /'
    echo
    echo "Recovery — run for each path:"
    echo "\$GITLINKS" | while IFS= read -r p; do echo "  git rm --cached -f \$p"; done
  } >&2
  exit 1
fi

# ── pointer check — WARNING ONLY, never blocks ──────────────────────────────────
POINTERS="$ROOT/_ops/bin/check-pointers"
[ -x "\$POINTERS" ] && "\$POINTERS" >&2 || true

exit 0
HOOK
  place_hook "$hook" "$tmp"
}

install_precommit_hook

# ── 3. the relocated config dir — ASKED, never assumed ────────────────────────
# WHAT IT DOES: sets CLAUDE_CONFIG_DIR=$ROOT/.claude-config in ~/.bashrc, so transcripts,
# prompt history, tasks and specialist memory live INSIDE this repo and travel between
# machines through git. Secrets and machine-local state stay out via .gitignore.
#
# WHY THE SYMLINK IS LOAD-BEARING: every specialist def is `memory: user`, which resolves to
# <config dir>/agent-memory/<name>/ — ABSOLUTE, so it survives the main session `cd`-ing,
# which is what `memory: project` does not (MEASURED 2026-09-09, Claude Code 2.1.267:
# `project` resolves against live cwd at spawn time and silently hands a specialist an
# empty lane). The symlink then puts the real files back at .claude/agent-memory/, where
# every doc says they are. Without it, lanes land in .claude-config/ and the tracked lane
# goes unread. WITHOUT THE RELOCATION AT ALL, lanes land in ~/.claude/agent-memory/ —
# outside the repo, untracked, and the memory story fails with no error. That is why this
# section exists, and why it asks instead of skipping.
#
# WHAT IS COPIED from an existing ~/.claude: the user-scope CONFIG only — settings.json,
# CLAUDE.md, keybindings.json, agents/, skills/, commands/. NOT copied: credentials (run
# `claude` and /login once per machine), and NOT transcripts/history of other projects —
# this repo is tracked, and another project's transcripts do not belong in its history.
# ~/.claude itself is never modified or deleted; undo is two lines in ~/.bashrc.
#
# The env var cannot live in settings.json: the config dir is resolved BEFORE settings are
# read. So it is a shell-profile line — the one thing this script writes outside the repo.
install_config_dir() {
  local cfg="$ROOT/.claude-config" link="$ROOT/.claude-config/agent-memory"
  local rc="$HOME/.bashrc" marker="# ws-managed: CLAUDE_CONFIG_DIR"

  if [ -f "$rc" ] && grep -qF "$marker" "$rc"; then
    : # already relocated on this machine; just make sure the pieces are in place
  elif [ "${WS_SETUP_RELOCATE:-}" = "yes" ]; then
    : # non-interactive opt-in
  elif [ -t 0 ]; then
    printf 'ws setup: relocate the Claude Code config dir into this repo?\n'
    printf '          (~/.claude -> %s; ~/.claude is left as it is) [y/N] ' "$cfg"
    local ans; read -r ans
    case "$ans" in y|Y|yes|YES) ;; *) say "config dir NOT relocated — specialist memory will land in ~/.claude/agent-memory, outside this repo. Re-run setup.sh to change that."; return 0 ;; esac
  else
    say "config dir NOT relocated (no terminal to ask). Run setup.sh interactively, or WS_SETUP_RELOCATE=yes."
    return 0
  fi

  mkdir -p "$cfg"
  if [ -L "$link" ]; then :
  elif [ -e "$link" ]; then warn "$link exists and is not a symlink — left untouched; agent lanes may not resolve"
  else ln -s ../.claude/agent-memory "$link"; say "linked $link -> ../.claude/agent-memory"; fi

  local old="$HOME/.claude" item
  if [ -d "$old" ] && [ "$(cd "$old" && pwd -P)" != "$(cd "$cfg" && pwd -P)" ]; then
    for item in settings.json CLAUDE.md keybindings.json agents skills commands; do
      [ -e "$old/$item" ] && [ ! -e "$cfg/$item" ] && cp -r "$old/$item" "$cfg/$item" && say "copied ~/.claude/$item"
    done
  fi

  if [ -f "$rc" ] && grep -qF "$marker" "$rc"; then :
  elif [ -f "$rc" ]; then
    { echo ""; echo "$marker (undo: delete these two lines; ~/.claude is untouched)"; echo "export CLAUDE_CONFIG_DIR=\"$cfg\""; } >> "$rc"
    say "added CLAUDE_CONFIG_DIR to $rc — restart your shell, then run \`claude\` (or \`ws\`) from $ROOT and /login once"
  else
    warn "no $rc — set CLAUDE_CONFIG_DIR=$cfg in your shell profile by hand"
  fi
}

install_config_dir

if [ "$WARNINGS" -gt 0 ]; then say "done, with $WARNINGS warning(s) above — nothing was deleted"; else say "done"; fi
