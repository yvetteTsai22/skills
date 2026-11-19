---
description: Code review a pull request via MCP-free subagents (context-safe fork of /code-review:code-review)
---

Code review the pull request given in ARGUMENTS (default: the PR for the current branch).

This is a context-safe fork of `/code-review:code-review`. Two differences, and both matter:

- Every subagent is a **named `pr-review-*` type with no MCP tools**. Never use `general-purpose`
  here — it carries `Tools: *`, which loads every MCP server's schemas into each agent and
  exhausts its context before it reads a line of code.
- The diff is **extracted once, to a file**, and agents are handed the path. Never let six agents
  each run `gh pr diff`.

Make a todo list first.

## 0. Extract once

```bash
PR=<number>
D="$SCRATCHPAD/pr$PR.diff"     # scratchpad dir from your environment; never /tmp
gh pr diff "$PR" --patch > "$D"
gh pr diff "$PR" --name-only > "$SCRATCHPAD/pr$PR.files"
gh pr view "$PR" --json headRefOid --jq .headRefOid   # full sha, needed for permalinks
wc -l "$D"
```

If the diff exceeds ~4000 lines, also split it per file into `$SCRATCHPAD/pr$PR/<name>.diff` and
hand each agent only the slices it needs.

**Call graph** (for `pr-review-bugs` and `pr-review-reach`). Only when the local checkout *is*
the PR head: the graph is built from the working tree, so any other checkout would describe the
wrong code. Start it in the background (Bash `run_in_background`) right after extracting: it runs
while steps 1–3 do, and costs ~30s cold, a few seconds warm.

```bash
G="$SCRATCHPAD/pr$PR.graph.txt"
if [ "$(git rev-parse HEAD)" = "<headRefOid from above>" ] && [ -z "$(git status --porcelain --untracked-files=no)" ]; then
  ~/.claude/bin/pr-review-graph --base "$(git merge-base "origin/$(gh pr view "$PR" --json baseRefName -q .baseRefName)" HEAD)" --out "$G"
else
  echo "Graph: none (checkout is not the PR head)" > "$G"
fi
```

The script runs `gitnexus analyze --index-only` on the checkout (incremental; writes only
`.gitnexus/`, never AGENTS.md / CLAUDE.md / skills), maps the diff to changed symbols, and writes
their callers, unchanged callees, and import cycles. It never fails the review: on any error the
file says `Graph: unavailable (...)` and the agents fall back to grep. Wait for it only when you
launch step 4.

Also start the miss-retro history extract in the background now (`~/.claude/review-miss-retro.md`
step 1). It counts toward nothing in the agent cap.

## 1. Eligibility

`pr-review-scout`: is the PR closed, a draft, automated/trivial, or already reviewed by you?
If any, stop and say why.

## 2. Conventions

`pr-review-scout`: list paths (not contents) of the root `CLAUDE.md`, any `CLAUDE.md` in modified
directories, and any `.claude/rules/*.md`.

## 3. Summary + ticket

`pr-review-scout`: summarize the change from the extracted diff path.

Ticket (you, not a subagent — the agents have no MCP tools): find the linked issue (Linear
identifier in the branch name, PR title/body, or the `linear-code[bot]` linkback comment), fetch
its description with the Linear MCP `get_issue`, and write it to `$SCRATCHPAD/pr$PR.ticket.md`.
No linked ticket → skip the spec leg and say so in the final message.

## 4. Review — eight agents, one message, in parallel

Give every one of them the diff path, the files list, the CLAUDE.md paths from step 2, the scout's
summary, and the ticket path plus any precedent paths the ticket names. Add nothing else: no
statements of what the code guarantees, no "focus on", no "known / don't repeat" list (see the frozen
template in `pre-pr-review.md`). `pr-review-bugs` and `pr-review-reach` also get `Graph: <G>`.

Launch them as **background** agents (`run_in_background: true`) so each result arrives on its
own and step 5 can start per leg.

**Concurrency cap: at most 8 agents in flight** (review legs + verifiers together; the scout
counts). More than that hits API rate limits (`429 Rate limited`): a PR #205 run peaked at 17 and
stalled in retries. Keep one queue:
1. review legs first, longest first: bug/reach slices, then `spec`, `history`, `design`,
   `guidelines`, `comments`, `prior-art`;
2. verifiers after any unlaunched leg, in the order their findings arrived.

Launch up to the cap, then launch the next queued agent each time one returns. If you still see a
429 retry, lower the cap to 6 for the rest of the run.

| agent | job |
|---|---|
| `pr-review-guidelines` | compliance with CLAUDE.md and `.claude/rules/*.md` |
| `pr-review-bugs` | significant bugs in the changed lines themselves |
| `pr-review-reach` | bugs outside the diff: unchanged callees the PR newly calls, import cycles, secret sinks, incomplete fixes, latent risks |
| `pr-review-history` | regressions, judged against bounded git history |
| `pr-review-prior-art` | review comments on earlier PRs that recur here |
| `pr-review-comments` | code that contradicts its own comments, docstrings, or docs |
| `pr-review-spec` | the ticket's "Done when" and definitions vs what the code delivers (gets the ticket path) |
| `pr-review-design` | duplication of precedents, unasked complexity, size / reasons to change, decisions inside `async` shells |

`pr-review-reach` also reports a separate **latent** list: things that break the day a caller the PR
prepares for (wiring, config, a non-empty set) lands. Keep them; they are not speculative.

If an agent dies on context, do not silently drop its leg. Re-run it with a narrower input (a
per-file diff slice, fewer files), and if it still fails, say so in your final message to the user
so they know that angle went uncovered.

Diff over ~4000 lines: slice both bug legs. Group the per-file slices (files that call each other,
per the graph, go together; aim for ~2000-4000 lines a group, **at most 3 groups**), then run **one `pr-review-bugs` and
one `pr-review-reach` per group**, all in the same parallel launch. These are the legs whose time
grows with diff size. Each gets the frozen prompt with the full diff as `Diff:` plus one extra line:
**"Slice: <group diff path> (files: <group files path>). Review only this slice; the full diff is
context."** Both agents know what that line means. The other six legs still get one agent over the
whole diff.

## 5. Score

One `pr-review-verifier` per finding. **Pipeline it:** as each review leg returns, queue the
verifiers for that leg's findings at once; do not wait for the other legs. They share the step-4
concurrency cap. (Scoring is
per finding, so nothing is lost by starting early.) Go to step 6 when every leg has returned and
every verifier has scored. Each gets the diff path, the finding, the
CLAUDE.md paths, and the ticket path (spec findings are scored against the quoted ticket line).

## 6. Filter

Drop everything under 75 (the rubric is 0/25/50/75/100 — a bar of 80 keeps only 100). If nothing
survives, stop.

Treat as false positives: pre-existing issues; things that look like bugs but are not; nitpicks a
senior engineer would not raise; anything a linter, typechecker, or CI is configured to catch and
would fail on (a repo rule stricter than the tool's configuration stays in scope); general quality
gripes with no rule behind them; rules the code explicitly silences with a documented reason
comment; intentional changes that are the point of the PR (never a `pr-review-spec` finding: a PR
that intentionally departs from its ticket is exactly what that leg reports); findings on lines the
PR did not modify.

"Coverage gripes with no rule behind them" does **not** cover: an untested behaviour change
(intentional or not), a test whose only assertions are `hasattr`/`inspect`/AST or source-grep/
field-list snapshots, or a missing parity test when a diff changes two implementations of one port.
Those survive the filter.
Verifiers for `pr-review-spec` findings are dispatched with `model: sonnet`.

Exceptions to the last two — these are **not** pre-existing and survive:
- unchanged code the PR newly calls, or newly routes a new case through, whose assumptions no
  longer hold for the new caller (e.g. a GitHub-shaped classifier now deciding a non-GitHub leg);
- an unchanged entry point that must be touched for the ticket's "Done when" to be reachable
  (from `pr-review-spec`);
- an import the PR adds that closes a cycle with an existing import in the other direction.

A `pr-review-design` duplication finding is not a false positive because the copied code follows a
precedent; copying the precedent is the finding.

## 7. Re-check

`pr-review-scout`: confirm the PR is still eligible.

## 8. Comment

Post with `gh pr comment`. Write each finding using the `writing-pr-review-comments` skill:
severity marker on its own line, then the concrete outcome in plain words, then the mechanism with
real line numbers, then a `Fix suggested by claude:` list. No em dashes, no mirrored clauses.

Permalinks need the **full sha from step 0**, never a `$(git rev-parse HEAD)` substitution — the
comment renders as literal Markdown:
`https://github.com/<owner>/<repo>/blob/<full-sha>/<path>#L<start>-L<end>`, with at least one line
of context either side.

Format:

```
### Code review

Found N issues:

1. <brief description> (<source> says "<quote>")

<permalink>
```

Or, with none: `No issues found. Looks good!`

The comment ends at the last permalink. Do **not** append a `🤖 Generated with Claude Code` footer
or any other attribution line: the session's attribution note covers commits and PR descriptions,
not review comments.

## 9. Miss retro

Findings that survived step 6 on a PR already reviewed (an earlier `/pr-review`, `/pre-pr-review`
or `/address-pr-comments` in any session on the head branch) are leaks. Per
`~/.claude/review-miss-retro.md`: **launch** (classify + background `pr-review-miss-retro`) as soon
as step 6 ends, so it runs during steps 7-8; **print** retro, vent and improvements after posting.
It shares the 8-agent cap. Nothing from it goes into the GitHub comment.

Do not build or typecheck the app. CI does that.
