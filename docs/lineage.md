# Lineage

## v1.0 — the ICM starter kit
The first version of this repository (tag-less; inspectable at commit `61f91eb`) was a
public starter kit built on the **Interpretable Context Methodology** (ICM),
https://arxiv.org/abs/2603.16021 — a PARA-shaped workspace with a shared memory file, a
health check, an `rm` guard, nine skills, and a setup interview that personalized the tree.
It was used by people other than its author, which is the bar this version keeps.

Nothing carries forward from it but `LICENSE` and the git history. The ICM debt is real and
this file is where it is paid: the one-file-per-fact rule, the dated journal as the history
surface, and "the agent onboards itself" are ICM's, and they survive here in different clothes.

## v2 — the extracted boilerplate
This version is the generalized mechanism of a private workspace that ran from the v1.0 kit
and then outgrew it: the same tree its author uses daily, with every piece of content
removed and every measurement kept. The test each file passed on the way in: *would this be
true for someone who is not the author?*

**Kept from the private tree:** the routing shape, the rules, the guard ladder, the
memory system and its checks, the templates, the hooks, the launcher, the session lifecycle
(`/thread`, `/wrap`, the `Session:` trailer), three specialist roles and four workers, the
author skills, and the measured harness behaviour in `GUIDE.md` and `harness-hooks.md`.

**Dropped as content:** the author's name and vocabulary, the specialists' names and
identity memories, every project, the journal, the notebook, a shared identity text, and a cognitive
profile. The specialists that ship are roles, and they name themselves.

**Exists upstream, not here — held deliberately, not forgotten:**
- **A maintenance pipeline** that runs unattended between sessions: digests transcripts and
  per-session diffs into the journal, checks the tree, and proposes rather than acts. It
  destroyed a live edit once (`incidents.md`) and is held until its write-set discipline is
  proven from the outside.
- **Its ledger** — one append-only record outside git, written by every check. Coupled to
  the pipeline, so held with it; the shipped checks print to stderr instead.
- **A model guard** — a PreToolUse hook that refuses spawning a subagent on a particular
  model. Its reason is specific to the upstream tree's history and would not generalize.
- **The leak guard's wordlist.** The mechanism ships as `check-leak`; the words are the
  author's names and projects, and shipping them would ship what the guard prevents.
- **A case study** of the nine months that produced this shape. Deferred; needs writing.

## What this repository is for
Three things, in order: to demonstrate an understanding of terminal agents and Claude Code;
to demonstrate architecture — context management above all; and to be usable by someone who
is not an expert. Where the three conflict, the third wins, because a boilerplate nobody can
run demonstrates nothing.
