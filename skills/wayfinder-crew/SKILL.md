---
name: wayfinder-crew
description: Wayfinder with the usual add-ons baked in — chart or work a Linear decision map (work or personal workspace), terse caveman replies, cavecrew subagents for code lookups/edits/reviews, and an optional 繁體中文 illustrated explainer for grilling tickets. Use in place of invoking wayfinder + cavecrew + illustrating-in-chinese separately.
disable-model-invocation: true
argument-hint: "[work|personal] [loose idea | map id/URL] [ticket id] [圖解|no-圖解] [no-review]"
---

# Wayfinder crew

One entry point for three skills the user always stacks:

| Layer | Source | What it adds |
|---|---|---|
| Protocol | `wayfinder` | map / tickets / fog / one ticket per session |
| Voice + delegation | `caveman` + `cavecrew` | terse chat, compressed subagent output |
| Readability | `illustrating-in-chinese` | 中文圖解 page for grilling tickets |

## Step 0 — load the base protocol (always)

`wayfinder` is `disable-model-invocation`, so the Skill tool cannot load it. **Read `~/.agents/skills/wayfinder/SKILL.md` in full and follow it as the protocol.** It is the source of truth for the map body, ticket types, fog of war, out-of-scope, and both invocation modes. Everything below only fills its gaps or overrides it; where this file is silent, wayfinder wins.

Mode from `$ARGUMENTS`:
- a loose idea → **Chart the map**
- a map id/URL (optionally + ticket id) → **Work through the map**
- `圖解` / `no-圖解` → force the illustration on / off for this session
- `work` / `personal` → Linear profile (see Tracker)

## Tracker: Linear, work or personal (fills wayfinder's "tracker doc")

**Read `~/.agents/crew/LINEAR-PROFILES.md` first** and pick the profile there (arg `work` / `personal`, else auto-detect). It holds tool prefix, workspace check, Wayfinder label ids per workspace, and shared ops (blocking, claim, resolve, refer by name). Wayfinder-specific on top of it:

- Wherever wayfinder says `wayfinder:<type>`, apply the matching Wayfinder group child from the profile table.
- Spec / Tickets / Implementation children are not wayfinder ticket types — don't apply them unless the user names them (Implementation: only when the map's Notes carry execution).
- Find maps: `<linear>list_issues label:<Map id>`. **Before charting**, check for an existing map on the same destination — don't open a duplicate.
- Frontier query: `<linear>list_issues parentId:<map>` → open, unassigned, all blockers closed.
- Resolve: after the shared resolve op, patch the map's Decisions-so-far with `[<ticket title>](url): <gist>`.
- Map reaches its destination and that destination is a spec → suggest `/to-spec-crew <map>` in one line; then `/to-tickets-crew <spec>`.

## Sub-skill mapping (wayfinder names skills that aren't installed)

| Wayfinder says | Do instead |
|---|---|
| "grilling" | Skill `grill-me` |
| "domain-modeling" | Skill `codebase-design` when the ticket is about code shape; otherwise fold domain terms into the grilling |
| "research" (in-repo facts) | `caveman:cavecrew-investigator` subagents, 2–3 in parallel for broad questions |
| "research" (docs / third-party / web) | `general-purpose` subagent told to use `ctx7` / `deep-research`; must return findings ≤ 300 words, caveman style |
| "prototype" | Build inline; a 1–2 file stub may go to `caveman:cavecrew-builder` on a throwaway `prototype/<name>` branch |
| task (AFK) touching ≤ 2 known files | `caveman:cavecrew-builder` |
| review a prototype / diff | `caveman:cavecrew-reviewer` |

Cavecrew rules carried over: don't hand builder an unknown file (investigate first); builder `too-big.` means do it in main thread; paraphrase cavecrew output before showing it to the human.

## Voice

- **Chat replies: caveman `full`**, in the user's language (usually 中文). Drop filler, keep technical terms, ids, and exact errors verbatim. Normal clarity for irreversible actions and for grilling questions whose options would be ambiguous as fragments.
- **Grilling questions**: one question at a time, lead with the recommended option, ≤ 4 options, each ≤ 1 line.
- **Tracker writes are not caveman.** Map body, ticket bodies, resolution comments: short plain prose, full sentences. Language by Linear profile: work → English; personal → 繁體中文（台灣書面語）.

## 圖解 for grilling tickets (optional layer)

When working a Wayfinder › Grilling ticket, after claiming and zooming, **before the first question**, decide:

**Build it when any holds:** the ticket weighs ≥ 2 competing routes; the mechanism spans ≥ 3 components or a state/event flow; the user passed `圖解`; or the user asks mid-grill "看不懂 / 畫一下".
**Skip when:** single-axis yes/no question, pure naming/preference, `no-圖解`, or a research/task ticket.

If building:
1. Invoke Skill `illustrating-in-chinese` (it loads `artifact-design` and draws the figure with `archify`) and follow it. Source = the ticket body + the closed tickets it depends on + relevant code.
2. Nothing is decided yet → closing block is **修法** (trade-off between the ticket's routes), never 驗收. Mark the route you'll recommend, don't pretend it's chosen.
3. Publish as an Artifact, give the link in one line, then start grilling with the page as shared reference.
4. After the ticket resolves, update the same artifact only if the user asks (closing becomes the chosen route). Put the artifact link on the Linear ticket only if the user asks — it's a private page.

Charting mode: no 圖解 by default; offer it in one line for the map itself if the destination is hard to picture.

## Code review before PR (situational)

Wayfinder produces decisions, not code — but code does happen: an AFK **Task** ticket, a map whose
Notes carry execution into the map (Wayfinder › Implementation tickets), or the user saying the
ticket's code is written.

**Run Skill `pre-pr-review` when all hold:**
- the working branch has changes vs `main` (commits, staged, unstaged, or untracked), **and**
- that code is meant to ship via a PR (not a throwaway), **and**
- no PR is open for the branch yet (`gh pr view` fails). PR already open → suggest `/pr-review <n>` instead.

**Skip:** `prototype/*` and `research/*` branches (throwaway assets — linked, never merged); pure
decision tickets with no diff; the user said `no-review`. Doc-only or config-only diff → ask in one
line instead of running it (it's five agents; not free).

**When:** after the code is done, **before** recording the resolution and before suggesting a PR.
Findings → ask whether to fix. Fix loop stays in this session; re-run `pre-pr-review` once after
fixes if any 🔴 was found. Commit, push and open the PR on the feature branch without asking; merge only if the repo opts in via `AUTONOMY.md`.

Resolution comment on the ticket: one line on review outcome (`Pre-PR review: clean` or
`Pre-PR review: N findings, fixed` / `N open`). No finding details in Linear.

## Session end

Report (caveman): ticket resolved (title + link), decision gist, tickets added / fog graduated / ruled out of scope, 圖解 link if made, pre-PR review totals if run, and the next frontier ticket by title. Still one non-research ticket per session.
