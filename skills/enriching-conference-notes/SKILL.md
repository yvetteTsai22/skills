---
name: enriching-conference-notes
description: Use when the user has watched a conference talk, keynote, panel, or recorded session and wants to enrich raw or sparse notes before storing them. Triggers on phrases like "I just watched a talk", "from yesterday's keynote", "rough notes from [conference]", "help me write up this session", or pasting bullet-point notes that read like a transcript. Skip if the user has already produced a thorough write-up or only wants to capture-as-is.
---

# Enriching Conference Notes

## Overview

Most conference notes capture **what was said** but lose the speaker's angle, the user's own judgment, and the connections to existing knowledge. This skill turns raw notes into durable, retrievable knowledge by asking targeted questions — picked from a tiered bank, weighted by *when* the user is invoking the skill (during the talk, right after, or weeks later).

**Core principle:** Ask few questions, ask them well, and pick them based on the gaps in the user's existing notes — not a fixed checklist.

## When to Use

Symptoms that this skill applies:

- User pastes notes that read like a transcript or bullet dump from a talk
- User says "I just watched a keynote / talk / panel / workshop"
- User has rough conference notes from days or weeks ago and wants to extract value before forgetting
- User mentions a specific conference, speaker, or session
- User is mid-session and wants to capture more deliberately

Skip if:

- User has already written a thorough write-up
- User explicitly asks to capture-as-is or "just save it"
- The content isn't a talk-format session (1:1, customer call, decision meeting → different skill)

## Mode Detection

The skill recognizes 4 modes from cues in the invoking message:

| Mode | Triggered by phrasing like... | What the skill does |
|---|---|---|
| **Before** *(rare)* | "I'm about to watch...", "talk in 10 min on X" | Prints a 5-item listening checklist, then exits. No follow-up. |
| **During** | Present-tense, "I'm in a session", "live notes" | Asks 2 quick anchor questions, then offers a small "things to listen for" list. |
| **After (fresh)** | "Just watched", "today at [conf]", "just got out of" | Full flow — runs ~5 tiered questions, one at a time. |
| **Later (cold)** | "From last week", "found old notes", "a while ago" | Skips Anchor, weights Connect + Crystallize heavily. |

**Detection logic:**

1. Read the invoking message for time and tense cues.
2. If clear → enter that mode silently.
3. If ambiguous → ask **one** question: *"Quick check — is this notes from a session you're in/just left, or from a while ago? (during / fresh / cold)"*
4. Don't quiz the user on mode if the cues already answered it.

**Edge case — strong existing notes:** If the user pastes detailed notes that already cover most tiers, do not fire 5 questions. Acknowledge what's strong, then ask only about the genuine gap. Example: *"You've captured the content well — what's missing is your own take. One question: what did you push back on internally while listening?"*

## The 5 Tiers

The question bank is organized into five tiers. Each tier targets a different dimension of value.

### Tier 1 · Anchor — context and source credibility

1. Who was speaking, and what's their angle — vendor pitching their product, academic, practitioner with battle scars, journalist with no skin in the game?
2. What was the talk's one-sentence promise — what did the title or abstract claim it would deliver?
3. What track did you pick this over, and why this one?
4. What conference or venue, and was this a headline slot or a deep-cut session?
5. (Cold mode only) What approximate date or month did you watch this? Helps locate it later.

### Tier 2 · Substance — the actual content

1. What's the speaker's central claim, in one sentence — not a list?
2. What did you learn that you didn't already know? (Reframings count.)
3. What concrete example, demo, or number is the talk's strongest evidence?
4. What did the speaker NOT explain or hand-wave past?
5. What was the most surprising claim — confirmed, contradicted, or stretched something you believed?

### Tier 3 · Critical thinking — judgment and skepticism

1. What did you find yourself disagreeing with or questioning while listening?
2. What assumption is the talk built on that the speaker didn't name?
3. What worked for *them* that wouldn't transfer to your context — and why?
4. What's the strongest counter-argument they didn't address?
5. Does the speaker have a financial, professional, or ideological interest that shapes this message?

### Tier 4 · Connections — links to existing knowledge

1. What does this remind you of from your existing notes or current projects?
2. If this claim is true, what else changes for you or your team?
3. Who else needs to hear this — and what's the one-line pitch you'd send them?
4. What new question does this raise that you'd want to research next?
5. What's the closest thing in your current work that this could improve, kill, or replace?

### Tier 5 · Crystallize — lock in retrievable value

1. If you had to teach the core idea in 60 seconds, what would you say?
2. What phrase, slide, or example do you want to remember verbatim?
3. What would future-you in 6 months want you to have written down?
4. What's the one action this talk actually changes in your work?
5. Stripped of jargon, what's the talk really *about*?

## Mode-to-Tier Weighting

How many questions to pull from each tier, per mode:

| Mode | Anchor | Substance | Critical | Connect | Crystallize | Total | Notes |
|---|---|---|---|---|---|---|---|
| **Before** | priming | priming | priming | priming | priming | 5-item listening checklist | One bullet per tier — *not* questions. |
| **During** | 1 | 1 | 0 | 0 | 0 | **2 + watch-list** | Quick anchor, then a small "things to listen for" list. |
| **After (fresh)** | 1 | 1 | ~1 | 1 | 1 | **~5** | One per tier; Critical *preferred* not required. Skip any tier already strongly covered. |
| **Later (cold)** | 0 | 1 | 1 | 2 | 1 | **5** | Skip Anchor (forgotten anyway). Heavy Connect — that's where dormant value lives. |

**Hard cap: 5 questions per round.** If more is needed, finish the round, produce partial output, then offer a second round: *"Want to go deeper on connections, or are we done?"*

### Before-mode listening checklist

When the skill enters Before mode, output a 5-item checklist (one per tier) and exit:

- **Anchor:** Notice the speaker's angle and incentive — vendor, academic, practitioner?
- **Substance:** Listen for *one* central claim. If you can't find it, you missed it.
- **Critical:** Watch for the assumption nobody names. Listen for what's NOT discussed.
- **Connect:** Tag moments that connect to your existing work — even if you don't know how yet.
- **Crystallize:** Catch one phrase or example you'd quote later. Write it down verbatim.

## Selection Rules

When picking which questions to ask in After-fresh or Later-cold mode:

1. **Read first.** Identify which tiers the user's existing notes already cover. Don't ask what they've already written.
2. **One per missing tier, not three from one.** Breadth beats depth on the first round.
3. **Quote their words.** Whenever possible, reference a specific phrase from their notes: *"You wrote 'cohort retention dropped 12%' — what's the speaker's explanation?"* — not a generic *"What stood out?"*
4. **Prefer at least one Critical question.** Conference notes are weakest at judgment; passive listening produces description. Skip only if Critical is already strongly covered.
5. **Ask one at a time.** Conversational, not a batch dump.

## Output Flow

After the user answers the questions:

1. **Briefly summarize what you have** — one or two lines, just enough to confirm.
2. **Offer the output menu** in this default order:

```
You've answered the questions. What would you like as output?

  1. A short personal reflection (focused on what you learned)
  2. A clean knowledge note (markdown, ready to save)
  3. Both — the note above, plus a separate "follow up on" list
     (links, papers, people to email, things to research next)
  4. Enriched raw notes — keep the original structure, just slot in
     the new content where it fits

  (or tell me to do something else)
```

3. **Produce the chosen output.** Format depends on the choice:
   - **Reflection:** ~150–300 words, first-person, in the user's voice.
   - **Knowledge note:** Structured markdown with sections (Source, Central Claim, Key Points, My Take, Connections, Open Questions). Surface 1–2 atomic, linkable claims that could become standalone notes.
   - **Both:** Reflection inline + knowledge note + follow-up list (plain markdown bullets at the end).
   - **Enriched raw:** Original notes verbatim with answers slotted next to relevant bullets.

### Saving (the user's call)

The output is text in the chat. Saving is a separate, deliberate step the user takes: ask once, after the output, where it goes:

```
Save it?
  1. Personal Notion (a private page)
  2. Local file (default: ~/notes/conferences/<YYYY-MM-DD>-<talk-slug>.md)
  3. Leave it here
```

- **Personal Notion:** use a Notion connector for the user's *personal* workspace. The `notion-work` connector is the work workspace: if it is the only one connected, say so and offer the local file instead.
- **Local file:** write the markdown with the Write tool to the path the user confirms; create the folder if needed. Reply with the path.
- Save only the output the user picked, exactly as shown.

### Stopping rules

- **The user can bail anytime.** *"Just give me the output now"* / *"skip the rest"* → summarize with whatever has been answered and go to the output menu.
- **Save on the user's answer.** Producing text ends the content work; the save prompt follows, and the user picks the destination.
- **If the user says "just enrich, don't quiz me"** at the start, skip directly to Option 4 (enriched raw) using inferences from existing text.

## Quick Reference — gap to tier

| Existing notes have... | Then prefer asking from... |
|---|---|
| Speaker's content but no angle / bias | Anchor |
| Bullet-point summary, no clear thesis | Substance ("central claim?") |
| All description, no judgment | Critical thinking |
| Isolated note, no links to other work | Connections |
| Long talk, very short note | Substance ("most important thing said?") |
| No personal voice or takeaway | Crystallize ("teach in 60 seconds") |
| Strong on most tiers, weak on follow-up | Connect ("who else needs to hear this?") |

## Common Mistakes

- **Asking all 5 questions when notes already cover 3 tiers.** Read first; pick gaps. A 2-question round is fine.
- **Generic questions instead of quoting the user's words.** *"What stood out?"* is weak. *"You wrote X — why did Y change in Q1?"* is strong.
- **Skipping Connections.** A note that doesn't link to anything decays. Always probe at least one.
- **Stopping at description.** *"What did they say?"* < *"What did you learn?"* < *"What changes for you if this is true?"*
- **Saving before asking.** The user picks the destination (Notion, local file, or nowhere) after seeing the output.
- **Stacking questions from one tier.** Three Substance questions in a row is worse than one Substance + one Critical + one Connect.
- **Treating Before mode as a Q&A.** Before is a 5-item listening checklist, then exit. No questions, no follow-up.
