# projects/ — committed work

One folder per project. A project is where knowledge about that project lives; this index
only points. To create one, use the `project-author` skill (it loads on touching anything
under `projects/`).

## Index
| Project | Kind | Clone lives at | Remote |
|---|---|---|---|
| *(none yet)* | | | |

Two kinds of project. A **plain folder** is tracked by this repo. A **shelled repo** is an
external repository with its own `.git`, sitting one level down inside a folder this
workspace owns:

```
projects/<name>/              <- this workspace owns it. Private notes about the repo go HERE.
projects/<name>/<name>-repo/  <- the clone. Gitignored, wholesale.
```

The shell exists so notes about a shared repo are never committed *into* that repo. **Write
the ignore line before the clone** — a clone into a path with no ignore line is the silent
failure: this repo starts tracking its contents. The remote name need not match the
directory name; the table's last column is where that is recorded.

## Why wholesale, and what it cost
Measured in throwaway repos rather than reasoned about:

| `.gitignore` form | `git add -A` result |
|---|---|
| `<repo>/*` + `!<repo>/.claude/` | **gitlink created** (mode 160000) |
| `<repo>/*` alone, no negation | **gitlink created** |
| `<repo>/` — the directory | **clean; git never walks in** |

`dir/*` excludes a directory's *children*, never the directory. Git still walks in, finds the
nested `.git`, and records a **gitlink**: a submodule-shaped pointer that pins a SHA into the
umbrella without being a submodule, so nobody can clone the contents back. No git config turns
this into an error — `advice.addEmbeddedRepo` and `--no-warn-embedded-repo` govern the
warning only. The gitlink guard (`.claude/hooks/pretooluse/gitlink_guard.sh` and the
`pre-commit` that `setup.sh` installs) catches the case where the ignore line was forgotten.

**The cost, accepted knowingly:** a gitignored directory is invisible to skill discovery, so
the clone's own `.claude/` never loads here. Put the capability in the shell above it — the
shell's `.claude/` is this workspace's and loads; the clone's is for whoever clones that repo.
