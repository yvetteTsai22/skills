---
name: perts-linear-issue
description: Write a Linear issue for a bug, defect, or failure using the PERTS format (Problem, Error code, Root cause, Troubleshooting steps, Solution). Use when filing or rewriting a bug ticket in Linear, or when a session's investigation needs to become a ticket someone else can read.
---

# PERTS — Linear issue format

Linear tickets are read at a glance by people who did not do the investigation.
A fixed section order lets a reader jump straight to the part they need; long
prose buries the actionable half.

## When to activate

Use for any Linear write **about an issue**: a bug, defect, regression, or
failure.

Do not use for feature requests, task tickets, test-plan tickets, review
comments, or status updates. Those just stay terse. PERTS is for something that
went wrong.

## Two rules that apply to every Linear write

1. **English, always** — bodies, titles, comments, every field, regardless of
   the language of the conversation you are having. Linear is a shared
   workspace read by people who were not in that conversation. A Chinese
   comment posted to a ticket gets deleted on sight.
2. **Short.** Push evidence, transcripts, and verification detail into a
   resolution comment. The body carries the reasoning, not the proof.

## The five sections

One `##` heading each, in this order, no others.

**## Problem** — what is wrong, what was expected instead. Name the concrete
artifacts: ticket, PR, repo, commit SHA, timestamp. Include the smallest
contrast that shows it is a defect ("this input works, that one does not").

**## Error code** — the error code, or the error message quoted verbatim if
there is no code. Either satisfies this section. If there is genuinely
neither, write it out — `None — no exception raised` — and say what the
evidence actually is. **Never drop the section.** Many real bugs are failures
of absence: nothing threw, nothing logged, the thing simply did not happen. An
empty E section is information, not a gap.

**## Root cause** — the cause if you know it. If you do not, write
`Not determined` or `Not confirmed` and then say:
- what you ruled out, and what evidence ruled it out;
- what hypothesis survives, marked as a hypothesis.

Do not assert a cause you have not verified. A ticket that guesses confidently
sends the next reader down your dead end.

**## Troubleshooting steps** — a numbered list of what you actually did, in
order. Include what you could not do and why (an unavailable log, a missing
permission) — that tells the next person where to start.

**## Solution** — the fix, or the next concrete step toward it. If the cause is
unconfirmed, this section is the experiment that would confirm it, written so
someone else can run it: exact command, exact ticket, exact order of actions.
Name anything that must be avoided and why.

## Steps (in this order, none optional)

1. Draft the title and body with the five sections above.
2. Run the draft through the `/ste80-humanizer` skill. **Run it even when the
   draft already looks short and plain.** "It's already plain" is exactly the
   judgement this step replaces. Keep the five headings, their order, quoted
   error text, code, identifiers, and the `Related:` line exactly as they are;
   humanize the prose only.
3. Only now call `save_issue` / `save_comment`.
4. In your reply to the user, report the humanizer edits by rule number (e.g.
   `§8, S1, S6`), or `humanizer: no changes`. A reply with no humanizer line
   means step 2 was skipped.

## Closing lines

End with `Related:` and the ticket identifiers, if any. Linear expands a bare
`MEE-123` into a link automatically — do not paste full URLs.

## Template

```markdown
## Problem

## Error code

## Root cause

## Troubleshooting steps

1.

## Solution

Related: MEE-000
```

## Title

One line, present tense, stating the failure — not the area. Prefix `🐛`.

- Good: `🐛 A changes_requested review can arm no rework dispatch at all`
- Bad: `🐛 Rework bug`, `🐛 Problem with reviews`

## Worked example

MEE-667 and MEE-668 are both written this way. Both carry
`None — no exception` under Error code and an unconfirmed Root cause, which is
what an honest ticket looks like when the symptom is something not happening.
