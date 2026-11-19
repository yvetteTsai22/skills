# Style presets

`engineering-notebook` is the default. Use it unless the subject clearly matches another row in the Choosing table below; only ask the user when two presets are genuinely close.

Each preset gives ground / ink / accent / semantic / display face / figure convention. Semantic colors are always separate from the accent; the accent never doubles as "good" or "bad".

Every preset still follows the theme-token rule in SKILL.md: the values below are the light set, and both dark blocks redefine the same complete set.

Figures are chosen by question (SKILL.md › The figure) and drawn inline in the preset's tokens. Each preset's "Figure" line styles the chrome around them — frame, caption, callouts, the 今天/改後 worked example. Only when a figure is an `archify` architecture diagram, pair it with this `meta.visual_preset`:

| Page preset | archify `meta.visual_preset` |
|---|---|
| `engineering-notebook` | omit (`classic`) |
| `blueprint` | `blueprint` |
| `diagnostic` | `signal-flow` |
| `textbook-plate` | `editorial` |

This is the only case where setting `meta.visual_preset` is right: the page style is the user's explicit style choice.

---

## 1. `engineering-notebook` — 工程筆記

Restrained, document-like. **The default preset** — use it unless the subject clearly calls for another.

**Best for:** completed work — a merged PR, a shipped refactor, conformance coverage, "here's what changed and why".

| role | light | dark |
|---|---|---|
| paper | `#f2f3f6` | `#0d0f16` |
| surface | `#ffffff` | `#161a25` |
| ink / ink-2 | `#151821` / `#495063` | `#e7eaf3` / `#a9b1c6` |
| rule | `#d2d7e3` | `#29303f` |
| accent | `#2f4f7f` steel | `#7ea6e2` |
| semantic | domain-native (PR: `#1a7f37` / `#8250df` / `#cf222e`) | `#3fb950` / `#a371f7` / `#f85149` |

Display Noto Serif TC 600. Figure: bordered cards in two stacks, 3px accent left-rule on grouped rows, chevron SVG hinge. Radius 5–8px, no shadows.

---

## 2. `blueprint` — 藍圖

Deep navy ground with hairline cyan. Reads as a schematic, not a webpage.

**Best for:** data flow and pipelines — what enters, what transforms, what leaves. Multi-stage mechanisms. Before/after of a wiring change.

| role | value |
|---|---|
| ground | `#0e1826` |
| surface | `#14243a` |
| ink / ink-2 | `#dce9f5` / `#8aa4c0` |
| hairline | `#2a4460` |
| accent | `#5fd0e0` cyan |
| semantic | `#7fd694` / `#e8c15f` / `#e8735f` |

Single-theme by design — commit to it, paint `body` explicitly, skip the dark blocks (SKILL.md permits this when deliberate).

Display JetBrains Mono 700 uppercase with `letter-spacing:.08em`; body Noto Sans TC. Figure: 1px cyan strokes only, no fills; `background-image` grid of 24px cyan lines at 6% opacity; boxes are hairline rectangles with mono labels; the hinge is a drawn line with an arrowhead, not a chevron glyph.

---

## 3. `diagnostic` — 診斷儀表

Slate panel with severity stripes and big figures. Numbers are the point.

**Best for:** incidents and regressions with real quantities — a retry storm at 40 concurrent, a cost of $57.67, latency that went from 80ms to 4s, an error rate.

| role | value |
|---|---|
| ground | `#151920` |
| panel | `#1d222c` |
| ink / ink-2 | `#e9edf5` / `#98a1b3` |
| rule | `#2b3240` |
| accent | `#e0a13c` amber |
| severity | ok `#43b581` · warn `#e0a13c` · crit `#e05c4b` |

Also single-theme. Display Noto Sans TC 700 (not serif — this is an instrument, not a document). Figure: rows with a 4px left severity stripe, `font-variant-numeric: tabular-nums` on every digit, one oversized stat per panel with its unit at 0.5× size. Pills for state, uppercase 10.5px.

---

## 4. `textbook-plate` — 教科書圖解

Warm paper-grey, one ink, one annotation red. Numbered callouts with leader lines, caption under the figure.

**Best for:** teaching — onboarding, explaining a concept to someone who didn't write the code, a mechanism a reader meets for the first time.

| role | light | dark |
|---|---|---|
| paper | `#efeee9` | `#17161a` |
| surface | `#f8f7f4` | `#201f24` |
| ink / ink-2 | `#23211c` / `#5d594f` | `#eae7e0` / `#a09a8e` |
| rule | `#d6d3c9` | `#34313a` |
| annotation | `#b3402e` | `#e07a63` |

Display Noto Serif TC 700 with a small-caps-style eyebrow (`font-size:11px; letter-spacing:.18em; text-transform:uppercase`). Figure: the drawing sits centered with numbered circles ① ② ③ in annotation red, thin leader lines to each part, and a `<figcaption>` in 13px italic-weight below. The numbers are the only place the red appears.

**Watch:** keep the paper grey-warm, not cream — `#F4F1EA` plus a serif display plus terracotta is the flagged AI-default look. One annotation red used sparsely on callouts is what separates this from it.

---

## Choosing

| The source is… | Preset |
|---|---|
| a merged PR / completed refactor | `engineering-notebook` |
| a pipeline, a fold, a fan-out, a wiring change | `blueprint` |
| an incident, a cost blow-up, a perf regression | `diagnostic` |
| onboarding material, a concept explainer | `textbook-plate` |
