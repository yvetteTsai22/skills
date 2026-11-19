---
name: writing-pr-review-comments
description: Use when leaving review comments on a GitHub or GitLab pull request, or when a review has produced findings that need to be attached to specific files and lines
---

# Writing PR Review Comments

## Overview

A review comment is read in a narrow box by someone who has not read your analysis. It has three parts, in this order: **what happens**, **why it happens**, **what to do**. Anything else is noise.

## The recipe

Every comment is exactly these parts, in order:

**0. Severity marker.** A coloured circle and the severity word, on their own line: `🔴 **Critical**`. The circle is the scan target in a long thread; the word carries the meaning for anyone reading in plain text, in an email notification, or without colour vision. Never the circle alone.

**1. Consequence.** One sentence naming the concrete bad outcome, in words the author would use. This is the opener. No jargon term in the first sentence, no category name, no severity label.

**2. Mechanism.** The specific facts that produce it: line numbers, the two things that combine, what is missing. Cite lines you actually read.

**3. The fix**, under a literal `Fix suggested by claude:` line. One action per line, joined by `and`. No prose paragraph.

Optional 4th part: a one-line command that would settle the question at runtime.

```
🔴 **Critical**

If `apply_sandbox` throws here, the Job stays live WITHOUT its sandbox, and the run still reports it as a success.

Two separate causes: the Job was already written with the base spec at lines 85-90 and nothing undoes that write; and lines 87/90 appended the name to `created` before this call, so `provision_complete` lists it as created even though the `except` below also records it in `failed`.

Fix suggested by claude:
delete the Job when apply_sandbox fails on a sandbox=True target,
and move the created/updated append to after apply_sandbox returns,
and report the deleted names separately from the ones where the delete also failed.
```

## Severity markers

| Marker | Meaning | Author's next move |
|---|---|---|
| 🔴 **Critical** | Blocks merge | Fix before this lands |
| 🟠 **High** | Should fix before merge | Fix, or argue it down explicitly |
| 🟡 **Medium** | Worth fixing | Their call, with a reason either way |
| 🟢 **Low** | Optional, nit | Ignore freely |

Pick the level by **what the author has to do**, not by how interesting the finding is. A marker that overstates costs you the next one: if 🔴 turns out to mean "I felt strongly", it stops meaning "stop".

Use one marker per comment and nothing else decorative: no emoji in the prose, none in the fix list, none as section bullets. The marker works because it is the only symbol in the comment.

## Name the outcome, not the category

Security and reliability vocabulary compresses a mechanism into a term the author may not share. The term belongs in your own notes; the comment gets the mechanism.

| Instead of | Write |
|---|---|
| "This fails open." | "If X throws, the Job stays live without its sandbox and still reports success." |
| "TOCTOU." | "The value can change between the check on line 40 and the write on line 58." |
| "Unbounded." | "One slow response holds the worker until the process restarts." |
| "This is a footgun." | "A caller who omits the flag gets the unencrypted path with no warning." |
| "Fails silently." | "Nothing errors and nothing is logged. The board looks provisioned." |

The test: could the author act on this sentence without knowing your term? If not, replace the term with what it stands for.

## Never hard-wrap prose

GitHub and GitLab comments render as Markdown **with hard line breaks enabled**: a single newline becomes a visible `<br>`. Wrapping prose at 72 or 80 columns, the way you would in a code comment, puts line breaks in the middle of sentences in the rendered comment.

- Prose paragraph: **one line**, however long. Let the box wrap it.
- Blank line between paragraphs.
- The `Fix suggested by claude:` list: one line per action. Those breaks are semantic and intended.
- Fenced code blocks: wrap normally, they are preformatted.

## Write it plainly

Review comments are read fast, by someone who did not do your analysis. Rhetorical shape slows that down, and it reads as generated. Six habits to drop, in rough order of how much they cost:

**Antithesis and mirrored clauses.** "The one key the code calls the security boundary is the one key not parsed at the boundary." "A missing Job fails loudly; an unsandboxed one fails silently." The shape sounds insightful, but the reader has to unfold two halves to get one fact. State the fact, then the consequence, in separate sentences.

**Em dashes.** Pick real punctuation instead. A full stop splits two thoughts. A colon introduces the thing that follows. Parentheses hold a genuine aside. A comma is often enough. Swapping every em dash for a comma just relabels the same pause.

**Mid-sentence capitals and bold for emphasis.** `stays live WITHOUT its sandbox`, `with NO target_tags`. If a word carries the weight of the sentence, restructure so its position carries it. Save bold for the severity word.

**Three-part rhythm.** "no error, no log line, and the board looks fine." Two facts and a cadence. List what is true; stop when you run out.

**Stacked parentheticals.** Three asides in one paragraph means three decisions not made about whether the content belongs. Promote it to a sentence or cut it.

**Definitional flourishes.** "This is not a configuration problem, it is a trust problem." Restates what you already said, in a frame. Delete the sentence and nothing is lost.

The check: read the comment aloud. Anywhere it sounds like it wants to be quoted, rewrite that sentence flat.

## Choosing the anchor

Only lines inside a diff hunk are commentable: changed lines, plus the context lines shown around them.

1. **Anchor on the new code that introduces the problem**, not on a pre-existing line it combines with. A line that was safe before this PR and is dangerous now is a *cross-reference*, not the primary anchor.
2. **If the real site is not in the diff**, anchor on the nearest in-diff line and name the other file in the body. Do not skip the finding.
3. **One finding, one primary comment.** Related files get a two-line pointer back to it. Three full copies of the same argument leaves the author unsure where to reply.

Verify the line number against the file before posting; a comment on the wrong line costs the author more time than no comment.

## Quick reference

| Part | Rule |
|---|---|
| Line 1 | Severity marker: circle + word, e.g. `🔴 **Critical**` |
| Sentence 1 | The concrete outcome, no jargon |
| Middle | Mechanism with real line numbers |
| Fix | Under `Fix suggested by claude:`, one action per line |
| Prose | One line per paragraph, never hard-wrapped |
| Style | No em dashes, no mirrored clauses, no mid-sentence capitals |
| Anchor | The new code that introduces it, inside a diff hunk |
| Duplicates | One primary comment, short pointers elsewhere |
| Footer | None. No `🤖 Generated with Claude Code` or other attribution line; that note is for commits and PR descriptions, not comments |

## Common mistakes

**Spending the sentence on the severity.** `HIGH: the reconcile fails open.` The marker line already carries the level. Repeating it in prose costs the one sentence the author is guaranteed to read. Put the level on its own line, then spend sentence 1 on the outcome.

**A bare circle.** `🔴` with no word renders as nothing in a plain-text notification and as an unlabelled dot to a colourblind reader. Always `🔴 **Critical**`.

**Restating the code.** `This calls apply_sandbox after update_job.` The author wrote it. Say what that ordering costs.

**A fix paragraph instead of a fix list.** Prose hides how many separate changes are being asked for. Three lines joined by `and` makes it countable.

**Writing a line you would be pleased to have quoted.** That instinct produces antithesis, triads, and closing flourishes. The comment is a work item, not a paragraph.

**Hedging the ask.** "It might be worth considering whether..." If it is worth a comment, it is worth a sentence in the indicative.

**Claiming what you did not verify.** If the conclusion depends on runtime behavior, say so and give the command that settles it, rather than asserting it.
