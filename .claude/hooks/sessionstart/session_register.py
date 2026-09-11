#!/usr/bin/env python3
"""session_register.py — SessionStart. Appends one line to the session->specialist sidecar.

Transcripts do not record which --agent a session ran as (checked 2026-09-10, Claude Code 2.1.268:
no agent field on any transcript line). The SessionStart payload does carry it, as
`agent_type` — harness-set, not inheritable (see thread_delivery.py for why the env var is
never trusted). So this hook is the only place the join can be made, and check-sessions,
check-digest and the LAST.md brief all read it.

Line: session_id <TAB> specialist-or-blank <TAB> ISO time <TAB> cwd <TAB> source
Sidecar: <config dir>/session-specialists.tsv — tracked, so it travels with the transcripts.
Fails open; appends nothing on any doubt.
"""
import json, os, sys, datetime

def main():
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return
    if not isinstance(data, dict) or not data.get("session_id"):
        return
    agent = data.get("agent_type") or "blank"
    if not all(c.isalnum() or c in "._-" for c in agent):
        return
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    cfg = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(root, ".claude-config")
    # Create the dir rather than fail open into silence: if it is absent the sidecar is never
    # written, and check-sessions, check-digest and the LAST brief all go dark with no error
    # anywhere. Creating one empty directory is the cheaper side of that trade.
    try:
        os.makedirs(cfg, exist_ok=True)
    except OSError:
        return
    path = os.path.join(cfg, "session-specialists.tsv")
    line = "\t".join([data["session_id"], agent,
                      datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      data.get("cwd") or root, data.get("source") or ""]) + "\n"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"session_register: {exc}", file=sys.stderr)
    sys.exit(0)
