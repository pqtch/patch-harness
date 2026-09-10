#!/usr/bin/env bash
# gitlink_guard.sh — layer 2 of the gitlink guard: PreToolUse, settings-level.
#
# Why two layers: ~/workspace/docs/harness-hooks.md. Layer 1 (.git/hooks/pre-commit, installed by
# _ops/bin/setup.sh) is defeated by `git config core.hooksPath /dev/null`. This layer is a
# Claude Code PreToolUse hook registered in settings.json with matcher "Bash" — it does not
# live under .git at all, so it survives that. Neither layer covers the other's blind spot
# (this one only sees commits made through this harness's Bash tool); both are installed.
#
# Reads stdin JSON (tool_name, tool_input.command, cwd, ...). Only fires when tool_name is
# Bash AND a `;`/`&&`/`||`/`|`-separated segment actually *invokes* git with `commit` as its
# subcommand — not merely mentions the words `git` and `commit` anywhere in the segment (that
# looser check used to fire on e.g. `head .git/hooks/pre-commit`). See GIT_COMMIT_RE below for
# the exact grammar. Only acts if cwd is inside THIS workspace's repo — the guard is scoped to the tree
# it ships in, not every repo the harness might touch.
#
# Predicate is identical to layer 1's: read the staged DELTA (git diff --cached --raw
# against HEAD, or the empty tree on the first commit), never `git ls-files -s`.
#
# FAILS OPEN. Any internal error (missing jq, bad JSON, git failure) falls
# through to `exit 0` — this guard must never be the thing that breaks a session.

set -u

# ROOT is this workspace — derived from the script's own location, never hardcoded.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd -P)"

# GIT_COMMIT_RE — matches a segment that *invokes* git with `commit` as its subcommand.
# Grammar: optional leading whitespace, optional `VAR=val` assignments, then the command
# word (bare `git` or any path ending in `/git`), then zero or more global options — either
# a value-taking flag (`-C <dir>`, `-c k=v`) or a bare `-x`/`--long[=val]` flag — then
# `commit` as the first non-option word. This deliberately does NOT match plain-text
# mentions of "git" and "commit" in unrelated commands (`head .git/hooks/pre-commit`,
# `ls git-commit-notes`), nor a quoted string like `echo "git commit"` — because none of
# those are the command word `git` at the start of the segment. Err toward firing: any
# actual invocation shape we didn't anticipate should be added here rather than worked
# around at the call site.
GIT_COMMIT_RE='^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*=[^[:space:]]*[[:space:]]+)*([^[:space:]]*/)?git([[:space:]]+(-[Cc][[:space:]]+[^[:space:]]+|--[A-Za-z0-9-]+(=[^[:space:]]*)?|-[A-Za-z]+))*[[:space:]]+commit\b'

# Everything is best-effort inside this block; any failure falls through to allow (exit 0).
main() {
  command -v jq >/dev/null 2>&1 || return 0

  local input tool_name command cwd
  input="$(cat)" || return 0

  tool_name="$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null)" || return 0
  [ "$tool_name" = "Bash" ] || return 0

  command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)" || return 0
  [ -n "$command" ] || return 0

  cwd="$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)" || return 0
  [ -n "$cwd" ] || return 0

  # "Runs git commit" filter: split on command separators, check each segment against
  # GIT_COMMIT_RE (defined above) — an actual git-commit invocation, not just a mention.
  local fires=0 seg
  local IFS_OLD="$IFS"
  local normalized
  normalized="$(printf '%s' "$command" | sed -E 's/(&&|\|\||[;|])/\n/g')"
  while IFS= read -r seg; do
    if printf '%s' "$seg" | grep -qE "$GIT_COMMIT_RE"; then
      fires=1
      break
    fi
  done <<EOF
$normalized
EOF
  IFS="$IFS_OLD"

  [ "$fires" -eq 1 ] || return 0

  # Only act inside this workspace's repo. Resolve cwd's repo root and compare against ROOT.
  local repo_root ws_root
  repo_root="$(cd "$cwd" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null)" || return 0
  [ -n "$repo_root" ] || return 0
  ws_root="$ROOT"
  repo_root="$(cd "$repo_root" 2>/dev/null && pwd -P)" || return 0
  [ "$repo_root" = "$ws_root" ] || return 0

  local empty_tree base gitlinks
  empty_tree="4b825dc642cb6eb9a060e54bf8d69288fbee4904"
  base="$(cd "$repo_root" && git rev-parse --verify -q HEAD 2>/dev/null || echo "$empty_tree")"

  gitlinks="$(cd "$repo_root" && git diff --cached --raw "$base" 2>/dev/null | awk '$2=="160000" {print $NF}')" || {
    return 0
  }

  if [ -n "$gitlinks" ]; then
    {
      echo "ws: gitlink guard (layer 2) — refusing this commit"
      echo "The following would be staged as submodule entries (mode 160000):"
      echo "$gitlinks" | sed 's/^/  /'
      echo
      echo "Recovery — run for each path:"
      echo "$gitlinks" | while IFS= read -r p; do echo "  git rm --cached -f $p"; done
    } >&2
    return 2
  fi

  return 0
}

main
exit $?
