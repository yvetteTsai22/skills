# Design (user-approved "v4")

**Spotlight.** 35% dark overlay outside a rounded cut-out feathered ~2.5 px at output. The cut-out slides/resizes between targets over 0.3 s ease-in-out and follows the real element: the open menu, then the clicked item, then the result.

**User steps** are only things the reader must do. Indigo `#4F46E5` card, `STEP n OF N`, ≤8 words, decorative `Next →` pill, pointer arrow, thin indigo outline, pulsing click beacon on each click (two staggered rings, redrawn every frame). Fold the confirmation in as a `Done: …` line on the last segment of the step rather than a separate step.

**Automatic events** are what the system does; never call them steps. Dark slate card, teal accent bar + bolt icon, header `AUTOMATIC · <PRODUCT>`, no number, no Next. Teal outline + glow; soft breathing ring instead of a click beacon.

**Pacing.** Waits 8–50x, clicks ~1x, key results held ≥2–3 s at 1x (or slowed: speed 2–4 after the change lands), long idle gaps as `ff` with "Fast-forward · a few minutes later". Final frame held 2.5 s. Target 30–40 s total.

**Placement.** Cards must not cover the target or the line above it; pick `side` and `anchor_y` so the arrow points at the clicked row. Fonts: HelveticaNeue.ttc (SFNS renders too wide); arrows are drawn as shapes because the font lacks `→`.

**Privacy.** Blur assignee/member lists and emails wherever visible, for the full time they are on screen (find region + time from frames). Colleagues' names in chat history (Slack @mentions, message authors) are the user's call: list them with region + time and ask, blur on a yes.
