---
name: content-preflight
description: Checks a writing topic before drafting with three go/no-go questions (reuse, sameness, real goal), each with a verdict and reason, then a write/rework/drop call. Use before starting a blog post, article or social post, when a topic might be the one everyone already wrote, or 動手前三問、動筆前檢查、這題值不值得寫.
---

# content-preflight

Three questions decide whether a topic is worth the hours before anyone drafts it. Each gets a verdict (`pass` or `fail`), a one-line reason that cites the author's own material, and, on `fail`, a concrete fix to the topic.

## 1. Pick the language file

Detect the language of the topic or the author's notes. Read only one file:

- Chinese: [`zh.md`](zh.md)
- English or anything else: [`en.md`](en.md)

The file holds the three questions as that tradition phrases them, the pass bar for each, and the usual fixes.

## 2. State the topic

Write the topic as one sentence, then the **default take**: the piece a reader expects from that headline, the one most posts on the topic already are. Done when both lines exist.

## 3. Ask the three questions

Run all three, in order, from the language file:

1. **Reuse**: can this piece be reused many times (cited, linked, cut into other formats, built on by the next piece)? A one-off that dies with the news cycle fails.
2. **Sameness**: is the planned take the default take? Same take, same structure, same examples as everyone else fails.
3. **Real goal**: what is the piece actually for: what the reader should know or do after it, and what the author needs from it? A goal that is only "write something good about X" fails.

For each: the verdict, the reason (quote or name the author material it rests on), and on `fail` the smallest change to the topic that would make it pass. Never invent material to make a question pass; when the author gave nothing to judge by, the verdict is `fail` with reason `no material`, and the fix is the question to ask the author.

Done when all three rows have a verdict, a reason and, on every `fail`, a fix.

## 4. Output

| # | Question | Verdict | Reason (author material) | Fix to the topic |

Then the call, one line:

- **write**: all three pass.
- **rework**: one or two fail and their fixes are doable with the material in hand. Restate the topic with the fixes applied.
- **drop**: the sameness question fails and no fix the material supports gets away from the default take, or the real goal fails and the author cannot name one.

## Writing the piece in the same run

Run steps 2-4 first, even when only the piece is asked for. On **rework**, write the reworked topic, not the original. On **drop**, say so and stop instead of drafting. The default take appears in the piece at most once, as the view it answers.
