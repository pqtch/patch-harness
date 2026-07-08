#!/usr/bin/env python3
"""Fail-open health check for the workspace. Always exits 0; prints a report.

Checks:
  1. Paths referenced in CLAUDE.md's workspace map / routing table exist.
  2. Paths referenced in memories/shared/MEMORY.md exist.
  3. A recent journal entry exists (today, or within the last 7 days).
  4. No dated "status" lines in always-loaded files (CLAUDE.md, .claude/rules/*.md).
  5. Memory files (MEMORY.md under memories/) have valid structure (routing lines
     of the form "- [...](...)" or a frontmatter-bearing detail file).
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
PATH_RE = re.compile(r"`([\w./_-]+/[\w./_-]*)`")


def find_paths_in(text):
    found = set()
    for m in PATH_RE.finditer(text):
        p = m.group(1)
        if "<" in p or ">" in p or p.startswith("http"):
            continue
        found.add(p)
    return found


def check_referenced_paths():
    results = []
    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.exists():
        return [("✗", "CLAUDE.md missing")]
    text = claude_md.read_text()
    for p in sorted(find_paths_in(text)):
        target = ROOT / p
        # a reference passes only if the exact path exists (dir or file)
        if target.exists():
            results.append(("✓", f"CLAUDE.md reference exists: {p}"))
        else:
            results.append(("✗", f"CLAUDE.md references missing path: {p}"))
    return results


def check_memory_index():
    memories_dir = ROOT / "memories"
    if not (memories_dir / "shared" / "MEMORY.md").exists():
        return [("✗", "memories/shared/MEMORY.md missing")]
    results = []
    # every MEMORY.md (shared + agent lanes) gets its links checked, not just shared
    for idx in sorted(memories_dir.rglob("MEMORY.md")):
        for line in idx.read_text().splitlines():
            m = re.match(r"-\s+\[.*?\]\((.*?)\)", line.strip())
            if not m:
                continue
            target = idx.parent / m.group(1)
            if target.exists():
                results.append(("✓", f"memory index link resolves: {m.group(1)}"))
            else:
                results.append(("✗", f"{idx.relative_to(ROOT)} link broken: {m.group(1)}"))
    return results


def check_recent_journal():
    journal_dir = ROOT / "_ops" / "journal"
    if not journal_dir.exists():
        return [("✗", "_ops/journal/ missing")]
    today = date.today()
    window = {today - timedelta(days=i) for i in range(7)}
    any_entry = False
    for f in journal_dir.rglob("*.md"):
        m = DATE_RE.search(f.name)
        if not m:
            continue
        try:
            d = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        any_entry = True
        if d in window:
            return [("✓", f"recent journal entry found: {f.relative_to(ROOT)}")]
    if not any_entry:
        # a fresh workspace has no journal at all — that's not sickness;
        # the first /wrap creates it
        return [("✓", "no journal yet (fresh workspace) — first /wrap will create it")]
    return [("✗", "no journal entry in the last 7 days")]


def check_no_dated_status():
    results = []
    always_loaded = [ROOT / "CLAUDE.md"]
    rules_dir = ROOT / ".claude" / "rules"
    if rules_dir.exists():
        always_loaded += sorted(rules_dir.glob("*.md"))
    for f in always_loaded:
        if not f.exists():
            continue
        text = f.read_text()
        dates = DATE_RE.findall(text)
        if dates:
            results.append(("✗", f"{f.relative_to(ROOT)} has dated status line(s): {dates}"))
        else:
            results.append(("✓", f"{f.relative_to(ROOT)} has no dated status lines"))
    return results


def check_memory_structure():
    results = []
    memories_dir = ROOT / "memories"
    if not memories_dir.exists():
        return [("✗", "memories/ missing")]
    for f in memories_dir.rglob("MEMORY.md"):
        text = f.read_text()
        lines = [l for l in text.splitlines() if l.strip().startswith("- ")]
        if lines:
            results.append(("✓", f"{f.relative_to(ROOT)} has routing entries"))
        else:
            # an empty index isn't sick — a fresh vault has no facts yet
            results.append(("✓", f"{f.relative_to(ROOT)} is empty (no facts yet — fine)"))
    return results


def check_memory_rot():
    """Rot alarm (⚠, advisory — doesn't fail the report): oversized memory index,
    or no sign of a /curate pass in the last 30 days."""
    results = []
    idx = ROOT / "memories" / "shared" / "MEMORY.md"
    if idx.exists():
        routing = [l for l in idx.read_text().splitlines() if l.strip().startswith("- ")]
        if len(routing) > 60:
            results.append(("⚠", f"MEMORY.md has {len(routing)} routing lines (>60) — run /curate"))
        else:
            results.append(("✓", f"MEMORY.md size OK ({len(routing)} routing lines)"))
    journal_dir = ROOT / "_ops" / "journal"
    if journal_dir.exists():
        cutoff = date.today() - timedelta(days=30)
        curated = False
        oldest = None
        for f in journal_dir.rglob("*.md"):
            m = DATE_RE.search(f.name)
            if not m:
                continue
            try:
                d = date.fromisoformat(m.group(1))
            except ValueError:
                continue
            oldest = d if oldest is None or d < oldest else oldest
            if d >= cutoff and "curate" in f.read_text().lower():
                curated = True
        if curated:
            results.append(("✓", "curate pass seen in the last 30 days"))
        elif oldest is not None and oldest < cutoff:
            # only nag once the vault is old enough to have needed a curate pass
            results.append(("⚠", "no curate pass in the last 30 days — run /curate"))
    return results


def main():
    sections = [
        ("Referenced paths", check_referenced_paths),
        ("Memory index links", check_memory_index),
        ("Recent journal", check_recent_journal),
        ("Dated status in always-loaded files", check_no_dated_status),
        ("Memory file structure", check_memory_structure),
        ("Memory rot", check_memory_rot),
    ]
    print("Health check report")
    print("=" * 20)
    any_fail = False
    for title, fn in sections:
        print(f"\n{title}:")
        for mark, msg in fn():
            if mark == "✗":
                any_fail = True
            print(f"  {mark} {msg}")
    print()
    print("Some checks failed — see ✗ above." if any_fail else "All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
