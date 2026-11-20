---
description: Full /pr-review-grade review of the LOCAL branch — committed, unpushed, and uncommitted changes alike; pass a PR number to cover an open PR plus local work. Reports in the terminal; posts nothing.
argument-hint: "[PR number | base-branch, default main] [--loop] [--reset] [--quick] [--delta]"
---

Review everything on this branch that isn't on the base yet, **before** opening a PR:
commits (pushed or not) **plus** staged, unstaged, and untracked changes.

Same engine as `/pr-review` (read `~/.claude/commands/pr-review.md` for the shared rules), with
three differences: the diff comes from git instead of `gh`, there is no eligibility gate, and the
result goes to the terminal, never to GitHub.

Same hard rules as `/pr-review`: every subagent is a named `pr-review-*` type (no MCP tools, never
`general-purpose`); the diff is extracted **once** to a file and agents get the path.

Never run `git add`, `git add -N`, `git stash`, or `git commit` — the working tree is read, not touched.
(Sole exception: the loop-state snapshot in step 0, which runs `git add` against a throwaway
`GIT_INDEX_FILE` in the scratchpad and never touches the real index.)

Make a todo list first.

## 0. Extract once

**PR already open?** Pass its number (`/pre-pr-review 743`). This command then covers the whole
PR — pushed commits, local unpushed commits, and uncommitted changes — in one diff, so it replaces
`/pr-review` for a fix loop that must not commit. Before extracting:

Arguments: `[PR number | base-branch] [--loop] [--reset] [--quick] [--delta]`. `--delta` = review only the commits `/address-pr-comments` just pushed (see "Delta mode"). `--loop` = this run is one round of a
fix loop (see "Fix loop"); `--reset` = discard the loop state and start at round 1; `--quick` = a
cheap mid-work check (see "Quick mode"), never combined with `--loop`.

```bash
set -- $ARGUMENTS
TARGET=""; LOOP=0; RESET=0; QUICK=0; DELTA=0
# Allowlisted read-only gh wrapper; this command never writes to GitHub.
GH=gh; ~/.claude/bin/ro-gh repo view --json name >/dev/null 2>&1 && GH=~/.claude/bin/ro-gh
for a in "$@"; do case "$a" in --loop) LOOP=1 ;; --reset) RESET=1 ;; --quick) QUICK=1 ;; --delta) DELTA=1 ;; *) TARGET=$a ;; esac; done
[ "$QUICK" = 1 ] && [ "$LOOP" = 1 ] && echo "QUICK_AND_LOOP: stop, --quick cannot run as a loop round"
if [[ "$TARGET" =~ ^#?[0-9]+$ ]]; then
  PR=${TARGET#\#}
  read -r BASE HEADREF STATE < <($GH pr view "$PR" --json baseRefName,headRefName,state -q '.baseRefName+" "+.headRefName+" "+.state')
  [ "$(git branch --show-current)" = "$HEADREF" ] || echo "WRONG_BRANCH: on $(git branch --show-current), PR is $HEADREF"
  git fetch origin "$HEADREF" --quiet
  git merge-base --is-ancestor "origin/$HEADREF" HEAD || echo "BEHIND_REMOTE: origin/$HEADREF has commits HEAD lacks"
  "$GH" pr view "$PR" --json body -q .body > "$SCRATCHPAD/prepr.pr-body.md"
fi
```

- `WRONG_BRANCH` → stop and ask. Never checkout.
- `BEHIND_REMOTE` → stop and ask: remote-only commits would be missing from the review. The user
  pulls (you don't — no git writes). Only after that does "PR + local committed + uncommitted" hold.
- Findings don't re-report open reviewer comments (that's `/address-pr-comments`), but reviewers'
  comments are the best signal of what classes this code has. Fetch them once:
  ```bash
  { "$GH" api "repos/{owner}/{repo}/pulls/$PR/comments" --jq '.[] | "\(.path):\(.line) \(.body[0:400])"'
    "$GH" api "repos/{owner}/{repo}/issues/$PR/comments" --jq '.[] | "issue: \(.body[0:1500])"'
  } > "$SCRATCHPAD/prepr.prior-comments.md"
  ```
  `$SCRATCHPAD/prepr.pr-body.md` (PR mode) goes into the `pr-review-spec` prompt as
  **"PR description: <path>. Flag every claim in it the diff does not match."**
  Its path goes into the `pr-review-bugs`, `pr-review-prior-art`, `pr-review-spec`,
  `pr-review-design`, and `pr-review-guidelines` prompts (step 2).

```bash
BASE=${BASE:-${TARGET:-main}}
git fetch origin "$BASE" --quiet || true              # compare against the real base if reachable
REF=$(git rev-parse --verify -q "origin/$BASE" || git rev-parse "$BASE")
MB=$(git merge-base "$REF" HEAD)
D="$SCRATCHPAD/prepr.diff"                            # scratchpad dir from your env; never /tmp
F="$SCRATCHPAD/prepr.files"

UNTRACKED() { git ls-files --others --exclude-standard | grep -v '^\.gitnexus/'; }  # never the graph index
git diff "$MB" > "$D"                                 # commits + staged + unstaged, vs merge-base
UNTRACKED | while read -r u; do
  git diff --no-index /dev/null "$u" >> "$D" || true  # untracked files as additions
done
{ git diff --name-only "$MB"; UNTRACKED; } | sort -u > "$F"

git log --oneline "$MB"..HEAD                         # what's committed
git status --short                                    # what isn't
wc -l "$D"
grep -Eil 'token|secret|credential|password|redact|scrub|log\.(exception|error)|exc_info' "$D" >/dev/null \
  && echo "SENSITIVE=1"                               # secret/logging touched: see step 2

# Cross-PR lessons: bug classes human/Copilot reviewers caught that this command missed.
REPO_NAME=$(git remote get-url origin 2>/dev/null | sed 's#.*/##; s#\.git$##')
LESSONS="$HOME/.claude/review-lessons/${REPO_NAME:-local}.md"
[ -s "$LESSONS" ] && echo "LESSONS=$LESSONS"
# Miss-retro history (~/.claude/review-miss-retro.md step 1): run that block in the background
# now (run_in_background), skip under --quick. Findings are not needed yet.

# Leg-skip signals (step 2 "Skip rules")
git diff --diff-filter=MDR --name-only "$MB" | grep -q . && echo "MODIFIES_EXISTING=1"

# Mechanical pre-checks over added lines only, passed to the guidelines leg as extra input
grep -E '^\+' "$D" | grep -vP 'type:\s*ignore\[[^]]*\]\s+#' | grep -E 'type:\s*ignore' > "$SCRATCHPAD/prepr.mech-ignore.txt" || true
grep -E '^\+' "$D" | grep -E '\bAny\b' > "$SCRATCHPAD/prepr.mech-any.txt" || true
grep -E '^\+' "$D" | grep -P 'from \S+ import (\w+) as \1\b|^\+\s*"[A-Za-z_]+",?\s*#.*__all__' > "$SCRATCHPAD/prepr.mech-reexport.txt" || true
MECH="$SCRATCHPAD/prepr.mech-checks.md"
{
  echo "type: ignore with no trailing # reason:"; cat "$SCRATCHPAD/prepr.mech-ignore.txt"
  echo "bare Any in added lines:"; cat "$SCRATCHPAD/prepr.mech-any.txt"
  echo "re-exports (from X import Y as Y, or __all__-only names) outside __init__.py:"
  cat "$SCRATCHPAD/prepr.mech-reexport.txt"
} > "$MECH"
[ -s "$MECH" ] && echo "MECH=$MECH"

# New output sinks: a value newly written to a log, event, message or DB row (PR #216: a URL-derived
# label carried clone-URL credentials into logs, Pub/Sub and task_run; no secret keyword was in the diff)
grep -E '^\+' "$D" | grep -Eq 'log\.(info|warning|error|debug|exception)\(|\.bind\(|publish|Envelope|Event\(|Column\(|model_dump|json\.dumps' \
  && echo "NEW_SINK=1"
# Untrusted reads: files, sandbox commands or remote content read into the process (PR #216:
# symlink escape, whole file crossing the transport before a cap, frontmatter past a read prefix)
grep -E '^\+' "$D" | grep -Eq 'execute_command|read_text|read_bytes|open\(|subprocess|\b(cat|head|tail|find)\b |realpath|httpx\.|\.get\(' \
  && echo "UNTRUSTED_READ=1"

# Context from outside the diff, fetched once so no review agent needs a shell or the network:
# CI/Dockerfiles, docs and other surfaces that name changed identifiers, references to removed
# identifiers, sibling repos' local clones (git show origin/<branch>, no fetch), and mechanical
# hits for ticket/PR refs, history words and literal dates. Optional per-repo config:
# ~/.claude/review-context/<repo>.json (related_repos, ticket_pattern, extra_context).
git diff --name-only "$MB" > "$SCRATCHPAD/prepr.files.txt"
~/.claude/bin/prepr-context --diff "$D" --files "$SCRATCHPAD/prepr.files.txt" \
  --repo-name "${REPO_NAME:-local}" --out "$SCRATCHPAD/prepr.external"   # prints EXTERNAL=<manifest>
```

`prepr-context` only reads. A related repo's snapshot is as old as its last `git fetch`; the
manifest says how old. If it is days old, say so in the report — do not fetch it yourself.

**Loop state** (only with `--loop`). State lives per worktree in `$(git rev-parse --git-dir)/prepr-loop/`.
A snapshot of the working tree is taken with a **throwaway index**; this is the one allowed use of
`git add`, because it never touches the real index or the working tree:

```bash
if [ "$LOOP" = 1 ]; then
  S="$(git rev-parse --git-dir)/prepr-loop"
  [ "$RESET" = 1 ] && rm -rf "$S"
  mkdir -p "$S"
  [ "$(cat "$S/branch" 2>/dev/null)" = "$(git branch --show-current) $MB" ] \
    || { rm -f "$S"/*; echo "$(git branch --show-current) $MB" > "$S/branch"; }
  N=$(( $(cat "$S/round" 2>/dev/null || echo 0) + 1 ))
  TMPIDX="$SCRATCHPAD/prepr.index"; rm -f "$TMPIDX"
  TREE=$(GIT_INDEX_FILE="$TMPIDX" sh -c 'git read-tree HEAD && git add -A && git rm -r -q --cached --ignore-unmatch .gitnexus && git write-tree')
  NEXT=$(cat "$S/next" 2>/dev/null || echo full)      # full | delta | gate — written by the previous round
  [ "$N" = 1 ] && NEXT=full
  if [ "$NEXT" = delta ]; then
    git diff "$(cat "$S/tree")" "$TREE" > "$SCRATCHPAD/prepr.delta.diff"
    wc -l "$SCRATCHPAD/prepr.delta.diff"
  fi
  echo "ROUND=$N KIND=$NEXT"
fi
```

An empty delta diff means nothing changed since the last round: run a `gate` round instead.

Empty diff: stop, say "nothing to review vs $BASE".
Over ~4000 lines: split per file into `$SCRATCHPAD/prepr/<name>.diff`, hand each agent only its slices,
and slice both bug legs: one `pr-review-bugs` and one `pr-review-reach` per group (see `/pr-review`
step 4).

**Call graph.** Start it now in the background (Bash `run_in_background`) so it overlaps step 1; it
covers committed and uncommitted work, since it indexes the working tree. Rebuild it every round (a
fix loop changes the tree), which is cheap: the index is incremental.

```bash
G="$SCRATCHPAD/prepr.graph.txt"
~/.claude/bin/pr-review-graph --base "$MB" --out "$G"
```

It runs `gitnexus analyze --index-only` (writes only `.gitnexus/`, never AGENTS.md / CLAUDE.md /
skills; the snapshot and untracked listings above skip that dir), then writes each changed symbol's
callers, unchanged callees, and import cycles. It never fails: on error the file reads
`Graph: unavailable (...)` and the agents grep instead. Wait for it only when launching step 2.

## Timing log

Every run records how long each step and each agent took, so later retros can see where review
time goes. One JSON line per event, appended to
`TL="$HOME/.claude/review-timing/${REPO_NAME:-local}.jsonl"` (create the dir):

```
{"run":"<branch>@<short HEAD>-<epoch>","round":<N or 0>,"kind":"full|delta|gate|quick",
 "pr":<PR or null>,"what":"step:0-extract|step:1-scout|leg:<agent>|verifier:<leg>#<i>|probe:<i>|step:4-report|retro|run",
 "start":"<ISO>","end":"<ISO>","duration_ms":<n>,"tokens":<subagent_tokens or null>,
 "tool_uses":<n or null>,"result":"ok|dead|skipped|timeout","findings":<n or null>}
```

- Steps: take `date -u +%FT%TZ` at each step's start and end (fold into a Bash call you already make).
- Agents: use `duration_ms`, `subagent_tokens` and `tool_uses` from each agent's completion
  notification; `start` is when you launched it. A dead or re-run leg gets one line per attempt.
- The last line of a run is `"what":"run"` covering the whole command, with total findings.
- Write the lines in one Bash call at the end of step 4 (keep the values in your notes until then);
  the background retro appends its own `retro` line when it finishes. Never let logging delay the
  report.

## Agent prompts are frozen

Build each agent's prompt from **this template only**; fill the `<…>` slots and add nothing else:

```
Review the extracted diff file; it includes local uncommitted work. Never call `gh pr diff` /
`gh pr view` for the current change — GitHub doesn't have the local part. `gh` is fine for looking
up *earlier* PRs (prior-art).
Diff: <D>  Files: <F>  Repo: <root>  Conventions: <paths from scout>
Ticket: <ticket path or "none">  Precedents named by the ticket: <paths or "none">
Change summary (from pr-review-scout, not the author): <scout bullets>
Graph: <G>        (pr-review-bugs and pr-review-reach only; omit the line for other agents)
<the step-2 extra lines for this agent, verbatim, only when they apply>
```

**Forbidden in agent prompts:** statements of what the code guarantees ("X must not overwrite Y",
"compare-then-write"), "focus on", "prior pass found nothing", "confirm quickly", "the uncommitted
fix is in…", and any "known / accepted / don't repeat" list. The author's beliefs about the code are
exactly what the review is testing. The one allowed suppression is a finding with a **ticket ID and
file:line** that a previous round already reported and the user deferred; list those only in the
final report under `suppressed:`, never in a prompt.

A **full** round is **all eight legs (minus any the step-2 skip rules exclude) + scout + one verifier per finding**. Only a full round can
mark the branch clean. In a fix loop, the rounds between full rounds are **delta** rounds (see
"Fix loop" at the end): they review the fixes since the last round, not the whole branch.

## 1. Conventions + summary

One `pr-review-scout`: list paths (not contents) of root `CLAUDE.md`, any `CLAUDE.md` in modified
directories, `.claude/rules/*.md`, and any plan/decision docs (`docs/**/*plan*.md`,
`docs/decisions/**`, any doc mentioning the ticket id or its parent id); then summarize the change
from `$D`. **This summary, not your own, is the only change description agents receive.**
If `SENSITIVE=1`, also list the paths of the logging setup and exception renderer
(e.g. `grep -rln 'structlog.configure\|logging.config' src`).

Ticket (you, not the scout — agents have no MCP tools): take the Linear identifier from the branch
name (e.g. `mee-812` → `MEE-812`) or the PR, fetch it with the Linear MCP `get_issue`, and write
its description to `$SCRATCHPAD/prepr.ticket.md`. None found → skip the spec leg, say so in the report.
If the ticket names a precedent to start from ("start from the Linear precedent", a file or module
name), resolve it to repo paths; those go in the `Precedents` slot.
When Linear is available, also fetch the ticket's parent and any related/linked tickets and write
their descriptions to `$SCRATCHPAD/prepr.related-tickets.md`. Pass both this path and the
plan/decision doc paths from the scout to the guidelines and spec legs with: **"Decisions recorded
here are rules; quote them."**

## 2. Review — eight agents, one message, in parallel

Identical to `/pr-review` step 4: `pr-review-guidelines`, `pr-review-bugs`, `pr-review-reach`,
`pr-review-history`, `pr-review-prior-art`, `pr-review-comments`, `pr-review-spec`,
`pr-review-design`. Each gets the frozen prompt above. Launch them as background agents so step 3
can start per leg, under `/pr-review` step 4's **8-in-flight concurrency cap** (legs first,
longest first; verifiers queue behind unlaunched legs).
Dead leg → re-run narrower; still dead → name the uncovered angle in the report.

**Skip rules.** A leg with nothing to inspect is skipped, not run empty. A skipped leg is **not** a
missing leg: list it in the report as `skipped: <leg> (<reason>)`, and it does not block the clean
marker.
- `pr-review-spec`: skipped when no ticket was found (step 1). In `--loop`, its full check runs
  only in `full` and `gate` rounds; in a PR-mode `delta` round it runs the description check only.
- `pr-review-prior-art`: skipped unless PR mode with a non-empty `prepr.prior-comments.md`, or
  `LESSONS` is set.
- `pr-review-history`: skipped unless `MODIFIES_EXISTING=1` (a diff of only new files has no
  history to regress).

Extra lines, added verbatim to the named agent's prompt when they apply (these are the only
additions the frozen template allows):
- Diff over ~4000 lines → each sliced `pr-review-bugs` / `pr-review-reach`: **"Slice: <group diff
  path> (files: <group files path>). Review only this slice; the full diff is context."** Every
  other extra line below still goes to every slice of the named agent.
- `SENSITIVE=1` from step 0 → have the scout (step 1) also list the logging / exception-renderer setup
  files, pass those paths to `pr-review-reach`, and say: **"Secret or logging code changed: trace each secret to every sink
  (log kwargs, exc_info, exception text, repr, responses, headers) and read the sink config."**
- Any commit in `git log "$MB"..HEAD` is a fix, or uncommitted changes address review findings →
  `pr-review-bugs` and `pr-review-reach`: **"This branch contains fixes: check each one closes the class, not just the
  reported line. A fix is new code: check it for over-breadth too. A new `except`, a widened
  classification set, a new latch or retry branch: does it now also catch, latch, or retry cases the
  original finding did not name?"** Also, on a fix loop, **do not narrow the prompt to the previous
  round's findings.** Every round gets the full, unanchored prompt; a loop that only re-checks last
  round's class converges on "clean" while a different class goes unreviewed.
- PR mode with `$SCRATCHPAD/prepr.prior-comments.md` non-empty → `pr-review-bugs`,
  `pr-review-prior-art`, `pr-review-spec`, `pr-review-design`, `pr-review-guidelines`:
  **"Prior reviewer comments: <path>. For each comment in your leg's scope, name its class and
  find other instances of that class in the diff. Report only instances the comment did not point
  at."**
- `NEW_SINK=1` from step 0 → `pr-review-reach`: **"New output sinks: for every value the diff
  newly writes to a log, event, message, DB row or agent context, trace it back to its origin
  (config, URL, user or repo input), including through unchanged helpers whose docstrings claim a
  narrower use. Report any path where a credential or untrusted text can reach the sink."**
- `UNTRUSTED_READ=1` from step 0 → `pr-review-bugs` and `pr-review-reach`: **"Untrusted reads:
  for every file, command output or remote body read in, check symlinks and path escape, where the
  size is bounded (the bound must hold where the bytes first enter the process, not after), encoding,
  and every parser that needs an end marker (frontmatter, fences, quotes) when the read is partial."**
- Any fix in the branch (same condition as the fix line above) → `pr-review-bugs`: **"For every
  hash, count or size the diff records, check it is computed from exactly the bytes the consumer
  receives, with no strip or normalisation in between."**
- Any fix in the branch, or a delta round → `pr-review-bugs`: **"List every function, method or
  branch the fixes added (not refactors of existing ones). For each, give at least two `probe:`
  entries: one boundary case (empty, at a cap, out of order, raises) and one interaction with
  existing code it now shares state with. A new path with only happy-path tests is a finding."**
  These probes are run in step 3 like any other; a new path is never marked clean on reading alone.
  (MEE-2078 Batch B: `_uncounted_siblings` and a `_tear_down` raise path, both added in round 3,
  were caught only in round 4.)
- PR mode, including delta rounds → `pr-review-spec` runs on the delta too, with only this line
  and the PR-description line from step 0: **"The fixes changed code the PR description
  describes. Flag every claim in the description the current code no longer matches."**
  (Batch B: two PR bodies still described pre-fix behaviour for a whole round.)
- `LESSONS=<path>` from step 0 → `pr-review-bugs`, `pr-review-reach`, `pr-review-design`, and
  `pr-review-guidelines`: **"Bug classes that past
  human or Copilot reviewers on this repo caught and this review missed: <path>. Check the diff for
  every class listed."**
- `MECH=<path>` from step 0 → `pr-review-guidelines`: **"Mechanical pre-check results on added
  lines: <path>. Each hit is a candidate finding; confirm against the actual line (a listed `Any`
  may be inside a string or comment) before reporting it."**
- `EXTERNAL=<manifest>` from step 0 → every leg except `pr-review-scout`: **"Context outside the
  diff, already fetched: <manifest>. You have no network; read the files it lists. Never edit them."**
  Plus one per leg:
  - `pr-review-bugs` (missed code bugs): **"For each changed computation, write a boundary
    timeline before judging it — the ordinary case, the field missing or None, two events at the
    same instant, a value going negative, an interval interrupted and resumed, the legacy row the
    old code wrote, a timezone or date boundary. For each, state input → expected → what the code
    computes. For each changed test, name the single assert that makes it fail if the code under
    test is wrong; a test whose only failing assert checks something else, or that round-trips the
    code's own output, is a finding. List doubtful cases under `probe:` as a minimal test you would
    run (input, expected)."**
  - `pr-review-reach` (needs an external source): **"Using the manifest: (1) every value this diff
    writes or reads across a process, repo or service boundary — compare the producer's and the
    consumer's meaning (units, date basis, which status counts, null handling) in the related-repo
    files; (2) check CI actually runs each new test (services it needs, skip markers, path
    filters); (3) check each new runtime dependency (module, system package, tz data, env var) is
    installed in the image that runs it. Anything that needs a build, a deploy or real data to
    settle goes under `unverified:` prefixed `manual:` with the exact check to run."**
  - `pr-review-guidelines` (context gaps): **"For each finding, say whether the convention it
    rests on is written in CLAUDE.md, .claude/rules or docs. If it is not written anywhere, tag it
    `context-gap` and draft the rule in two lines (rule + why) — a reviewer would only know it from
    past reviews."**
  - `pr-review-design` (solution design): **"Also look for: one format written in one place and
    parsed in another (or built in several); the same tuple unpacked repeatedly; parameters that
    must change together or that compete; a distinct id/enum type degraded to str or a bare
    literal; a default that exists only for tests; an invariant held by `assert`; one business
    rule implemented in two places. Tag each `owner-decision` if fixing it changes an interface."**
  - `pr-review-spec` (recorded decisions): **"Before any other check, build a decision table:
    one row per decision recorded in the ticket, its parent and related tickets, and the
    plan/decision docs (quote it), with a cell `satisfied | violated | n/a` and the file:line that
    shows it. Every `violated` row is a finding. Print the table in your output."**
  - `pr-review-comments` (docs drift): **"Using `doc-mentions.txt` and `stale-references.txt`
    from the manifest, and the related-repo docs: list docs, OpenAPI, skill descriptions and
    examples that still describe the old name, shape or behaviour, and docs that hardcode a date,
    a count or a name the code now derives."**

**Push first, review in parallel.** Pushing fixes does not wait for this review: GitHub CI runs
the full suite while a delta review runs here. What waits is **posting** replies and `gh pr ready`:
neither happens until the delta review of every pushed fix commit is clean (or its leftovers are
deferred to an approved ticket) and CI is green. A fix commit no review round ever saw is the gap
that leaked bugs before (PR #216, PR #399): pushed early is fine, never reviewed is not.

A lighter inline review (e.g. `caveman-review`) never substitutes for this command's delta review:
fixes are new code and must go through the full legs again. **`/code-review` (ECC) does not
substitute for this command before `gh pr ready` either.** One `/code-review` pass is enough to open
a **draft** PR so Copilot can start; the loop then runs locally with the PR number.

## 3. Score and filter

One `pr-review-verifier` per finding. Pipeline it as in `/pr-review` step 5: queue a leg's verifiers
the moment that leg returns, under the same 8-in-flight cap as the legs. Verifiers for
`pr-review-spec` findings are dispatched with `model: sonnet`; all others keep the agent's default.
Its prompt is frozen too:

```
Diff: <D>  Ticket: <ticket path or "none">  Conventions: <paths from scout>
Finding from <leg>, verbatim:
<the leg's output block, unedited — no summary, no question, no context you add>
```

Never add a framing question ("real gap or acceptable deferral?"), a defence ("the daemon has no
browser"), or a status ("already assigned to MEE-812"). The verifier judges the leg's words, not yours.

Drop under 75, with the same false-positive list **and exceptions** as `/pr-review` step 6
(newly-called unchanged code, unreachable Done-when entry points, and cycle-closing imports survive
even though the lines are unchanged).

**Never dropped:** a `pr-review-spec` finding tagged `blocks-closing`, `needs-owner`, or
`unverified`. Verify it (the score goes next to it in the report), but it goes into its step-4
section whatever it scores. A score of 0 there means "the verifier disagrees" and is shown, not
hidden. The owner decides, not the verifier.

**Probes (missed-bug class).** For each `probe:` from `pr-review-bugs` you cannot settle by
reading, write the minimal test to `$SCRATCHPAD/prepr.probe_<n>_test.<ext>` (never in the repo
tree) and run it with the repo's own test runner, pointed at that file. It may only read: no
network, no writes outside the scratchpad. A failing probe becomes a 🔴/🟡 finding with the
probe's output as evidence; a passing one is dropped and listed under `dropped by verifier:` as
`probe passed`. Delete nothing in the repo; the probe files stay in the scratchpad.

Print every dropped finding under `dropped by verifier:` with its score and the verifier's `why:`
line. Silence is not a disposition.

## 4. Report — terminal only

Write findings for a human reading a terminal, not in the one-line `caveman-review` GitHub format
(that format stays in `/pr-review` for posting). No throat-clearing, no praise per finding.

**Language.** Match the language the user wrote in. Chinese user → labels `問題` / `修法` / `來源` /
`問` and prose in Chinese; English user → `Problem` / `Fix` / `Source` / `Q`. Code, paths,
identifiers, rule file names and severity emoji stay verbatim.

**Layout.**
- Header `### Pre-PR review (vs <BASE>, <N> commits + <M> uncommitted files)`, then the totals
  line `totals: <a>🔴 <b>🟡 <c>🔵 <d>❓`.
- Group by file. Each group opens with `── <path relative to the package root, e.g.
  tools/workpad/gitops.py> ─────`. Order groups by their worst severity, then path. Inside a
  group sort by severity (🔴 → 🟡 → 🔵 → ❓), then line.
- Each finding is multi-line, with a blank line between findings:
  ```
  <emoji> L<line>  <short title, ≤8 words>
     Problem: <one or two sentences>
     Fix: <one sentence>
     Source: <rule file · design tag · spec ref · committed|uncommitted|latent>
  ```
  - `❓` findings replace `Problem`/`Fix` with one `Q:` line (`問:` in Chinese).
  - `Source` joins whatever applies with ` · `: the rule file a guideline agent cited
    (`rules/single-writer-state.md`), `design: <kind>` for `pr-review-design`, `<TICKET-ID> Done
    when` or the quoted definition for spec findings, then `committed` / `uncommitted`. Latent
    findings (from `pr-review-reach`'s latent list) are 🟡 and add `latent`. Omit the line if
    nothing applies.
  - A security finding, or one whose fix needs more than a sentence, may take one extra indented
    prose line under `Fix`.
- No GitHub permalinks; the group header plus `L<line>` locates it.

Worked example (Chinese user):

```
### Pre-PR review (vs main, 3 commits + 1 uncommitted files)
totals: 1🔴 1🟡 0🔵 1❓

── orchestrator/worker.py ─────

🔴 L88  停止後又跑第二次 run_burst
   問題: agent 已停止仍再呼叫 run_burst，重演多輪迴圈的成本問題。
   修法: 第一次 burst 結束後直接 return。
   來源: rules/one-loop-per-run.md · committed

❓ L120  stall 計時是否該重設
   問: 新 session 沿用舊的 last_event_at，是刻意的嗎？

── agent/openhands.py ─────

🟡 L41  await 沒有 timeout
   問題: 對外部的 await 沒包 asyncio.timeout，卡住會拖住整個 worker。
   修法: 用 read_timeout 包起來。
   來源: rules/structured-concurrency-and-timeouts.md · uncommitted
```

After the findings, **always** print these sections as short bullet lists (one `- ` item each, same
language rule), even when empty (`- none`). Also list `- skipped: <leg> (<reason>)`, uncovered
angles and `dropped by verifier:` the same way:

```
ticket-closure blockers:   # every pr-review-spec finding graded "blocks closing, not merging"
  <path:line>: <gap>. Needs: sign-off from ticket owner + blocking link to <follow-up ticket>.
needs owner decision:      # every pr-review-spec `needs-owner` finding, even if the PR documents it
  ❓ q: ticket says "<quote>"; PR does <X> (docs:<line>). Confirm with ticket owner.
suppressed:                # findings a previous round reported and the user deferred, with ticket ID
unverified:                # claims proven only against fakes/mocks, runtime behaviour no agent observed,
                           # and every bug/reach agent's `unverified:` list (not sent to verifiers)
manual check needed:       # every `manual:` item: needs a build, deploy, CI run or real data
  <what to run or look at> — settles <finding>
docs out of sync:          # pr-review-comments drift items: docs/OpenAPI/skills/examples in this
  <path:line>: says <old>; code now <new>   # or a related repo, still on the old name or shape
context gap — propose as rule:   # every `context-gap` finding, and any $LESSONS class seen in ≥2 PRs
  <rule, one line> — why: <one line> — target: <CLAUDE.md | .claude/rules/<name>.md>
```

`pr-review-design` findings tagged `owner-decision` also go under `needs owner decision`.
`context gap` rules are drafts for the user; never write them into the repo yourself.

`No issues. Ready for PR.` is allowed only when there are no findings **and** `ticket-closure
blockers` and `needs owner decision` are both empty. Plus one line per uncovered angle, and one per
leg that didn't run (a round missing a leg is never "clean").

**Clean marker.** When the round ran every leg, the report has no 🔴/🟡, and `ticket-closure
blockers` is empty, write the reviewed HEAD so a PR-create step can check it:

```bash
git status --porcelain | grep -q . \
  && echo "not marking clean: uncommitted changes aren't in HEAD" \
  || git rev-parse HEAD > "$(git rev-parse --git-dir)/prepr-clean"
```

Otherwise delete a stale marker: `rm -f "$(git rev-parse --git-dir)/prepr-clean"`.

**Miss retro.** If this round has any 🔴/🟡 (or ❓ the user later confirms real) and an earlier
review ran on this branch (another session's `/pre-pr-review` / `/pr-review` /
`/address-pr-comments`, or an earlier `--loop` round in `$S`), run `~/.claude/review-miss-retro.md`
over those findings: **launch** (classify + background `pr-review-miss-retro`, under the agent
cap) as soon as step 3's filter ends. **Never wait for it**: write and print the report (and in
`--loop`, start the fixes) without its result. The retro writes to
`$(git rev-parse --git-dir)/prepr-retro/round-<N>.md`; the report ends with one line
`miss retro: running → <that path>`. When it finishes, print a short summary (retro, vent,
improvements) as a separate message; if the session has already ended, the next round prints any
unread retro file first. A worker reporting to a coordinator sends its report immediately and
mentions only the retro path, never holds the report for it; a delta round's findings in code the last round's fixes wrote count as
`regression-by-fix`. `--quick` rounds skip it (they are not a gate) but are counted as earlier
reviews by later rounds.

Without `--loop`: ask whether to fix the findings. Do not fix, commit, push, or open the PR unasked.

## Delta mode (`--delta`)

Used by `/address-pr-comments` step 6, right after it pushes, while GitHub CI runs. The full
eight-leg round runs **once**, when the PR first goes ready; fixes for review comments get delta
rounds only, and nothing re-runs before merge.

- Diff: the commits listed in the caller's `$D/commits.txt` (`git diff <first>^ <last>`), written
  to `$SCRATCHPAD/prepr.delta.diff`; `$D` (whole branch) as context. No local build or full suite.
- Legs: `pr-review-bugs` + `pr-review-reach` + `pr-review-design`, plus `pr-review-spec`
  (description check only) in PR mode, then verifiers. Same frozen template and the delta-round
  extra line from "Fix loop"; the fix-completeness and probe lines always apply.
- **Two delta rounds maximum** per `/address-pr-comments` run. Round 2's leftover 🔴/🟡 are not
  fixed: list them under `needs owner decision` with "follow-up ticket".
- Never writes the clean marker (only a full or gate round does).

## Quick mode (`--quick`)

A cheap check while work is in progress. It is **never** a substitute for a full round before a
push, `gh pr ready`, or the clean marker.

- Steps 0 and 1 as normal, but skip the call graph (the `Graph:` line reads `unavailable (quick
  mode)`) and skip the loop-state block.
- Step 2 runs **four** agents only: `pr-review-scout` (already run in step 1), `pr-review-bugs`,
  `pr-review-reach`, `pr-review-guidelines`. Same frozen template, same extra lines.
- Step 3: verifiers only for 🔴 and 🟡 candidates; 🔵 and ❓ are reported unverified under
  `unverified:`.
- Step 4 report header reads `### Quick pre-PR review (NOT a clean gate)`. Never write the clean
  marker; delete nothing either (an existing marker stays as-is, since HEAD comparison already
  invalidates it). Instead of `No issues. Ready for PR.`, say `No issues in quick legs. Run
  /pre-pr-review before pushing.`
- List the legs not run: `not run (quick): history, prior-art, comments, spec, design`.

## Fix loop (`--loop`)

One invocation = **one round**: review, fix, write state, stop. The next round starts in a **fresh
context** (`/clear`, then the same command again, or `~/.claude/bin/prepr-loop` which runs each
round as its own `claude -p`). Never run a second round in the same context: every round's agent
output would stay in the main context and be re-read on every later turn.

**Round kinds** (`KIND` from step 0):

| kind  | legs | diff the legs get |
|-------|------|-------------------|
| full  | all eight + scout + verifiers | whole branch (`$D`) |
| delta | `pr-review-bugs` + `pr-review-reach` + `pr-review-design` (+ `pr-review-spec` in PR mode, description check only) + verifiers | fixes since last round (`prepr.delta.diff`); `$D` as context |
| gate  | same as full | whole branch |

A delta round uses the frozen template with `Diff: <delta path>` and adds one allowed extra line:
**"This diff is the fixes made since the last review round. Full branch diff for context: <D>.
Review every line of the delta; read the full diff only for context."** The fix-completeness line
from step 2 always applies to a delta round. This is not narrowing to last round's findings: the
delta is all of the new code, reviewed unanchored.

**Reviewer comments arrive while the loop runs** (PR mode, e.g. Copilot on the draft PR): every
round re-fetches `prepr.prior-comments.md`. Comments not seen in an earlier round (keep their ids in
`$S/seen-comments`) become candidate findings: one `pr-review-verifier` each, fixed like any other
finding when ≥75. Draft replies into `$S/replies.md`; post nothing. For each verified comment the
loop had **not** already reported, append one line to `$LESSONS` (create the dir if needed):
`- <class of bug, one sentence> (e.g. <path> in PR #<n>, found by <reviewer>)`. Skip a class
already listed.

**Scope is frozen once round 1 starts.** A fix closes a finding in the existing diff; it never
adds behaviour, config, or a refactor the finding did not require. A finding whose fix would add
any of those is listed under `needs owner decision` with the default recommendation "follow-up
ticket", not fixed. A finding in code the diff did not touch is a follow-up, not a fix. (Batch B
ran six rounds partly because mid-review owner decisions kept adding code each round re-reviewed.)

**What gets fixed:** only 🔴 and non-latent 🟡, without asking. 🔵, `[latent]`, spec items graded
"blocks closing, not merging", `needs owner decision` items (including design `owner-decision`),
`manual check needed`, and `context gap` drafts are listed and **not** fixed.
Fix the class, not the instance: grep the diff for every other occurrence and fix those too, or say
why not.

**After fixing, write state** so the next round knows what to do:

```bash
echo "$N" > "$S/round"; echo "$TREE" > "$S/tree"   # tree snapshot taken BEFORE this round's fixes
cp "<this round's report>" "$S/round-$N.md"
```

and write `$S/next`:
- this round found 🔴/🟡 and fixed them → `delta`
- delta round found no 🔴/🟡 → `gate`
- gate round found no 🔴/🟡 (and no `ticket-closure blockers`) → `done`; write the clean marker
- gate round found 🔴/🟡 → fix, then `delta`

**Stop and ask the user** (write `stop` to `$S/next`, say why) when:
- this is the **second** gate round that found a 🔴 in code the fixes did not touch: new bugs in
  old code after two gates means scope or design, not polish;
- round 6 is reached without `done`;
- any file under review has grown more than 30% since round 1 (`git diff --stat "$MB"`).

End every round with one line: `round <N> (<kind>): <totals>. leaked-from-earlier: <n> (<top cause>). next: <next>` and, unless next is
`done` or `stop`, `run: /clear then /pre-pr-review <same args>`.
Do not build or typecheck — the repo's hooks and CI do that.
