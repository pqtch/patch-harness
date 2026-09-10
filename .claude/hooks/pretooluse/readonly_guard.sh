#!/usr/bin/env bash
# readonly_guard.sh — the Bash half of the `p.*` read-only rule (workspace-rules.md rules 4, 6).
#
# The permission rung covers this only partway. `.claude/settings.json` denies Edit(p.*) and
# Edit(**/p.*), which the harness applies to every file-EDITING TOOL. It cannot see a Bash
# command: sessions here run bash-first (auto mode explicitly prefers sed/heredocs over Edit),
# so `sed -i p.notes.md` walked straight past the permission rung until this hook existed.
#
# Note also (2026-09-01): `Write(...)` and `NotebookEdit(...)` PATH rules do nothing at all —
# the harness prints a startup warning saying only Edit(path) rules are matched. Four such dead
# rules were removed the same day. Do not re-add them; see _note_permissions in settings.json.
#
# What this refuses: a Bash command that looks like it MUTATES a p.-prefixed file — an in-place
# editor, a redirect onto it, or a move/copy/delete of it. Reading (`cat p.notes.md`, `sed -n`,
# `grep`) is always allowed: the rule is read-ONLY, not no-access.
#
# Deliberately conservative about what counts as a write. A shell is arbitrarily expressive and
# no regex closes it (`P=p.notes.md; sed -i "" $P`, base64, a python one-liner). This raises the
# cost of an ACCIDENT — the realistic failure — and does not pretend to stop a determined
# workaround. Rule 5: better a guard whose blind spot is written down than prose nobody reads.
#
# FAILS OPEN — any internal error exits 0. A guard must never be the thing that breaks a session.
set -u

main() {
  command -v jq >/dev/null 2>&1 || return 0
  local input tool_name command
  input="$(cat)" || return 0
  tool_name="$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null)" || return 0
  [ "$tool_name" = "Bash" ] || return 0
  command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)" || return 0
  [ -n "$command" ] || return 0

  # A p.-prefixed FILENAME: start of string, or after a space, slash, quote or =.
  local PFILE='(^|[ /"'"'"'=])p\.[A-Za-z0-9._-]+'

  printf '%s' "$command" | grep -qE "$PFILE" || return 0

  local why=""
  # 1. in-place editors naming a p. file anywhere in the command
  if printf '%s' "$command" | grep -qE '(^|[ ;&|])(sed|perl|ruby)([ ]+-[^ ]*)*[ ]+-[^ ]*i'; then
    why="an in-place editor (sed/perl -i)"
  # 2. redirect onto a p. file:  > p.foo   or  >> p.foo   (but not 2>/dev/null etc.)
  elif printf '%s' "$command" | grep -qE '>>?[[:space:]]*([^ ;&|]*/)?p\.[A-Za-z0-9._-]+'; then
    why="a shell redirect onto it"
  # 3. destructive file ops with a p. file as an argument
  elif printf '%s' "$command" | grep -qE '(^|[ ;&|])(rm|mv|cp|truncate|dd|tee|install|chmod|chown)([[:space:]]+-[^[:space:]]*)*[[:space:]]+([^;&|]*[[:space:]/"'"'"'=])?p\.[A-Za-z0-9._-]+'; then
    why="a destructive file operation (rm/mv/cp/tee/truncate/...)"
  # 4. python/awk in-place-ish write helpers
  elif printf '%s' "$command" | grep -qE "open\([^)]*p\.[A-Za-z0-9._-]+[^)]*['\"](w|a|r\+)"; then
    why="a python open() in write mode"
  fi

  [ -n "$why" ] || return 0

  {
    echo "ws: read-only guard — refusing to modify a \`p.*\` file."
    echo
    echo "Detected: $why."
    echo "Rule 4: the \`p.\` prefix marks the file as the owner's and read-only. Reading is fine"
    echo "(cat, sed -n, grep, head); writing is not — including from Bash, which the"
    echo "Edit(p.*) permission rules cannot see."
    echo
    echo "If the owner asked for this change, have THEM make it, or ask them to confirm explicitly."
  } >&2
  return 2
}

main
exit $?
