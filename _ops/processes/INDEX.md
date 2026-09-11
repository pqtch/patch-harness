# _ops/processes/ — where scheduled processes run from

`check-digest` launches its headless model call from this directory: it is inside the repo,
but `settings.json` is read for the launch directory only and does not cascade from a
subdirectory, so the workspace's hooks never load for that child — it cannot consume a
thread or register itself as a session (measured, Claude Code 2.1.268). Any other scheduled
process — cron, a transcript sweep — runs from here for the same reason.

## Index
*(empty — processes write elsewhere; this is only where they stand)*
