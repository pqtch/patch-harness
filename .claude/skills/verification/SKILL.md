---
name: verification
description: Use before claiming any task is done — run it, read the output, and state what actually passed instead of assuming success.
---

# Verification

"Done" means verified, not "should work."

1. Run the actual test, command, or flow the change affects — don't infer success
   from reading the diff.
2. Read the real output. A clean exit code isn't enough if the output shows wrong
   behavior.
3. State plainly what you verified and what you didn't ("tests pass; did not check
   the UI live") rather than implying full coverage.
4. If verification isn't possible in this environment, say so instead of claiming
   success anyway.
