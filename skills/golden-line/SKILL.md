---
name: golden-line
description: Polish a finished draft's golden lines (金句) before ste80-humanizer runs. Measures the highlight rate (畫線率, target 10–40%), caps AI tells (not-X-but-Y, triads, one-line closers), and marks the sentences to keep so the humanizer leaves them alone. Use after a first draft, or when a pipeline reaches the polish step before de-AI.
---

# golden-line

Pass over a finished draft. Make a few sentences worth underlining, cap the AI tells, and **mark** the sentences you keep on purpose so the next step (`ste80-humanizer`) does not flatten them. This skill always runs before the humanizer, never after.

## 1. Pick the language file

Read the draft and decide its language by the body text, not the title. Read exactly one file:

- Chinese draft: [`zh.md`](zh.md)
- English draft: [`en.md`](en.md)

Done when one file is read and the other is not.

## 2. Measure

Split the body into sentences (a heading is not a sentence). Count:

- **Highlight sentences**: sentences a stranger would underline or quote. They stand alone and carry a concrete noun, number or scene. Be strict; a summary that restates the paragraph does not count.
- **Highlight rate** = highlight sentences / total sentences × 100.
- **AI tells**, each listed with its sentence:
  - *not-X-but-Y*: "not X but Y", "not just X, it's Y", 「不是…而是…」, 「不僅…更…」, a contrast split across two sentences.
  - *triad*: a list of exactly three parallel items or clauses.
  - *one-line closer*: a short last line of a section that restates the section.

Done when you have the four numbers (sentences, highlight sentences, rate, tells by kind).

## 3. Polish

Work section by section with the language file's patterns:

- Rate under 10%: rewrite flat sentences that already hold a concrete detail into golden lines. Start with the opening and the ending (peak-end rule: readers remember the peak and the end).
- Rate over 40%: the draft is all slogans. Turn the weakest lines back into plain narration.
- AI tell caps, after your edits:
  - one-line closer: at most **one per section**, and only after a long build-up.
  - not-X-but-Y: at most one per piece, and only when the reader really holds X and the text has already said so.
  - triad: at most one per piece, and its third item turns.
- Use only facts already in the draft. Change words, not facts.

Done when the rate is in 10–40% and every cap holds.

## 4. Mark the keepers

Wrap each sentence you crafted or chose to keep, as it stands, in the keep marker:

```
<!-- gl:keep -->The sentence, exactly.<!-- /gl:keep -->
```

Rules: one sentence per marker pair, never spanning a paragraph break, never nested. Mark only golden lines and deliberate rhetorical choices (the one allowed closer, the one allowed contrast), typically 5–15% of sentences. HTML comments are invisible when Markdown renders, so a marked draft can still be published.

## 5. Hand off to ste80-humanizer

`ste80-humanizer` edits every sentence it sees, so hide the keepers from it with [`keep.py`](keep.py) (Python 3, no dependencies):

```bash
python3 keep.py protect draft.md > draft.protected.md   # each keeper becomes [[GL-KEEP-01]]; map saved to draft.md.keep.json
# run ste80-humanizer on draft.protected.md -> draft.human.md
python3 keep.py restore draft.md.keep.json draft.human.md > draft.final.md
python3 keep.py check draft.md draft.final.md            # exit 1 lists any keeper that changed or went missing
```

Tell the humanizer: "Tokens like `[[GL-KEEP-01]]` are identifiers. Keep each one exactly, in place, as its own sentence." If no shell is available, do the same by hand: swap each keeper for its token before the humanizer, swap back after, and compare.

Done when `check` passes (exit 0). If the humanizer dropped a token, `restore` names it; put the keeper back where it stood in `draft.md` and run `check` again.

## 6. Report

Return the polished draft (with markers, or the final text after step 5), then:

```
sentences: N | highlights: H | rate: R% (target 10–40) | tells: not-X-but-Y a, triad b, closer c (per section max 1) | keepers: K
```

and one line per change: the old sentence, the new one, and the pattern used.
