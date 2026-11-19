---
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr list:*), Bash(gh pr review:*), Bash(gh api:*), Bash(gh search:*), Bash(gh issue view:*), Bash(git log:*), Bash(git diff:*), Bash(git blame:*), Bash(git fetch:*), Bash(git rev-parse:*)
description: Review someone else's pull request and leave inline comments
disable-model-invocation: false
---

Review the given pull request and leave the findings as inline comments.

Adapted from the official `code-review:code-review` flow. Same eligibility gate, same parallel review, same confidence filter. It differs in one place: the findings are posted as **inline comments anchored to file and line**, not as a single summary comment.

**REQUIRED SUB-SKILL:** Use `writing-pr-review-comments` for the wording, severity markers, and anchor choice of every comment you post. Do not invent a format here.

Follow these steps precisely.

## 1. Eligibility

Use a Haiku agent to check whether the PR (a) is closed, (b) is a draft, (c) does not need review (automated, or very simple and obviously fine), or (d) already carries a review from you. If any hold, stop.

## 2. Establish the real scope

Do this yourself, not in an agent, and before dispatching anything.

```
gh pr view <n> --json baseRefName,headRefName,changedFiles,additions,deletions
git fetch origin
git diff origin/<baseRefName>...HEAD --stat
```

The file count from `git diff` must equal `changedFiles`. If it does not, your local base branch is stale and the diff is silently wider than the PR. Re-fetch and reconcile before continuing. Never scope from a bare local branch name (`main...HEAD`); always `origin/<base>...HEAD`.

Reviewing code that is not in the PR wastes the author's time and destroys their trust in the rest of the review.

## 3. Gather context

Use a Haiku agent to return the file *paths* (not contents) of relevant CLAUDE.md files: the root one, plus any in directories the PR modifies. Use another to summarise the change.

## 4. Review in parallel

Launch 5 Sonnet agents. Each returns a list of issues with the reason each was flagged. Give each the scope from step 2 so none of them reviews outside it.

Use a narrow agent type: `code-reviewer` for a-c-d-e, `python-reviewer` (or the language's reviewer) for b. Do **not** use `general-purpose`. Its tool list is `*`, so every MCP server's schemas load into the agent before it reads a line of code, and the launch fails with `Prompt is too long`.

- **a.** Compliance with the CLAUDE.md files from step 3. CLAUDE.md is guidance for writing code, so not every instruction applies at review time.
- **b.** Read the diff and scan for obvious bugs. Stay inside the changes; do not pull in wider context. Large bugs only, no nitpicks.
- **c.** Read `git blame` and history of the modified code, and identify bugs in light of that history.
- **d.** Read previous PRs touching these files and check whether any review comment there also applies here.
- **e.** Read code comments in the modified files and check the change complies with the guidance in them.

## 5. Score confidence

For each issue, launch a parallel Haiku agent with the PR, the issue, and the CLAUDE.md paths. It returns 0-100. Give it this rubric verbatim:

- **0** Not confident. False positive that does not survive light scrutiny, or a pre-existing issue.
- **25** Somewhat confident. Might be real, might not; the agent could not verify. If stylistic, not explicitly called out in the relevant CLAUDE.md.
- **50** Moderately confident. Verified real, but possibly a nitpick or rare in practice. Not important relative to the rest of the PR.
- **75** Highly confident. Double checked and very likely real and hit in practice. The PR's approach is insufficient. Directly impacts functionality, or is named in the relevant CLAUDE.md.
- **100** Certain. Double checked and confirmed real, frequent in practice, evidence directly confirms it.

For issues flagged on CLAUDE.md grounds, the agent must confirm the CLAUDE.md actually says that.

## 6. Filter

Drop everything below 80. If nothing remains, stop.

**Exception:** a finding that is exploitable, destructive, or fails a security control open is reported even at 50, and reported as what it is: a mechanism you have verified statically and a runtime check that would settle it. These score low because they depend on runtime facts, not because they are unlikely. Say so in the comment rather than dropping it.

## 7. Verify what survives

For each surviving finding, open the file and confirm the line numbers and the quoted code yourself. An agent's line number is a claim, not a fact. A comment on the wrong line costs the author more than no comment.

## 8. Re-check eligibility

Repeat step 1. The PR may have moved while you worked.

## 9. Post

One review, containing one inline comment per finding, anchored per `writing-pr-review-comments`.

```
gh api repos/{owner}/{repo}/pulls/{n}/reviews \
  -f event=COMMENT \
  -f body='<one or two sentences: what you reviewed and the scope from step 2>' \
  -F 'comments[][path]=<file>' -F 'comments[][line]=<n>' -F 'comments[][body]=<comment>'
```

Only lines inside a diff hunk accept a comment. If a finding's real site is not in the diff, anchor on the nearest in-diff line and name the other file in the body.

Use `event=REQUEST_CHANGES` when any finding is 🔴 **Critical**, otherwise `event=COMMENT`. Never `APPROVE` from this command; approval is the human's.

The summary body stays short: what was reviewed, the scope, and the counts by severity. Do not restate the findings there; they are already inline.

## False positives

Do not report:

- Pre-existing issues, or real issues on lines the author did not touch
- Things that look like bugs but are not
- Nitpicks a senior engineer would not raise
- Anything a linter, typechecker, or compiler catches (imports, types, formatting, broken tests). Assume CI runs separately; do not run builds yourself
- General code quality (coverage, documentation, generic security posture) unless CLAUDE.md requires it
- Issues named in CLAUDE.md but explicitly silenced in the code (a lint ignore, for instance)
- Functionality changes that are plainly intentional or part of the broader change

## Notes

- Use `gh` for GitHub, never web fetch
- Make a todo list first
- Cite and link what you claim. When linking code, use a full-sha permalink or the preview will not render: `https://github.com/<owner>/<repo>/blob/<full sha>/<path>#L4-L7`, with at least one line of context either side of the line you mean
- Do not check build signal
