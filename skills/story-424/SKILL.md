---
name: story-424
description: Turns an author's raw material into a story passage with the 4+3+2 method (4 steps for the skeleton, 3 points for the flesh, 2 moves to ignite), labeling every part and keeping the author's own words. Outputs an article passage or a short-video script. Use when the author has a story to tell inside a post or video, beside article-scaffold, or 講故事、4+3+2、故事段落、短影音腳本.
---

# Story 4+3+2

Input: one story the author lived or witnessed, in their own words (interview answers, notes, a draft paragraph). This skill shapes the story; it never invents facts, lines or feelings. Missing a piece? Ask the author one question, or mark the slot `MISSING`.

In the blog pipeline it runs at the scaffold step: `article-scaffold` places the story in a section, this skill writes that section's story.

## 1. Pick the language file

Detect the language the piece will be written in (the user's draft or request; else the material). Read exactly one file beside this one:

- Chinese: [`zh.md`](zh.md)
- English, or any other language: [`en.md`](en.md)

The file names the parts and gives the rules for each. The steps below apply to both.

## 2. Quote bank

List every line the author said that could go into the story, verbatim, one per line, numbered `Q1, Q2...`. Spoken lines and concrete details (numbers, objects, places, times) first. Use these words; paraphrase only to join them.

## 3. Build the parts

Fill each part named in the language file, in its order: first the 4 skeleton steps, then the 3 flesh points, then pick the 2 moves. For each part write one line and cite the quote ids it uses. A part with no material is `MISSING`, not made up.

Done when the conflict is one sentence with two sides, and the emotional peak cites at least one quote.

## 4. Write the output

Ask which form, or infer it from the platform: article (blog, newsletter, long post) or short video (Douyin, Reels, TikTok, Shorts, 小紅書 video).

**Article passage:**

```
STORY PLAN
  <part name>: <one line> [Q..]
  ... (every part from the language file)
  Order: <the told order, e.g. peak → background → conflict → turn>

PASSAGE
<the story, 150–500 words, each paragraph tagged at its end like ⟦conflict⟧ or ⟦peak · scene⟧>
```

**Short-video script:**

```
STORY PLAN (same as above)

SCRIPT
| Time | Part | Shot / on-screen | Voice-over or line |
| 0–3s | <the hook: conflict or peak first> | ... | ... |
| ...  | ... | ... | ... |
Total: 30–90s. One part per row. Spoken lines are the author's words.
```

Give both forms only when asked.

## 5. Check

1. Every part from the language file is in the plan, filled or `MISSING`.
2. Every tag in the passage or script names a part from the plan.
3. At least half the sentences that carry a fact use a quote-bank phrase; no fact outside the material.
4. The emotional peak is a scene (what a camera would catch), not an emotion word.

Fix and recheck once if any fails. Return the plan plus the passage or script.
