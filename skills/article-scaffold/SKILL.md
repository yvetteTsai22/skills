---
name: article-scaffold
description: Builds an article skeleton (opening, structure, ending) from an angle and material already in hand, then runs a peak-end check. Use when outlining a blog post or article before drafting, choosing how to open or end a piece, or 搭骨架、選開頭結尾、峰終檢查.
---

# Article Scaffold

Input: an angle (one sentence) and the material: stories, numbers, quotes, opinions. No angle yet? Find one first (`angle-finder`); this skill only arranges material, it never invents it.

## 1. Pick the language file

Detect the language the piece will be written in (the user's draft or request; else the material). Read exactly one file beside this one:

- Chinese: [`zh.md`](zh.md)
- English, or any other language: [`en.md`](en.md)

The file holds the template menus and the selection rules. Everything below applies to both.

## 2. Inventory the material

List every usable item, one line each, tagged: `story`, `number`, `quote` (the author's own words, verbatim), `opinion`, `counterpoint`, `doubt`. Mark the single **peak**: the item a reader is most likely to retell. It is usually a concrete moment with a number or a spoken line, rarely an opinion.

Done when every item is tagged and exactly one is marked peak.

## 3. Choose opening, structure, ending

Use the selection rules in the language file. Choose from the material's shape, not from taste: each choice must name the inventory items that make it fit. A template whose condition the material does not meet is out, however good it sounds.

## 4. Write the skeleton

```
ANGLE: <one sentence>

OPENING — <template>
  Why: <which inventory items make it fit>
  Beats: <1–3 lines, using real items>

SECTION n — <role in the structure template>
  Why: ...
  Beats: <items placed here>
  ... (one block per section)

ENDING — <template>
  Why: ...
  Beats: ...

PEAK-END CHECK
  Peak: section <n> — <item>
  End: <the last thing the reader sees>
  Verdict: pass | fix
  Fix: <only if fix: which item moves where, or which ending replaces which>
```

Every inventory item lands in one section or is listed under `UNUSED` with a reason. Facts not in the inventory stay out.

## 5. Peak-end check

Readers remember a piece by its most intense moment and its last moment, and barely by its length (Kahneman's peak-end rule). Check:

1. **Peak placed:** the peak item sits in the opening or the final third, never buried mid-piece behind setup.
2. **End lands:** the last line is something concrete the reader can carry away (a callback to the opening, a scene, a question, the author's doubt), not a summary of what was just said.
3. **Peak and end connect:** the ending reuses an image, number or line from the peak or the opening.

Verdict `pass` only when all three hold. On `fix`, name the concrete move (for example "move Ada's Monday-morning line from section 3 to the opening; end on the lunch that came back") and rewrite the skeleton once with the move applied.

## Hand-off

Return the final skeleton. When drafting follows in the same session, the draft keeps the skeleton's order and quotes the author's `quote` items verbatim.
