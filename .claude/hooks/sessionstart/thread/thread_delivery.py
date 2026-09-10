#!/usr/bin/env python3
"""thread_delivery.py — SessionStart hook. Hands the baton to the session that picks it up.

/thread writes `thread.<agent>.md` into the project directory a session was working in.
This hook finds that file at the next boot of the same specialist, injects it, and DELETES it.
A consumed baton left on disk lies: its existence means a handoff is pending
(`docs/GUIDE.md`, "Where state lives"). Committed work is the source of
truth, so deleting loses nothing.

MEASURED 2026-08-16, Claude Code 2.1.233 — the env and stdin a SessionStart hook process actually sees
(clean room: `env -u CLAUDE_CODE_AGENT -u CLAUDE_CODE_SESSION_ID -u CLAUDE_PROJECT_DIR claude
--agent <name> --model sonnet -p ...`, with a no-`--agent` control and a deliberately
CONTAMINATED control):
  * stdin JSON carries: session_id, transcript_path, cwd, hook_event_name, source, and
    `agent_type` — the agent name, present ONLY when `--agent` was passed. Harness-set per
    session; it cannot be inherited from a parent process. **This is the authoritative
    identity source and is checked first.**
  * CLAUDE_CODE_AGENT **is** set in the hook process, to the `--agent` value — but it is an
    ordinary exported env var and is **INHERITED, not reset**. Control C: launching a BLANK
    `claude` (no `--agent`) from inside a session whose env already had
    CLAUDE_CODE_AGENT=center gave the child's hook CLAUDE_CODE_AGENT=center while stdin
    agent_type was correctly absent. CONSEQUENCE: trusting the env var first would hand the center's
    baton to a blank session and delete it. It is used only as a last resort, when stdin
    carried no parseable JSON at all — i.e. when the harness said nothing. This INVALIDATES
    the original spec line "agent name := CLAUDE_CODE_AGENT"; the var reaches the hook, but
    reaching is not the same as being true.
  * The same measurement is why the `ws` launcher exports NO identity var of its own: an
    exported identity propagates down every child process tree (that is how the center's identity
    leaked into dispatched sessions on 2026-07-21). WS_AGENT below is an explicit MANUAL
    override for fixtures and debugging — nothing sets it automatically.
  * CLAUDE_PROJECT_DIR **is** set, to the directory `claude` was launched from. That is the
    workspace root under the `ws` launcher, which always `cd $ROOT` first.
  * `source` is one of startup | resume | compact. This hook does not discriminate: a baton
    that survives to a compact boot is still an undelivered baton.
  * SessionStart does NOT fire for in-process Task subagents — only real sessions
    (interactive or headless `-p`). Subagents never consume a baton.

FAIL OPEN, always. Hook failures are invisible to the model, and a boot hook that dies must
never brick a session. Every path here ends in exit 0; diagnostics go to stderr only.
"""
import json
import os
import re
import sys

PRUNE_DIRS = {".git", "node_modules"}
# Molds are not batons. `.claude/templates/THREAD.tmp.md` is not named `thread.<agent>.md`
# today, but the templates dir is pruned so a future rename can never make a mold deliverable.
PRUNE_UNDER_CLAUDE = {"templates"}

SAFE_AGENT = re.compile(r"^[A-Za-z0-9._-]+$")


def read_stdin_json():
    """stdin → (dict, had_payload). Empty, truncated or non-JSON input is ({}, False).

    `had_payload` is the load-bearing half: it distinguishes "the harness told us this is a
    blank session" from "we were handed nothing and know nothing".
    """
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}, False
    if not raw or not raw.strip():
        return {}, False
    try:
        data = json.loads(raw)
    except Exception:
        return {}, False
    if not isinstance(data, dict):
        return {}, False
    return data, True


def resolve_agent(data: dict, had_payload: bool) -> str:
    """WS_AGENT (explicit manual override) → stdin agent_type (authoritative). Nothing else.

    CLAUDE_CODE_AGENT is deliberately NOT a fallback, though it is present in the environment.
    It is inherited rather than reset, so it is a *guess* about identity, and this hook's one
    irreversible act — deleting a baton — must never run on a guess.

    AMENDED 2026-08-16 (integrating). The build measured the env var reaching the hook
    and used it when stdin carried no parseable payload. Verified refusal case: garbage stdin
    plus an inherited CLAUDE_CODE_AGENT=<other> DELIVERED AND DELETED another specialist's baton — the wrong
    session consuming a handoff, which is the 2026-07-21 identity-leak failure exactly. The
    losses are asymmetric: an undelivered baton is delayed and still on disk, a wrongly
    consumed one is destroyed silently. An undelivered baton is recoverable and a destroyed one is not, so the tie goes to
    not-deleting. In practice this costs nothing — a real SessionStart always carries a
    payload, so the removed branch only ever fired in the degraded case where it was unsafe.
    """
    claims = [os.environ.get("WS_AGENT")]
    if had_payload:
        claims.append(data.get("agent_type"))
    for claim in claims:
        if claim and isinstance(claim, str) and SAFE_AGENT.match(claim.strip()):
            return claim.strip()
    return ""


def resolve_root(data: dict) -> str:
    """CLAUDE_PROJECT_DIR → stdin cwd → process cwd. First one that is a real directory."""
    for cand in (os.environ.get("CLAUDE_PROJECT_DIR"), data.get("cwd")):
        if cand and isinstance(cand, str) and os.path.isdir(cand):
            return cand
    return os.getcwd()


def find_batons(root: str, filename: str) -> list:
    """Every `thread.<agent>.md` under root, sorted. Usually 0 or 1."""
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in PRUNE_DIRS
            and not (os.path.basename(dirpath) == ".claude" and d in PRUNE_UNDER_CLAUDE)
        ]
        if filename in filenames:
            hits.append(os.path.join(dirpath, filename))
    return sorted(hits)


def main() -> None:
    data, had_payload = read_stdin_json()
    agent = resolve_agent(data, had_payload)
    if not agent:
        return

    root = resolve_root(data)
    parts = []
    for path in find_batons(root, f"thread.{agent}.md"):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                body = fh.read()
        except OSError as exc:
            print(f"thread_delivery: unreadable baton {path}: {exc}", file=sys.stderr)
            continue
        parts.append(f"## Baton: {path}\n\n{body.rstrip()}")
        # Delete AFTER a successful read. A baton that could not be read is left in place.
        try:
            os.remove(path)
        except OSError as exc:
            print(f"thread_delivery: could not delete {path}: {exc}", file=sys.stderr)

    if not parts:
        return  # No baton, no output. Silence is the normal case.

    text = (
        "A thread baton was waiting for you and has been delivered below. The file has "
        "already been deleted — do not look for it, and do not delete it again. It is a "
        "handoff, not a record: committed work is the source of truth.\n\n"
        + "\n\n".join(parts)
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": text,
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — fail open is the whole contract
        print(f"thread_delivery: {exc}", file=sys.stderr)
    sys.exit(0)
