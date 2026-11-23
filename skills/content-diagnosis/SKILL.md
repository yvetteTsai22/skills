---
name: content-diagnosis
description: Diagnoses a published piece from its numbers: maps each signal (high opens but few shares, likes without follows, fast drop-off) to likely causes and one concrete change for the next piece. Use after publishing, when asked why a post flopped or stalled, 數據診斷, 復盤, 為什麼沒爆, or to plan fixes before writing again.
---

# content-diagnosis

Read the numbers a piece earned, name each **signal**, and turn it into a cause and a change the author makes in the next piece. The output is a fix list, not a report card.

## 1. Pick the language file

Detect the language of the piece or the author's notes. Read only one file:

- Chinese: [`zh.md`](zh.md)
- English or anything else: [`en.md`](en.md)

It holds the signal table for that language's platforms. Write the diagnosis in that language.

## 2. Collect the numbers

List each metric the author gave, with its value and a comparison point (the author's usual number, or the platform benchmark the language file gives). A number with no comparison point is marked `no baseline`.

No numbers given: ask for them once. Still none (for example a draft not yet published): run a **pre-mortem**. Read the piece, predict which signals it is likely to show, and mark every row `predicted`. Never invent a metric and present it as measured.

## 3. Match signals

For each metric that sits clearly above or below its comparison point, find the signal in the language file's table. A signal pairs two metrics (one high, one low) far more often than it rests on one; read them in pairs.

## 4. Check the piece

For each signal, open the part of the piece the table points to (title, first screen, middle, ending, call to action) and quote the line that confirms or rules out each cause. A cause with no line from the piece behind it is marked `unconfirmed`.

## 5. Output

A table, one row per signal:

| Signal (metrics and values) | Likely causes, most likely first | Evidence from the piece (quoted) | Change for next piece (concrete) |

A change is concrete when the author can do it in the next draft: "end with the Ohio clinic owner's call and one question to readers", not "write a better ending".

Then: the one change to make first, and why.

Done when: every metric from step 2 is either in a row or listed as "within normal range"; every row has at least one cause and one concrete change; one first change is named.

## Writing the piece in the same run

When the run asks for a new piece rather than a diagnosis, run steps 3-5 as a pre-mortem on the draft before finishing it, fix the predicted weak spots in the piece, and keep the diagnosis table out of the piece unless asked.
