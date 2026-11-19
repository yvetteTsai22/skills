# Comprehension interactions

The reader is checking whether they actually understood. Add **one or two** — four turns a page into a quiz.

Patterns 1–2 are plain JS. Patterns 3–4 need runtime capabilities, so load `artifact-capabilities` before writing them and declare what you use.

Every pattern degrades: `claude.use(name)` returns `null` when unavailable, and the page must render correctly without it. Hide the affordance, never show a broken button.

---

## 1. 自我檢測 — reveal a hidden answer

The cheapest and the most reliably useful. **The question must target the counter-intuitive case you hid in the figure**, never a fact restated in the prose above it.

```html
<div class="check">
  <p class="q">repo-c 先 <code>pr_closed</code> 後 <code>pr_reopened</code>，頁面上顯示什麼狀態？</p>
  <button class="reveal" aria-expanded="false" aria-controls="a1">看答案</button>
  <p class="a" id="a1" hidden><b>open</b>。狀態取<b>最新</b>事件，不是第一條，也不是「有沒有 closed 過」。</p>
</div>
<script>
document.querySelectorAll(".reveal").forEach(b=>b.addEventListener("click",()=>{
  const a=document.getElementById(b.getAttribute("aria-controls"));
  a.hidden=!a.hidden; b.setAttribute("aria-expanded",String(!a.hidden));
  b.textContent=a.hidden?"看答案":"收起";
}));
</script>
```

Toggle with `el.hidden`, not `style.display` — the artifact head ships `[hidden]{display:none!important}`.

Two or three questions maximum, placed right after the figure.

---

## 2. 改前 / 改後 — one switch drives the whole figure

Lets the reader feel the difference instead of reading about it. One control, not per-row toggles.

```html
<div class="fig" data-mode="after">
  <div class="modes">
    <button data-set="before">改前</button><button data-set="after" class="on">改後</button>
  </div>
  <!-- rows carry data-when="before" / "after" / omitted for always -->
</div>
<style>
  .fig[data-mode="before"] [data-when="after"],
  .fig[data-mode="after"]  [data-when="before"]{display:none}
</style>
<script>
const fig=document.querySelector(".fig");
fig.querySelectorAll(".modes button").forEach(b=>b.addEventListener("click",()=>{
  fig.dataset.mode=b.dataset.set;
  fig.querySelectorAll(".modes button").forEach(x=>x.classList.toggle("on",x===b));
}));
</script>
```

Keep both states the same height so the page doesn't jump.

---

## 3. 用你的話說一遍 — the page checks the explanation

**The strongest comprehension check.** The reader types the mechanism back in their own words; the page asks Claude to compare it against the ground truth and name what's missing.

Needs `capabilities: {sample: {}}`. The viewer pays and consents on first call, so put it behind a click.

```js
const sample = await claude.use("sample");
if (!sample) box.hidden = true;            // degrade: no widget at all
else btn.addEventListener("click", async () => {
  const truth = `折疊規則：以 (repo, pr_number) 分組；state 取最新事件；url 取最後一條帶 url 的事件（pr_merged 的 webhook 可能不帶 html_url）。`;
  out.textContent = "檢查中…";
  try {
    const r = await sample.json(
      `以下是正確機制：\n${truth}\n\n讀者的說明：\n${ta.value}\n\n` +
      `回傳 JSON：{"got":[讀者答對的重點], "missed":[讀者漏掉或講錯的重點], "verdict":"抓到了"|"差一點"|"再看一次圖"}。` +
      `用繁體中文，每項 ≤25 字，識別字保留原文。`,
      { modelTier: "quick" }
    );
    render(r);                              // 你抓到的 / 你漏掉的 / 判定
  } catch (e) {
    out.textContent = e.code === "rate_limited" ? "稍後再試" : "檢查失敗，圖還在上面";
  }
});
```

Put the ground truth in the prompt — `sample` has no memory of the page or of the conversation that built it.

---

## 4. 這段我不懂 — mark a section, keep the mark

Per-section button that records what didn't land, so the author can read it back later with `read_db`.

Needs `capabilities: {db: {}}`. Shared doc when the page has one reader; `data/users/me/unclear` (add the `user` capability) when several people read the same page and each mark should stay private.

```js
const db = await claude.use("db");
if (!db) document.querySelectorAll(".unclear").forEach(b => b.hidden = true);
else {
  const doc = db.doc("feedback/unclear");
  doc.onSnapshot(s => paint((s.data()?.sections) ?? []));   // survives reload, shows on open
  document.querySelectorAll(".unclear").forEach(b => b.addEventListener("click", async () => {
    const cur = new Set((await doc.get()).data()?.sections ?? []);
    cur.has(b.dataset.section) ? cur.delete(b.dataset.section) : cur.add(b.dataset.section);
    await doc.set({ sections: [...cur], at: Date.now() });
  }));
}
```

Read it back from the session that published the page:
`Artifact({action:"read_db", url, db_op:"get", collection:"feedback", doc_id:"unclear"})`.

Tell the reader in one line that the marks come back to you — a button that silently reports is not okay.

---

## Choosing

| Want | Pattern |
|---|---|
| cheap, always safe | 1 自我檢測 |
| the change is the point | 2 改前/改後 |
| verify they really understood | 3 用你的話說一遍 |
| collect what didn't land | 4 這段我不懂 |

Default pairing for a teaching page: **1 + 3**. For a change review: **2 + 1**.
