#!/usr/bin/env python3
"""PreToolUse hook for Bash: blocks destructive operations against protected paths.

Governs by RESOLVED TARGET PATH, not the flag string. Covers rm/rmdir, `>` / `>>`
truncation, and `mv` overwrite-into-target. Fails closed: anything it can't parse or
resolve gets "ask", not "allow".

Policy (resolved against the workspace root):
  - deny: anything under .claude/; memories/**/MEMORY.md; system paths (/etc, /usr, ...)
  - ask:  anything else outside the workspace root; anything unresolvable/unparseable
  - allow: everything else inside the workspace

Hook protocol (Claude Code PreToolUse): deny -> reason on stderr + exit 2 (hard block);
allow/ask -> {"hookSpecificOutput": {"hookEventName": "PreToolUse",
"permissionDecision": ..., "permissionDecisionReason": ...}} on stdout + exit 0.
"""
import json
import re
import shlex
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]

DESTRUCTIVE_RE = re.compile(r"^(rm|rmdir)$")

SYSTEM_PATHS = ("/etc", "/usr", "/bin", "/sbin", "/boot", "/var", "/lib", "/opt", "/root")


def resolve(path_str, cwd):
    p = Path(path_str)
    if not p.is_absolute():
        p = cwd / p
    try:
        return p.resolve()
    except (OSError, RuntimeError):
        return None


def classify(resolved):
    """Return 'allow' | 'deny' | 'ask' for one resolved target path."""
    if resolved is None:
        return "ask"  # unresolvable -> fail closed on the human, not silently
    # /dev/* is a sink, not a file: >/dev/null lives in half of all shell commands,
    # and asking on it trains the user to click through — which kills the guard.
    if resolved == Path("/dev") or Path("/dev") in resolved.parents:
        return "allow"
    for sp in SYSTEM_PATHS:
        if resolved == Path(sp) or Path(sp) in resolved.parents:
            return "deny"
    try:
        resolved.relative_to(WORKSPACE_ROOT)
    except ValueError:
        return "ask"  # outside the workspace but not a system path -> human decides
    claude_dir = WORKSPACE_ROOT / ".claude"
    if resolved == claude_dir or claude_dir in resolved.parents:
        return "deny"
    if resolved.name == "MEMORY.md" and (WORKSPACE_ROOT / "memories") in resolved.parents:
        return "deny"
    return "allow"


def targets_from_rm(tokens):
    return [t for t in tokens[1:] if not t.startswith("-")]


def targets_from_redirect(command):
    # `>` or `>>` truncation/append targets, single-word or quoted paths
    return re.findall(r">>?\s*([^\s;&|]+)", command)


def targets_from_mv(tokens):
    # `mv a b` — the overwrite risk is the destination, b
    args = [t for t in tokens[1:] if not t.startswith("-")]
    return args[-1:] if len(args) >= 2 else []


def evaluate(command, cwd):
    try:
        segments = re.split(r"&&|\|\||;|\|", command)
    except re.error:
        return "ask", "could not parse command"

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
        try:
            tokens = shlex.split(segment)
        except ValueError:
            return "ask", f"could not tokenize segment: {segment!r}"
        if not tokens:
            continue

        cmd = tokens[0]
        targets = []
        if DESTRUCTIVE_RE.match(cmd):
            targets = targets_from_rm(tokens)
        elif cmd == "mv":
            targets = targets_from_mv(tokens)
        targets += targets_from_redirect(segment)

        for t in targets:
            # Name-based backstop: the guard cannot track `cd` across chained
            # segments, so a `.claude` component or a MEMORY.md target denies
            # regardless of where the path resolves.
            parts = Path(t).parts
            if ".claude" in parts or Path(t).name == "MEMORY.md":
                return "deny", f"destructive op targets protected name: {t}"
            resolved = resolve(t, cwd)
            verdict = classify(resolved)
            shown = str(resolved) if resolved else t
            if verdict == "deny":
                return "deny", f"destructive op targets protected path: {shown}"
            if verdict == "ask":
                return "ask", f"destructive op targets a path outside the workspace: {shown}"

    return "allow", "no protected path targeted"


def emit(decision, reason):
    """Speak the Claude Code PreToolUse hook protocol; return the exit code."""
    if decision == "deny":
        print(f"rm-guard BLOCKED: {reason}", file=sys.stderr)
        return 2  # exit 2 = hard block, honored by all CC versions
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,          # "allow" | "ask"
        "permissionDecisionReason": reason,
    }}))
    return 0


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return emit("ask", "unparseable hook payload")

    tool_input = payload.get("tool_input", {})
    command = tool_input.get("command", "")
    cwd = Path(payload.get("cwd", str(WORKSPACE_ROOT)))

    if not command.strip():
        return emit("allow", "no command")

    decision, reason = evaluate(command, cwd)
    return emit(decision, reason)


if __name__ == "__main__":
    sys.exit(main())
