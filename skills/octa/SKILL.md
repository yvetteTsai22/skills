---
name: octa
description: Octa — autonomous backlog coordinator. Scans a repo's Linear project, triages tickets (small → Orca worker, large → wayfinder-crew map, decisions → a kept-open Orca worktree that waits for the human), dispatches workers on any coding harness (claude, codex, ...), and merges on green only in repos that opt in via AUTONOMY.md. Run once with /octa, or on a schedule with /loop /octa.
argument-hint: "[repo path] [dry-run | init]"
---

# Octa

An octopus keeps most of its neurons in its arms: each arm acts on its own, the brain only coordinates.
Octa works the same way. **Arms** are Orca workers, one worktree per ticket. **Octa** (this session) only
triages, dispatches, gates merges, and calls the human when a decision is theirs.

Harness-neutral: this file lives in `~/.agents/skills/octa/` (symlinked into `~/.claude/skills/`).
Use only plain shell, `gh`, the Orca CLI, and the Linear MCP. Nothing here needs a Claude-only feature,
except the optional `/loop` and push-notification conveniences noted below.

## 0. Gate: is this repo enrolled?

Read `AUTONOMY.md` at the repo root. **No file → stop**, tell the user in one line, do nothing,
and offer `/octa init` to enrol the repo.

`init` argument: skip the sweep and follow `init.md` (wizard that writes `AUTONOMY.md` and opens a PR).
It is the contract. Everything below is a default that `AUTONOMY.md` may override.

Expected fields (plain markdown, see the TattooCraft one for an example):
- `merge`: `auto` (Octa merges on green) or `human` (Octa stops at an open PR)
- `verify`: commands that must exit 0
- `tracker`: Linear profile, team, project
- `agents`: default harness and per-area or per-label overrides (`agent:codex` label wins)
- `escalate`: categories and paths that always go to the human
- `limits`: max parallel arms, max waiting decision worktrees, retries per ticket

Load the Orca guide once per session: `orca skills get orchestration`. Linear language and
profile rules come from `~/.agents/crew/LINEAR-PROFILES.md`.

Resolve the target repo's Orca id once per session, from the git root of the cwd:

```
REPO_ID=$(orca repo list --json | jq -r --arg p "$(git rev-parse --show-toplevel)" \
  '.result.repos[] | select(.path==$p) | .id')
```

No match → stop and tell the user the repo is not registered in Orca. Never infer the repo from
`ORCA_WORKSPACE_ID`: the session may have been started from another repo's terminal.

## 1. Sweep (one pass)

Octa is **stateless between passes**: state lives in Linear (status, assignee, labels) and in Orca
(runs, dispatches). Re-read both every pass; never trust memory of a previous pass.

1. `orca orchestration check` — handle any worker mail first (§4).
2. List the project's open tickets (Backlog, Todo, In Progress, In Review).
3. Skip tickets already claimed (assignee set, or a live Orca dispatch for them), and anything
   labelled `octa:skip`.
4. Triage each remaining ticket into exactly one lane (§2).
5. Dispatch within `limits`. Overflow waits for the next pass.
6. Report the pass (§6).

`dry-run` argument: do 1–4 and print the triage table only.

## 2. Triage lanes

Ask: **can I state now which files change and what "done" means?**

| Lane | When | Action |
|---|---|---|
| **Arm** | Yes, and it fits one PR, and it touches no `escalate` path | Dispatch a worker (§3) |
| **Map** | No — big, foggy, or spans several areas | Hand to `wayfinder-crew`: research tickets run AFK as arms; the map's HITL tickets go to the Deck |
| **Deck** | A product/design decision, a wayfinder grilling or prototype ticket, a human-only task, an escalation | Open a decision worktree (§5) |
| **Hold** | Blocked by an open ticket, or waiting on the human already | Leave it |

`wayfinder-crew` is user-invoked only. Octa does not chart a map itself: it opens a Deck worktree whose
first message tells the human "this needs a map" and runs `/wayfinder-crew` there once they say go.

## 3. Arms: worker dispatch

```
orca orchestration worker-start --spec-file <spec> --task-title "<ID> <title>" \
  --worktree new-top-level --repo id:$REPO_ID --name <id>-<slug> --base-branch origin/main \
  --agent <harness from AUTONOMY.md> --json
```

The spec is the same for every harness. Template:

```
Ticket <ID>: <title>. Read it and its comments in Linear first; "Done when" is the bar.
Repo rules: CLAUDE.md / AGENTS.md and AUTONOMY.md.
Scope: <files/areas>. Do not edit outside it unless required; say why if you do.
Verify: <verify commands>; all must exit 0.
Done: commit on your branch, push, open a PR to main (body: summary, evidence, `Closes <ID>`
or `Refs <ID>` if human work remains). Move the ticket to In Review with the PR link.
Do NOT merge. Report via worker_done: PR URL, files, verify output, open questions.
Failure budget: if you cannot make verify pass after 2 honest attempts, stop and report why.
Linear writes: language per profile (personal → 繁體中文, work → English).
```

## 4. When an arm reports

- `worker_done` with a PR → **merge gate** (only if `merge: auto`):
  1. `gh pr checks <n> --watch --fail-fast` — every check must pass. No CI checks at all → do not merge; escalate.
  2. `gh pr view <n> --json mergeable,files` — mergeable, and no file under an `escalate` path.
  3. `gh pr merge <n> --merge --delete-branch`, then move the ticket to Done.
  Any step fails → the PR stays open and the ticket goes to the Deck with the reason.
- Conflicts with an already-merged PR → send the arm back: `orca orchestration send --to dispatch:<id> ...`
  to rebase, re-verify, and report again. Product-level conflict → Deck.
- Failure report or failure budget hit → Deck with the log and a recommendation.
- `merge: human` → leave the PR, list it in the pass report.

## 5. Deck: calling the human

The human lives in Orca, so a decision is a **kept-open worktree** they can switch into:

```
orca orchestration worker-start --keep-open --spec-file <deck-spec> --task-title "Decide: <title>" \
  --worktree new-top-level --repo id:$REPO_ID --name decide-<id> --base-branch origin/main --agent <default> --json
```

The deck worker's job:
1. Claim the ticket. Load the ticket, its blockers, related closed tickets, relevant code and research.
2. Prepare: context → options (≤ 4) → recommendation. Build a 圖解 artifact when the ticket weighs ≥ 2 routes.
3. **Stop and wait for the human.** Orca marks the worktree as needing attention.
4. When the human arrives: one question at a time (wayfinder grilling rules). Never answer for them.
5. Record the decision on the ticket, close or update it, create follow-up tickets, then `worker_done`
   so Octa can dispatch the resulting arms.

At most `limits.deck` (default 3) open at once; the rest queue, most-blocking first.
Optional (Claude Code): a push notification summarising "N decisions waiting, most urgent: <title>".

## 6. Pass report (to the human, terse)

Merged (PR, ticket) · In flight (arms) · Waiting on you (Deck worktrees by name) · Held · Anything
Octa refused to merge and why. Nothing changed → one line.

## Scheduling

- Claude Code: `/loop /octa` (self-paced; worker mail wakes Octa anyway).
- Other harnesses: run `/octa` (or the harness's equivalent) from an Orca automation or cron.

## Never

- Merge in a repo without `AUTONOMY.md` or with `merge: human`.
- Merge with failing, pending, or missing checks, or with files under an `escalate` path.
- Push to `main` or force-push a shared branch.
- Answer a Deck question on the human's behalf.
- Poll in a tight loop; Orca wakes Octa when arms report.
- Use `--worktree new-child` or `current`: they follow `ORCA_WORKSPACE_ID`, which can point at
  another repo. Always `new-top-level --repo id:$REPO_ID`.
