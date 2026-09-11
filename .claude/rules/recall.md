# recall — question → command

Every file here follows a standard, so a question maps to a command. Run it; do not guess.

| Question | Command |
|---|---|
| Do we already know about X? (memory, inbox, journal, notes) | `check-recall X` |
| When did we work on X, and as whom? (transcripts) | `check-sessions X` |
| Where is the file or directory named X? | `check-where 'X*'` |
| Which index points at X? | `check-rows X` |
| What was I last doing, as this specialist? | injected at boot; also `.claude/agent-memory/<specialist>/LAST.md` |

All in `~/workspace/_ops/bin/`, on PATH. Each script's header says exactly what it searches.
