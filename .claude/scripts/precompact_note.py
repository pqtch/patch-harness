#!/usr/bin/env python3
"""PreCompact hook: leave a trail before context compaction.

Compaction summarizes the conversation and details get lost. This hook (fail-open,
always exits 0) appends a timestamped marker to today's journal so the loss point is
visible — the marker itself carries the recovery instruction, since the NEXT reader of
the journal is the one who needs it (hook stdout is not guaranteed to survive into
post-compaction context).
"""
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    now = datetime.now()
    journal = ROOT / "_ops" / "journal" / now.strftime("%Y-%m") / f"{now.strftime('%Y-%m-%d')}.md"
    try:
        journal.parent.mkdir(parents=True, exist_ok=True)
        with journal.open("a") as f:
            f.write(
                f"\n> [!compaction] {now.strftime('%H:%M')} — context compacted here; "
                "detail before this point survives only in this journal. Reader: if the "
                "entries above don't cover current in-flight work, /checkpoint it now.\n"
            )
    except OSError:
        pass  # fail-open: never block compaction over a journal write

    print(
        "Context is being compacted. Anything in flight that isn't written down will "
        "blur — after compaction, re-read today's journal and /checkpoint the current "
        "task state if it isn't already there."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
