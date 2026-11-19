---
name: illustrating-in-chinese
description: Use when asked to explain something as a 中文/繁體中文 illustrated page — 圖解, 視覺化說明, visual explainer, 說明頁. Source can be a ticket, issue, bug, PR, review comment, design decision, architecture, code path, incident, concept, or article. Triggers include "explain this in Chinese", "把這個做成圖解", "畫一下給我看", "illustrative artifact for this review comment", or turning a Linear/Jira/GitHub item, a module, or a doc into a shareable Chinese explainer page.
---

# Illustrating in Traditional Chinese

## Overview

Turn one subject — a ticket, review comment, PR, design decision, code path, incident, concept, or article — into a single page the reader can **act on without returning to chat**. Not a Chinese translation of the source.

The page is written in **Traditional Chinese (Taiwan usage)**. This file is in English; the output never is.

**REQUIRED BACKGROUND:** load `artifact-design` first. It owns font loading, dual themes, responsive rules, CSP, and the publish flow. This skill only adds the Chinese-explainer contract on top. `archify` is **one option** for a figure, used only for true structure questions (see The figure).

**Reader model.** The reader is usually the user, alone, either **choosing between routes** or **understanding an unfamiliar mechanism**. They have not read the chat. A single impressive all-in-one diagram fails them: it looks good, but they can't tell where to start and have to go back to chat for context. So: orientation first, then one concrete case walked step by step, then small figures that each prove one thing, then the decision.

**Supporting files:**
- `styles.md` — four visual presets. Default to `engineering-notebook`; switch only when the subject clearly matches another preset's row in the Choosing table.
- `interactions.md` — four comprehension interactions. Include one or two when the reader needs to verify they understood.

## Process

1. **Read the source itself, not the text pasted into the prompt.** Ticket: Linear MCP or `gh issue view`. Review comment: `gh pr view --comments`. Actual change: `git log main..HEAD`, `git diff main...HEAD --stat`, and plain `git diff` — the uncommitted half is often the subject in question. Code path / architecture: read the real modules, not the README. Article / doc: fetch it. Run the tests if they exist and put the real number in the closing section.
2. **Name the reader's question**: what must they *decide* or *understand*? Then list every term, component and prior decision the source assumes they know — that list becomes 先讀這裡.
3. **Pick one real case to walk**: one real operation, ticket, request or payload that exercises the mechanism.
4. **Pick the figures by question** (router in The figure). Typical page: worked example + 1–3 small figures + comparison table when there are routes.
5. **Pick a style preset** from `styles.md` — `engineering-notebook` unless the subject clearly calls for another — and, if useful, an interaction from `interactions.md`.
6. Write the `artifact-design` design plan (color / type / layout), build the page with figures inline, publish.

## Page contract

The page **is** these blocks, in order. Four ★ are required; pick 1–3 more only where the source actually has the material. 5–7 blocks total.

| # | Block | Content |
|---|---|---|
| 1 ★ | header | H1 + one-line lede. The H1 states **the problem** — a question works well — not the task name. The lede says what this page lets the reader do. Ticket id only if there is a real ticket — **never invent an id or a status**, no emoji |
| 2 ★ | 先讀這裡 | Directly under the header, one surface. (a) One serif sentence: 「你要決定：…」 or 「你要理解：…」. (b) A `dl` glossary of 3–6 terms the source assumes — components, identifiers, jargon — each ≤ 40 字, stacking to one column on phones. (c) One line of already-decided facts, so the reader doesn't re-open them |
| 3 ★ | 走一次 | Worked example: the one real case from step 3, traced step by step with real names and values. With a before/after, use two columns 今天 / 改後: shared steps span both columns and stay muted; the broken step is red, the fixed step green. On phones each cell carries its own 今天/改後 tag |
| 4 | 小圖 | 1–3 small inline figures, each proving **one** claim; the caption states that claim. Prefer small multiples: the same mini-figure repeated with one variable changed. The counter-example is **one of the figures**, drawn and outlined in red — never a sentence under someone else's figure |
| 5 | 規則 | 2–4 cards, one rule each |
| 6 | 坑 | One callout: what goes wrong if you do the obvious version |
| 7 | 改動範圍 | file → one line each. **Only when a real diff exists** |
| 8 ★ | closing | Routes not yet chosen → **比一比**: comparison table, routes as columns, criteria as rows, a 結論 row, recommended column marked, good/bad cells colored. Work done → **驗收** (the source's own done condition — a ticket's Done when, a PR's test plan — + what you actually ran). Never claim you ran something you didn't |

## Word budget

- lede ≤ 40 字 · 先讀這裡 sentence ≤ 50 字 · each glossary entry ≤ 40 字 · rule card ≤ 40 字 · each worked-example cell ≤ 40 字
- Every body paragraph ≤ 3 sentences and ≤ 120 字. Reaching for a fourth sentence means that paragraph belongs in a figure or the worked example.
- Whole page ≤ 700 字 of body text. Figures, code, tables and the 先讀這裡 glossary don't count — context the reader lacks is never the thing to cut.

## Language

- **Traditional Chinese, Taiwan usage**: 程式碼 / 回傳 / 物件 / 佇列 / 快取 / 預設值 / 相依。Not 代码 / 返回 / 队列.
- **Identifiers stay in the original**: field names, function names, state values, error codes — `pr_url`, `401`, `single-flight`, `coalesce`. Explain them in the glossary, not inline.
- **Never coin a translation.** `single-flight refresh` stays `single-flight refresh`, not 「單一飛行刷新」. Mixed CJK/Latin headings are correct.

## The figure

Draw what answers the reader's question, not the topic. Self-test: cover every paragraph — can a reader still say what happens, to what, and where it breaks? If not, it's decoration.

**One claim per figure.** If the caption needs 「和」/「而且」, split it into two figures. Several small figures beat one big one.

| Reader's question | Figure | How |
|---|---|---|
| Which route should I pick? | comparison table (+ small multiples) | Routes as columns, criteria as rows, 結論 row. Optionally one mini-figure per route, same axes |
| What happens, in what order? | worked example, sequence | Step rows with real values; Mermaid `sequenceDiagram` with real message names when there are ≥ 3 actors |
| Who/what is affected by X? | small multiples, timeline | Same lanes per scenario, interrupted span in red; inline SVG |
| Which states, which transitions? | state machine | Mermaid `stateDiagram-v2`, every edge labelled with its trigger, failure and terminal states colored |
| How does a parameter change things? | explorable | One slider or step button bound to one output (`interactions.md`) |
| What exists and what connects? | architecture | Only this question uses `archify`; keep ≤ 8 nodes, one main path |

- **Inline, not iframed.** Hand-written inline SVG (theme tokens for every fill and text color, `viewBox` with room for labels, `width:100%`) or `<pre class="mermaid">` — artifacts render Mermaid natively, so load no library. No iframe, no viewer chrome, readable at 400px.
- **Real data as labels** (real workflow names, real PR numbers, real field names). Abstract A/B/C nodes are a wasted figure.
- **Mark what's schematic.** If a time axis isn't to scale, the figure must not imply it is.
- **archify, when used:** follow its fast authoring path, `validate --quality showcase`, `deliver`; omit `meta.locale`; embed as a supporting file in an iframe with explicit height plus a 「開新分頁看完整圖」 link, and say the viewer buttons are English. Report its receipt truthfully.
- **Breakout without shifting the column.** If the reading column is `display:grid`, give it `grid-template-columns:minmax(0,1fr)`, so a wide table or figure can't stretch the implicit `auto` track. Wide tables scroll inside their own `overflow-x:auto` wrapper.

## Color and type

Take the palette from the subject's own vocabulary — a domain usually ships one, and it beats invented semantic colors: PR states are GitHub's open `#1a7f37` / merged `#8250df` / closed `#cf222e`. Otherwise take the preset palette from `styles.md`, defaulting to `engineering-notebook`. Spend red only on broken / interrupted / counter-example, green only on working / kept / recommended.

Fonts load via `<link>`, not `@import`, placed **before** `<style>`:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700&family=JetBrains+Mono:wght@400;700&display=swap">
```

Body stack `"Noto Sans TC", -apple-system, "PingFang TC", "Microsoft JhengHei", sans-serif`. Always **TC**, never SC.

## Theme tokens

Declare every token in bare `:root`, then redefine **the same complete set** in both dark blocks — `@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]) }` and `:root[data-theme="dark"]`. Redefining `--paper` but forgetting `--ink` gives white-on-white when a light-OS viewer toggles dark. SVG text and fills use the same tokens.

## Common Mistakes

| Symptom | Fix |
|---|---|
| Reader doesn't know where to start | Missing or vague 先讀這裡. Its first sentence must name the decision or the thing to understand |
| Reader goes back to chat to ask what a term means | Add it to the glossary. Any identifier in the figures that isn't self-evident belongs there |
| One impressive diagram that's hard to digest | Split into a worked example + small figures, one claim each |
| Decision page drawn as an architecture diagram | Route question → comparison table. archify is for "what exists" only |
| Counter-example lives in a sentence under the figure | Draw it as its own small figure, red outline |
| Reads as a Chinese tech essay | Apply the word budget. The sentences that overflow were always the worked example |
| Figure is decoration | Cover-the-prose self-test. Swap labels for real data |
| Whole page sits right of center | Grid reading column lacks `grid-template-columns:minmax(0,1fr)` |
| Coined translations | Keep identifiers and terms in the original; explain in the glossary |
| Dark theme renders white on white | All three theme blocks cover the same token set, SVG included |
| Simplified characters slip in | Sweep for 代码 / 返回 / 队列 / 缓存 / 默认 / 应该 |
| Invents `MEE-XXX` or a 「待修復」 chip | No ticket in the source means no meta row. Missing facts stay missing |
| A review comment ends with 「測試全綠」 | Nothing implemented → closing is 比一比, not 驗收 |
