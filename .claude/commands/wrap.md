---
description: Close out a session — reconcile CLAUDE.md and STICKY.md against real state, retire finished to-dos, commit with a Session trailer, run the checks, and PUSH.
---

# /wrap

1. Read the cwd `CLAUDE.md`, its `.claude/STICKY.md`, and the `CLAUDE.md` of any sub-directory
   this session actually touched.
2. Verify their content and to-dos against the real state produced by this session's work.
3. Use judgement to accomplish the following checks:

| If | Then |
| --- | ---|
| conflicting info | trace it to the primary source and fix the incorrect copy |
| a to-do is done | cross it off; a to-do that outlived the session moves to STICKY |
| a `CLAUDE.md` length flag | replace content with file pointers to reduce token cost |

4. Commit all work from this session. Every commit carries a `Session: <id>` trailer, and the
   last one is the closing marker — its absence is the signal that a session was never
   wrapped.
5. Run `~/workspace/_ops/bin/check-selftest` — it plants the failure every guard refuses and
   must report 0 failed; a failure means a guard is silently not guarding, and the wrap stops
   until it is understood. Then run `~/workspace/_ops/bin/check-pointers`. It is a warning, not a gate — act on what it finds:
   repoint the unambiguous typo/rename dead pointers it names, and leave anything requiring
   judgment (a genuinely missing file, a historical record quoting an old path) listed rather
   than guessed at. (`check-types` and the gitlink guard run themselves, on every commit.)

6. **Push.** A wrap that does not push has not finished. The remote is the
   only thing that makes the work exist on more than one machine, and the failure mode is
   silent — the session looks complete, the tree looks clean, and the work is stranded.
   Before this rule existed, ten commits once sat unpushed at once.

   ```sh
   git -C ~/workspace push
   ```

   If the push is rejected because the remote moved, **stop and say so.** Do not force, and
   do not resolve a divergence at the end of a session when attention is lowest.
