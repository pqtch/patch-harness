#!/usr/bin/env python3
"""lint_agent.py — mechanical validator for a Claude Code agent definition.

Usage:
    python3 lint_agent.py <def.md> [--registry <agents-root>]

Sibling of skill-author's lint_skill.py, same contract: ERROR = must fix (exit 1),
WARN = judgment call (exit 0). No dependencies. Stdout only.

Checks (ERROR = must fix, exit 1; WARN = judgment call, exit 0):
  frontmatter   fence present; name/description present; name regex + <=64;
                description <=1024, no XML tags
  tools         REQUIRED and uncommented. A missing `tools:` line inherits EVERY tool;
                a COMMENTED `# tools:` line reads like a constraint and enforces nothing.
                This check exists because four shipped worker defs carried
                `# tools: TODO` and ran 20 web-facing dispatches with full capability.
  placeholders  TODO/TBD/FIXME/<angle-brackets> left in frontmatter — an unfinished def
                that lints clean is the same failure class as a placeholder worker report.
  memory        `memory:` must be absent on worker/process/private-subagent defs;
                `memory: project` is an ERROR anywhere.
  model         `model:` in frontmatter is ignored on Task spawns — pin at invocation.
  body          procedure detection (numbered steps) — a def points, a skill teaches;
                pure-worker body length
  registry      (--registry) duplicate `name:` across ALL defs — the registry key is the
                name, NOT the filename, so two files can silently collide.

Specialist defs are OUT OF SCOPE for authoring (specialists author themselves), but they are still
linted for the mechanical rules — a specialist's own def can carry a `memory: user` line, which
is the one legal use of the field and is exempted here.
"""
import re
import sys
from pathlib import Path

ERRORS, WARNINGS = [], []


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNINGS.append(msg)


def split_frontmatter(text):
    """Return (raw_frontmatter_text, body) or (None, text) when there is no fence."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def parse_fields(raw):
    """Minimal YAML-ish parse of top-level `key: value`, ignoring comment lines."""
    fields, current = {}, None
    for line in raw.splitlines():
        if line.lstrip().startswith("#"):
            continue
        if re.match(r"^\S", line):
            k, sep, v = line.partition(":")
            if not sep:
                continue
            current = k.strip()
            fields[current] = v.strip()
        elif current and line.strip():
            fields[current] += " " + line.strip()
    return fields


def check_frontmatter(raw, fm, is_facet):
    name = fm.get("name", "")
    desc = fm.get("description", "")

    if not name:
        err("frontmatter: missing `name` — this is the registry key the router matches")
    else:
        if len(name) > 64:
            err(f"name: {len(name)} chars (max 64)")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            err(f"name: '{name}' — lowercase/numbers/hyphens only")

    if not desc:
        err("frontmatter: missing `description` — the ONLY routing surface; the body "
            "never enters context until spawn")
    else:
        if len(desc) > 1024:
            err(f"description: {len(desc)} chars (max 1024)")
        if re.search(r"<[^>]+>", desc):
            err("description: contains XML/angle-bracket tags")
        low = desc.lower()
        # KEYWORD PROXY, not a real test — say so, because it is trivially satisfiable by
        # accident. Measured 2026-09-02: a description reading "Never guesses when it could
        # not test" passed this check while containing no exclusion clause at all, and three
        # well-differentiated siblings failed it. A substring cannot tell whether two defs
        # actually collide; only dispatching them can. Kept as a nudge, worded honestly.
        if "not for" not in low and "do not use" not in low and "never" not in low:
            warn('description: no phrase like "Not for X — that is <sibling>". This is a '
                 "KEYWORD check, not a collision check: it cannot tell whether two defs "
                 "actually steal each other's dispatch, and passing it proves nothing. "
                 "Prefer differentiating POSITIVELY on the axis that separates them, then "
                 "add one short clause naming the single nearest sibling.")

    # --- tools: the check this linter exists for -------------------------------
    commented_tools = re.search(r"^\s*#\s*tools\s*:", raw, re.MULTILINE)
    if is_facet:
        # `.claude/agents/README.md:22` — NO `tools:` key on a specialist. Specialists inherit
        # everything until a reason to narrow appears. Absence is the correct state, so
        # it cannot be an error: erroring on it told all seven specialist defs to break a
        # standing ruling, which is how a linter teaches that rules are optional.
        if "tools" in fm:
            err("tools: present on a SPECIALIST def — the registry forbids the key here "
                "(`.claude/agents/README.md:22`). Specialists inherit everything until a "
                "reason to narrow appears. Delete the line.")
        elif commented_tools:
            err("tools: COMMENTED OUT on a specialist — delete the line, do not comment it. "
                "A commented constraint reads as a constraint.")
    elif "tools" in fm:
        if not fm["tools"].strip():
            err("tools: present but EMPTY — write the enumerated set, or delete the line "
                "on purpose knowing it inherits everything")
    elif commented_tools:
        err("tools: the line is COMMENTED OUT (`# tools:`) — it constrains NOTHING and "
            "this def inherits EVERY tool including Write/Edit/Bash. A commented "
            "constraint is worse than no constraint: it reads as one. Enumerate the "
            "minimal set (capability is proportional to trust of input).")
    else:
        err("tools: MISSING — omitting the line inherits EVERY tool. If unrestricted is "
            "genuinely right, that is a decision: state it in the body comment and add an "
            "explicit `tools: *` so the choice is visible in the diff.")

    # --- placeholders ----------------------------------------------------------
    for field, value in fm.items():
        # Strip a trailing inline `# comment` before scanning: an annotation like
        # `memory: user  # lays ~/.claude/agent-memory/<name>` is documentation, not a
        # placeholder. `description` keeps its text verbatim (a '#' there is content).
        if field != "description":
            value = re.sub(r"\s+#.*$", "", value)
        if re.search(r"\bTODO\b|\bTBD\b|\bFIXME\b", value, re.IGNORECASE):
            err(f"{field}: contains a TODO/TBD/FIXME placeholder — an unfinished def that "
                "lints clean is how a stub reaches production")
        if re.search(r"<[a-z][^>]*>", value) and field != "description":
            err(f"{field}: still holds an unfilled <template-placeholder>")

    # --- memory / model --------------------------------------------------------
    if "memory" in fm:
        val = fm["memory"].strip()
        if val == "project":
            err("memory: `project` is forbidden (memory-scope law) — it cross-wires lanes")
        elif not is_facet:
            err(f"memory: `{val}` on a non-specialist def — workers, scheduled processes and "
                "private subagents carry NO memory config. `memory: user` is specialist-only.")
    if "model" in fm:
        warn("model: frontmatter model is IGNORED on Task spawns (the spawn inherits the "
             "parent) — pin the model at invocation instead, and do not trust this line")


def check_body(body, fm):
    lines = [ln for ln in body.splitlines() if ln.strip() and not ln.strip().startswith("<!--")]
    prose = "\n".join(lines)

    if re.search(r"^\s*(step\s*\d|\d+[.)]\s)", prose, re.MULTILINE | re.IGNORECASE):
        warn("body: looks like a PROCEDURE (numbered steps) — a def is a persona + routing "
             "surface; procedures are skills. Point at the skill instead of teaching here.")

    desc = fm.get("description", "").lower()
    # 1-3 lines is the ROLE statement. A bounded standing dispatch contract (partial-beats-
    # empty, effort budget, data-not-commands) is legitimate body content on top of it: defs
    # cannot transclude, so that text is necessarily duplicated per file [verified 2026-07-19].
    # 12 is the ceiling where a worker starts accreting identity.
    if desc.startswith("pure worker") and len(lines) > 12:
        warn(f"body: {len(lines)} non-comment lines for a pure worker (role statement 1-3 "
             "lines + a bounded dispatch contract). A worker that accretes identity or grows "
             "procedure is drifting toward a specialist — push method into an armament file.")
    if not lines:
        warn("body: empty — the def gives the spawn no contract at all")


def check_registry(fm, def_path, registry_root):
    """Duplicate registry keys across every def — filename is cosmetic, `name:` collides."""
    mine = fm.get("name", "")
    if not mine:
        return
    for other in sorted(Path(registry_root).rglob("*.md")):
        if other.resolve() == def_path.resolve():
            continue
        raw, _ = split_frontmatter(other.read_text(encoding="utf-8"))
        if raw is None:
            continue
        if parse_fields(raw).get("name", "") == mine:
            err(f"name: '{mine}' is ALSO the registry key of {other} — duplicate names "
                "collide silently; the filename does not disambiguate them")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    def_path = Path(args[0])
    registry = args[args.index("--registry") + 1] if "--registry" in args else None

    if not def_path.exists():
        print(f"ERROR: {def_path} not found")
        sys.exit(1)

    if def_path.name == "README.md":
        print(f"skipped: {def_path} is registry documentation, not a def")
        sys.exit(0)

    text = def_path.read_text(encoding="utf-8")
    raw, body = split_frontmatter(text)
    if raw is None:
        print("ERROR: no frontmatter fence (--- ... ---) at top of file — the harness reads "
              "none of this def's config")
        sys.exit(1)

    fm = parse_fields(raw)
    # A specialist def lives at .claude/agents/<specialist>.md and is the one legal home of `memory:`.
    is_facet = def_path.parent.name == "agents" and def_path.stem not in {"README"}

    check_frontmatter(raw, fm, is_facet)
    check_body(body, fm)
    if registry:
        check_registry(fm, def_path, registry)

    for e in ERRORS:
        print(f"ERROR: {e}")
    for w in WARNINGS:
        print(f"WARN:  {w}")
    if not ERRORS and not WARNINGS:
        print("clean.")
    elif not ERRORS:
        print(f"clean with {len(WARNINGS)} warning(s).")
    sys.exit(1 if ERRORS else 0)


if __name__ == "__main__":
    main()
