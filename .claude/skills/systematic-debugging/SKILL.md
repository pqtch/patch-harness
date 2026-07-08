---
name: systematic-debugging
description: Use when something is broken — code or the workspace itself — and the fix isn't obvious. Reproduce first, one hypothesis at a time.
---

# Systematic debugging

1. **Reproduce first.** Don't theorize from a description alone — see the failure
   yourself (run the command, read the actual error, check the actual file state).
2. **One hypothesis at a time.** State it explicitly, predict what you'd see if it's
   true, then check. Don't change multiple things and see what sticks.
3. **After 3 failed hypotheses, stop and widen the search** instead of trying a 4th
   narrow guess — re-read the surrounding code/config, check assumptions you took for
   granted, ask the user for anything you might be missing.
4. **State evidence, not guesses.** "The log shows X at line Y, so Z" beats "probably
   Z." If you're not sure, say so.
5. Once fixed, verify the original repro no longer fails — see the `verification`
   skill.
