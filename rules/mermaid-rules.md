# Mermaid Diagram Rules

Extensible rule set for the `mermaid-expert` skill.
Add new sections freely — each rule is independent.

---

## Rule 1: Label Safety — No Raw Angle Brackets

**Problem:** Mermaid parses node and subgraph labels as HTML fragments internally.
Raw `<` and `>` are emitted as literal `&lt;` / `&gt;` text in the rendered output instead of the glyph.

**Applies to:** all label strings in `["..."]`, `(...)`, `[...]`, `{...}` node syntax, and `subgraph` titles.

**Replacements:**

| Avoid | Use instead |
|---|---|
| `<2s` | `≤2s` or `under 2s` |
| `> 500ms` | `≥500ms` or `over 500ms` |
| `A < B` | `A #lt; B` (Mermaid entity escape) |
| `A > B` | `A #gt; B` |

**Preferred substitutes (in priority order):**
1. Unicode: `≤ ≥ → ← × ÷ ≠`
2. Prose: `under`, `over`, `max`, `min`, `up to`, `at least`
3. Mermaid entity syntax: `#lt;` / `#gt;` (only when the operator is semantically important)

---

## Rule 2: Line Breaks in Labels

Use `</br>` (not `\n`, not `<br>`, not `<br/>`) for line breaks inside node labels.

```mermaid
A["First line</br>Second line"]
```

---

<!-- Add new rules below this line. Use ## Rule N: Title format. -->
