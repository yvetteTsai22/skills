---
name: trend-hook
description: Finds what is trending now on Chinese and English platforms (Weibo hot search, 熱點日曆, Google Trends, HN front page, X trending, Reddit rising) and hooks the author's topic onto it, one hook per trend. Use when a piece should ride a trend, 追熱點, 蹭熱點, 借勢, or as the optional step beside angle-finder.
---

# trend-hook

Find 3-6 trends live this week, and for each write the **hook**: one sentence that ties the author's topic to the trend through something the author actually has (a story, a number, an opinion). A trend with no honest hook is dropped, not forced.

Optional step in the blog pipeline, beside `angle-finder` (run before it, so a hook can become an angle). Platform-specific operations (posting to Weibo, building a hashtag) live in `weibo-playbook`, not here.

## 1. Pick the language file

Detect the language the piece will be written in (the draft or request; else the topic). Read only one file:

- Chinese: [`zh.md`](zh.md)
- English or anything else: [`en.md`](en.md)

The file lists the trend sources for that language, how each one ranks, and the hook moves.

## 2. Collect trends

Check the sources the language file lists, live. For each trend keep: name, source, when seen (date), and its **stage** (rising, peak, fading, or scheduled for a calendar date).

No web access: use only the calendar section (dates are knowable), and mark every live-source trend `unverified`. Never present a trend you did not see as currently trending.

Done when 3-6 trends are listed, each with source, date, and stage.

## 3. Write a hook per trend

For each trend, name the **bridge**: the shared emotion, shared object, or shared question between trend and topic. Then write the hook as a headline-ready sentence in the piece's language. Use the hook moves in the language file.

Cut a trend when:
- the bridge needs a fact the author did not give, or
- the trend is a tragedy, disaster, or private person's misfortune and the hook would profit from it.

## 4. Output

| # | Trend | Source + date | Stage | Bridge | Hook (headline-ready) | Author material it uses |

Then: the pick (best bridge, earliest stage) and the timing note (publish within N hours/days, or "evergreen, no trend fits").

Done when: every row has a hook and names the author material it uses; cut trends are listed in one line with the reason; one pick is made, or the output says no trend fits.

## Writing the piece in the same run

Run steps 2-4 first. The piece then opens on the trend within the first two sentences and turns to the author's material by the end of the first paragraph; the trend appears again only to close. The author's material stays the body.
