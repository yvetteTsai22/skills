---
name: to-tickets-crew
description: to-tickets on Linear (work or personal workspace) — slice a spec into tracer-bullet tickets labelled Wayfinder › Tickets with native blocking, with caveman chat and cavecrew codebase lookups.
disable-model-invocation: true
argument-hint: "[work|personal] [spec id/URL]"
---

# To-tickets crew

## Step 0 — load the base protocol (always)

`to-tickets` is `disable-model-invocation`, so the Skill tool cannot load it. **Read `~/.agents/skills/to-tickets/SKILL.md` in full and follow it**, including vertical-slice rules, the expand–contract exception, the quiz step, and the issue template. Below only fills its gaps or overrides it; where this file is silent, to-tickets wins. Ignore its `/setup-matt-pocock-skills` instruction — this file is the setup.

## Tracker

**Read `~/.agents/crew/LINEAR-PROFILES.md`** and pick the profile (arg `work` / `personal`, else auto-detect).

- Source: fetch the spec with `<linear>get_issue` plus `<linear>list_comments`.
- Publish in dependency order (blockers first) with `<linear>save_issue`: same team as the spec, `parentId` = the spec, label **Wayfinder › Tickets** (id from the profile) in place of `ready-for-agent`.
- Blocking edges: native `blocks` / `blockedBy`, second pass after all ids exist.
- Never close or modify the spec, beyond it gaining children.

## Codebase exploration (step 2 of to-tickets)

Use 2–3 `caveman:cavecrew-investigator` subagents in parallel for prefactor opportunities and seams; paraphrase their output before showing it.

## Quiz

Show the breakdown as a numbered list (title / blocked by / what it delivers), then ask to-tickets' three questions one at a time, recommended answer first. Publish nothing until the user approves.

## Voice

Chat: caveman `full`, in the user's language. Ticket bodies in Linear: English, plain full sentences.

## Session end

Report (caveman): tickets created (titles + links), the frontier tickets by title, profile used.
