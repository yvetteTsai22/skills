---
name: to-spec-crew
description: to-spec on Linear (work or personal workspace) — synthesize the conversation or a finished wayfinder map into a spec issue labelled Wayfinder › Spec, with caveman chat.
disable-model-invocation: true
argument-hint: "[work|personal] [map or issue id/URL]"
---

# To-spec crew

## Step 0 — load the base protocol (always)

`to-spec` is `disable-model-invocation`, so the Skill tool cannot load it. **Read `~/.agents/skills/to-spec/SKILL.md` in full and follow it**, including its spec template. Below only fills its gaps or overrides it; where this file is silent, to-spec wins. Ignore its `/setup-matt-pocock-skills` instruction — this file is the setup.

## Tracker

**Read `~/.agents/crew/LINEAR-PROFILES.md`** and pick the profile (arg `work` / `personal`, else auto-detect).

- Source: if `$ARGUMENTS` names a map or issue, fetch it with `<linear>get_issue` plus `<linear>list_comments`. For a wayfinder map, also read the closed child tickets it indexes under Decisions so far — they hold the decisions; the map only gists them.
- Team: same team as the source issue; no source → ask in one line.
- Publish with `<linear>save_issue`, label **Wayfinder › Spec** (id from the profile). This replaces to-spec's `ready-for-agent` label.
- Source was a wayfinder map → set the spec's `parentId` to the map and add one line `- [<spec title>](url): spec published` to the map's Decisions so far. Do not close the map.

## Seam check

to-spec's only question to the user is the test seams. Ask it as one question: recommended seam first, at most 4 options, one line each.

## Voice

Chat: caveman `full`, in the user's language. Spec body in Linear: English, plain full sentences.

## Session end

Report (caveman): spec title + link, seam chosen, profile used, and next step `/to-tickets-crew <spec>`.
