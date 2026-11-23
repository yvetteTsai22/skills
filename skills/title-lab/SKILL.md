---
name: title-lab
description: Writes 5+ candidate titles for a finished skeleton or draft, each tagged with the title type it uses, so the author picks one. Use after outlining and before drafting, when a piece needs a title or headline, or 想標題、起標題、標題候選.
---

# Title Lab

Input: the angle (one sentence) and the skeleton or draft (`article-scaffold` output works). No angle yet? Find one first (`angle-finder`). A title only promises what the material delivers; it never adds a fact.

## 1. Pick the language file

Detect the language the piece is written in (the draft or skeleton; else the user's request). Read exactly one file beside this one:

- Chinese: [`zh.md`](zh.md)
- English, or any other language: [`en.md`](en.md)

The file holds the title types and the platform rules. Everything below applies to both.

## 2. Collect the hooks

List the material a title can stand on, one line each, tagged: `number`, `person` (who it is about or for), `contrast` (before/after, expected/actual), `quote` (the author's words, verbatim), `payoff` (what the reader gets). Mark the peak item from the skeleton if one exists.

Done when every hook points at a real item in the skeleton or draft.

## 3. Draft candidates

Write one candidate per title type in the language file whose material condition the hooks meet. Skip a type whose condition fails; a forced type produces a title the body cannot pay off.

At least 5 candidates, from at least 3 different types. Fewer than 3 types fit? Write two variants of the strongest type and say why the others were skipped.

## 4. Check each candidate

Strike a candidate that fails any check, then replace it so the count stays at 5 or more:

1. **True:** every number, name and claim is in the material.
2. **Paid off:** the body answers the question or delivers the promise within its first third.
3. **Platform:** passes the platform rules in the language file.
4. **Front-loaded:** the most specific word sits in the first half.

## 5. Output

```
ANGLE: <one sentence>

1. <title>
   Type: <type name from the language file>
   Hook: <the material item it stands on>
...

PICK: <number> — <one line: why it fits this angle and platform>
```

The author chooses; `PICK` is a recommendation. When drafting follows in the same session, the draft uses the picked title and its opening pays off the title's promise.
