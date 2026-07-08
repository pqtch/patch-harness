---
description: Run the health check script and report; act on any failing check
---

Run `.claude/scripts/health_check.py` and show the report as-is. For any `✗`, explain
what it means and either fix it directly or ask the user how they want to handle it.
The script fails open (always exits 0) — a `✗` is a signal to act on, not an error to
suppress.
