---
name: viral-teardown
description: Tears down 20+ viral pieces (爆款) on one keyword to find the patterns they share, each pattern cited by the pieces it appears in, then feeds proven patterns into other writing skills' zh.md / en.md examples. Use when analysing top posts before writing, 拆解爆款, 找共同模式, 對標, building a swipe file, or refreshing a skill's examples.
---

# viral-teardown

Find what 20+ proven pieces repeat, so a new piece copies the parts that already worked. A **pattern** is an element that recurs across pieces: a title shape, an opening move, a structure, a cover, a hook, a closing.

## 1. Pick the language file

Detect the language of the corpus or the request. Read only one file:

- Chinese: [`zh.md`](zh.md)
- English or anything else: [`en.md`](en.md)

It lists where to pull top pieces, what to tag, and examples for that language. Write output in that language.

## 2. Build the corpus

One keyword, one platform, sorted by most popular (hottest, most shared, top all-time). Number each piece `P1..Pn` with title, link or source, and its popularity number.

Done when: at least 20 pieces, all from one keyword. Fewer than 20 given or reachable: say how many, ask for more, and run only if the author says go; mark the output `small corpus (n=…)`.

## 3. Tag every piece

For each piece fill the tag set from the language file (title shape, opening, structure, emotion, format, closing). Quote short evidence, never paraphrase into a pattern yet.

Done when: every piece has every tag filled, or `n/a` with a reason.

## 4. Group into patterns

Merge equal tags across pieces. Keep a pattern when it appears in at least 3 pieces or 15% of the corpus, whichever is larger. Then read the top-voted comments of the 3-5 biggest pieces for **gaps**: what readers asked for that no piece gave.

## 5. Output

A table, sorted by count:

| # | Pattern (one line) | Kind (title/opening/structure/…) | Count | Pieces (P-numbers) | Shortest example quote |

Then: the gaps list, each with its comment source; and 2-3 lines on how to combine the top patterns into the next piece (about 70% proven patterns, the rest from a gap or the author's own material).

Done when: every pattern row lists the P-numbers it appears in and the count matches them; no pattern rests on a single piece.

## 6. Feed patterns into other skills

When asked to refresh examples, or when a pattern clearly fits a skill:

1. Map each pattern kind to its skill: angle → `angle-finder`, opening/structure/ending → `article-scaffold`, golden lines → `golden-line`, interview questions → `interview`.
2. Open that skill's `zh.md` or `en.md` (same language as the corpus only).
3. Add or replace one example under the matching section. Mark it `（爆款拆解，n=…）` / `(viral teardown, n=…)` with the keyword, and keep it to 1-3 lines. Write the pattern as a reusable shape with one short quoted instance, not a copy of a whole piece.
4. Drop an older example only if the new one covers the same move better; keep each file's size about the same.

Done when: each edited file has the new example in the right section and no section has two examples of the same move. One commit per skill edited.
