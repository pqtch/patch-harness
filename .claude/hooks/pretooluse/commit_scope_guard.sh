#!/usr/bin/env bash
# commit_scope_guard.sh — refuses a `git commit` that would sweep staged files the command did
# not name. PreToolUse, matcher Bash, settings-level.
#
# THE INCIDENT, twice (docs/incidents.md #3):
# a command stages SPECIFIC paths (`git add probe.md`) and then commits with NO pathspec
# (`git commit -m …`). `git commit` commits the whole index, so anything staged earlier — by
# a human mid-run, by a `git add -A` several commands ago — is swept into a commit that was
# meant for one file. 2026-08-26: a maintenance run came within one command of it. 2026-09-10:
# a session that had the first incident in context did it anyway, and the `reset --hard`
# that followed removed eleven files from the tree. A rule in a doc did not stop the person
# who wrote the doc. So: a hook.
#
# WHAT IT REFUSES, exactly: a Bash command in which some segment runs `git add <specific
# paths>` (not -A / --all / . / -u) AND some segment runs `git commit` without a `--`
# pathspec and without -a/--all, while the index ALREADY holds staged paths outside the
# named ones. Those extras are what would be swept; they are listed.
#
# WHAT IT DOES NOT REFUSE, deliberately: `git add -A && git commit` (intent is everything
# staged); a bare `git commit` with no `git add` in the same command (intent unknown — this
# guard does not nag, it catches the one shape that has actually bitten); `git commit -- p`.
#
# Blind spot, named: the index is read BEFORE the command runs, so a `git add` of extra paths
# inside the same command is invisible — but then the caller named them, which is the point.
# FAILS OPEN — any internal error exits 0.
set -u

GIT_ADD_RE='^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*=[^[:space:]]*[[:space:]]+)*([^[:space:]]*/)?git([[:space:]]+(-[Cc][[:space:]]+[^[:space:]]+|--[A-Za-z0-9-]+(=[^[:space:]]*)?|-[A-Za-z]+))*[[:space:]]+add([[:space:]]|$)'
GIT_COMMIT_RE='^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*=[^[:space:]]*[[:space:]]+)*([^[:space:]]*/)?git([[:space:]]+(-[Cc][[:space:]]+[^[:space:]]+|--[A-Za-z0-9-]+(=[^[:space:]]*)?|-[A-Za-z]+))*[[:space:]]+commit([[:space:]]|$)'

main() {
  command -v jq >/dev/null 2>&1 || return 0
  local input tool_name command cwd
  input="$(cat)" || return 0
  tool_name="$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null)" || return 0
  [ "$tool_name" = "Bash" ] || return 0
  command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)" || return 0
  cwd="$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)" || return 0
  [ -n "$command" ] && [ -n "$cwd" ] || return 0

  local named=() whole=0 commit_seen=0 commit_scoped=0 seg tok after
  while IFS= read -r seg; do
    if printf '%s' "$seg" | grep -qE "$GIT_ADD_RE"; then
      after="$(printf '%s' "$seg" | sed -E 's/^.*[[:space:]]add([[:space:]]|$)//')"
      for tok in $after; do
        case "$tok" in
          -A|--all|-u|--update|.|:/|./) whole=1 ;;
          --) ;;
          -*) ;;
          *) named+=("$tok") ;;
        esac
      done
    fi
    if printf '%s' "$seg" | grep -qE "$GIT_COMMIT_RE"; then
      commit_seen=1
      after="$(printf '%s' "$seg" | sed -E 's/^.*[[:space:]]commit([[:space:]]|$)//')"
      if printf ' %s ' "$after" | grep -qE ' (--|-a|--all|--only|-o|--include|-i) '; then commit_scoped=1; fi
    fi
  done <<EOF2
$(printf '%s' "$command" | sed -E 's/(&&|\|\||[;|])/\n/g')
EOF2

  [ "$commit_seen" -eq 1 ] || return 0
  [ "$whole" -eq 0 ] || return 0
  [ "${#named[@]}" -gt 0 ] || return 0
  [ "$commit_scoped" -eq 0 ] || return 0

  local root prefix staged
  root="$(cd "$cwd" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null)" || return 0
  prefix="$(cd "$cwd" 2>/dev/null && git rev-parse --show-prefix 2>/dev/null)" || return 0
  staged="$(cd "$root" && git diff --cached --name-only 2>/dev/null)" || return 0
  [ -n "$staged" ] || return 0

  local extras="" s n full
  while IFS= read -r s; do
    [ -n "$s" ] || continue
    local covered=0
    for n in "${named[@]}"; do
      n="${n#./}"; n="${n%/}"
      case "$n" in /*) full="${n#"$root"/}" ;; *) full="$prefix$n" ;; esac
      if [ "$s" = "$full" ] || [ "${s#"$full"/}" != "$s" ]; then covered=1; break; fi
    done
    [ "$covered" -eq 1 ] || extras="$extras$s"$'\n'
  done <<< "$staged"
  [ -n "$extras" ] || return 0

  {
    echo "ws: commit-scope guard — refusing this commit."
    echo
    echo "The command names paths for 'git add' (${named[*]}) but 'git commit' takes no pathspec,"
    echo "so it would also sweep these ALREADY-STAGED files into the same commit:"
    printf '%s' "$extras" | sed 's/^/  /'
    echo
    echo "Either commit only what you named:   git commit -m '…' -- ${named[*]}"
    echo "or commit everything on purpose:     git add -A && git commit -m '…'"
    echo "or unstage the rest first:           git reset -- <path>"
    echo "This is incident #3, which happened twice; see docs/incidents.md."
  } >&2
  return 2
}

main
exit $?
