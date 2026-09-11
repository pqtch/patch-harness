#!/usr/bin/env python3
"""lint_skill.py — mechanical validator for a Claude Code skill directory.

Usage:
    python3 lint_skill.py <skill-dir | skill-dir/SKILL.md> [--pool <installed-skills-dir>]

Checks (ERROR = must fix, exit 1; WARN = judgment call, exit 0):
  frontmatter   name/description present, name regex + <=64, description <=1024, no XML tags
  house rules   description carries "use when" AND "do not use" (mandatory here — sibling
                pools make pushy descriptions steal dispatch without the exclusion clause).
                SKIPPED for `disable-model-invocation: true` — a user-only skill is typed,
                never picked, so a dispatch clause on it describes nothing.
  third person  heuristic POV check on the description
  body          SKILL.md <500 lines (warn >300)
  evidence      EVIDENCE.md present with non-placeholder RED + Dispatch test sections
                (also skipped for user-only skills, same reason)
  refs          every relative .md link resolves, max one level deep from SKILL.md;
                reference files >100 lines should open with a heading/TOC
  pool overlap  (--pool) token-overlap of description vs each sibling skill's description;
                warns when two descriptions look close enough to steal each other's dispatch
                (0.35 jaccard threshold: empirically "same territory" for short texts; free,
                no-API stand-in for a semantic check)

No dependencies. Stdout only; verbose, specific messages (solve, don't punt).
"""
import re
import sys
from pathlib import Path

ERRORS, WARNINGS = [], []


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNINGS.append(msg)


def parse_frontmatter(text, label):
    """Minimal YAML-ish frontmatter parse: top-level `key: value` between --- fences."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        err(f"{label}: no frontmatter fence (--- ... ---) at top of file")
        return {}
    fields, current = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\S", line):
            k, _, v = line.partition(":")
            current = k.strip()
            fields[current] = v.strip()
        elif current and line.strip():  # folded continuation line
            fields[current] += " " + line.strip()
    return fields


def is_user_only(fm):
    """A skill the model can never self-trigger — `disable-model-invocation: true`.

    The three dispatch rules ("use when", "do not use for", EVIDENCE.md's dispatch test) all
    police one thing: being PICKED correctly out of a pool of siblings. A user-only skill is
    never picked — it is typed. Applying them anyway makes a skill carry clauses describing
    dispatch it does not do, which is decoration, and decoration in a linter teaches the
    reader to ignore it. The exemption is mechanical and narrow: it keys on a real Claude Code
    frontmatter flag, not on a judgment about what the skill is for.

    The flag is a DECLARATION, not a gate: measured 2026-09-11 on Claude Code 2.1.268, a
    session asked to invoke a skill carrying `disable-model-invocation: true` did so without
    error (docs/GUIDE.md). That does not weaken the exemption — the linter is reading the
    author's stated intent, which is exactly what a linter can read — but do not write
    anywhere that the flag stops the model, because today it does not.

    Everything else still applies — name, description length, POV, body size, links.
    """
    return str(fm.get("disable-model-invocation", "")).strip().lower() == "true"


def check_frontmatter(fm):
    name = fm.get("name", "")
    desc = fm.get("description", "")

    if not name:
        err("frontmatter: missing `name`")
    else:
        if len(name) > 64:
            err(f"name: {len(name)} chars (max 64)")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            err(f"name: '{name}' — lowercase/numbers/hyphens only")
        for reserved in ("anthropic", "claude"):
            if reserved in name:
                err(f"name: contains reserved word '{reserved}'")
        if name in {"helper", "utils", "tools", "data", "skill"}:
            err(f"name: '{name}' is vague — name the object/action")

    if not desc:
        err("frontmatter: missing `description` — the ENTIRE dispatch surface")
        return
    if len(desc) > 1024:
        err(f"description: {len(desc)} chars (max 1024)")
    if re.search(r"<[^>]+>", desc):
        err("description: contains XML/angle-bracket tags")
    low = desc.lower()
    if not is_user_only(fm):
        if "use when" not in low and "use this when" not in low:
            err('description: no "use when …" clause — dispatch depends on it')
        if "do not use" not in low and "don't use" not in low:
            err('description: no "do not use for …" clause — mandatory house rule '
                "(sibling pools; see skill-author references/description-craft.md)")
    # POV heuristic — warn, since exemplar text can legitimately quote these
    if re.search(r"^(i|you)\b|\byou can\b|\bi can\b|\bhelps you\b", low):
        warn("description: sounds first/second person — write third person "
             '("Extracts …", not "I can help you extract …")')


def check_body(skill_md, text):
    n = len(text.splitlines())
    if n >= 500:
        err(f"SKILL.md: {n} lines (hard ceiling 500) — push depth into references/")
    elif n > 300:
        warn(f"SKILL.md: {n} lines — consider splitting toward references/ before it grows")

    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL)
    root = skill_md.parent
    for link in re.findall(r"\]\(([^)#\s]+\.md)\)", body):
        if link.startswith(("http://", "https://", "/")):
            continue
        target = (root / link).resolve()
        if not target.exists():
            err(f"SKILL.md links '{link}' — file does not exist")
            continue
        try:
            depth = len(target.relative_to(root.resolve()).parts)
        except ValueError:
            warn(f"SKILL.md links '{link}' — resolves OUTSIDE the skill dir")
            continue
        # depth rule targets progressive-disclosure READING (references etc.);
        # examples/ are copy-source skeletons, exempt by design.
        if depth > 2 and target.relative_to(root.resolve()).parts[0] != "examples":
            err(f"SKILL.md links '{link}' — more than one level deep; flatten "
                "(nested refs get partial-read and silently missed)")


def check_reference_files(skill_dir):
    for ref in sorted(skill_dir.glob("references/*.md")):
        lines = ref.read_text(encoding="utf-8").splitlines()
        if len(lines) > 100:
            head = "\n".join(lines[:15])
            if not re.search(r"^#{1,3} ", head, re.MULTILINE):
                warn(f"{ref.name}: {len(lines)} lines with no heading/TOC in the first 15 — "
                     "partial reads won't see its scope")


PLACEHOLDER = re.compile(
    r"\bTODO\b|\bTBD\b|\bFIXME\b|\bN/?A\b|^\s*<.+>\s*$|\bnot yet\b|\bpending\b",
    re.IGNORECASE | re.MULTILINE,
)


def check_evidence(skill_dir, fm):
    """RED + dispatch test must leave an artifact — a gate with no record is prose.

    Mirrors the empty-report rule: degenerate content validates against any schema, so a
    section that exists but says nothing is a FAILURE, not a pass.
    """
    if is_user_only(fm):
        return  # user-only: there is no dispatch to record. See is_user_only().
    ev = skill_dir / "EVIDENCE.md"
    if not ev.exists():
        err("EVIDENCE.md: missing — RED (the observed failure, or the seed run for a "
            "commissioned skill) and the dispatch test must leave a record someone else "
            "can check. See skill-author Step 1 and Step 5.")
        return

    text = ev.read_text(encoding="utf-8")
    for heading, what in (("red", "the failure this skill was written to correct"),
                          ("dispatch test", "the plain-English request that fired it")):
        m = re.search(rf"^#{{1,3}}\s*{heading}\b.*$", text, re.IGNORECASE | re.MULTILINE)
        if not m:
            err(f"EVIDENCE.md: no `## {heading.title()}` section — record {what}")
            continue
        rest = text[m.end():]
        nxt = re.search(r"^#{1,3}\s", rest, re.MULTILINE)
        section = (rest[:nxt.start()] if nxt else rest).strip()
        section = "\n".join(ln for ln in section.splitlines()
                            if not ln.strip().startswith(("<!--", "-->")))
        if len(section.strip()) < 40:
            err(f"EVIDENCE.md: `{heading.title()}` section is empty or near-empty — "
                "an unrun gate recorded as run is worse than an admitted gap")
        elif PLACEHOLDER.search(section):
            err(f"EVIDENCE.md: `{heading.title()}` section still holds a placeholder "
                "(TODO/TBD/pending/<…>) — write what actually happened, or say plainly "
                "that it has not been run and leave the skill unfinished")


def tokenize(s):
    stop = {"a", "an", "and", "the", "for", "of", "to", "or", "in", "on", "with", "not",
            "use", "when", "do", "this", "is", "are", "files", "file", "user", "mentions"}
    return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in stop and len(t) > 2}


def check_pool_overlap(fm, skill_dir, pool_dir):
    mine = tokenize(fm.get("description", ""))
    if not mine:
        return
    for sibling in sorted(Path(pool_dir).rglob("SKILL.md")):
        if sibling.resolve() == (skill_dir / "SKILL.md").resolve():
            continue
        sib_text = sibling.read_text(encoding="utf-8")
        if not sib_text.startswith("---"):
            continue  # dispatch-inert stub (PROPOSED convention) — not in the pool's surface
        sib_fm = parse_frontmatter(sib_text, str(sibling))
        theirs = tokenize(sib_fm.get("description", ""))
        if not theirs:
            continue
        jac = len(mine & theirs) / len(mine | theirs)
        if jac >= 0.35:
            warn(f"description overlaps '{sib_fm.get('name', sibling.parent.name)}' "
                 f"(jaccard {jac:.2f}) — sibling dispatch-stealing risk: sharpen both "
                 'differentiators + "do not use for" clauses, or consolidate')


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    skill_dir = Path(args[0])
    # Accept the SKILL.md itself as well as its directory. Pointing the linter at the file is
    # the first thing anyone tries, and the old failure was "…/SKILL.md/SKILL.md not found".
    if skill_dir.name == "SKILL.md":
        skill_dir = skill_dir.parent
    pool_dir = args[args.index("--pool") + 1] if "--pool" in args else None

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: {skill_md} not found")
        sys.exit(1)

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text, "SKILL.md")
    check_frontmatter(fm)
    check_body(skill_md, text)
    check_reference_files(skill_dir)
    check_evidence(skill_dir, fm)
    if pool_dir:
        check_pool_overlap(fm, skill_dir, pool_dir)

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
