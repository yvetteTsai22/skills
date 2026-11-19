# Patterns — Zettelkasten Method Techniques

## Time-Based Unique ID
**When to use**: Every new note in a digital archive, and anything else you may want to point at (drafts, receipts, journal entries).
**How**: Use a `YYYYMMDDHHMM` timestamp (add seconds for rapid creation), put it in both the filename and the body, and generate it with a snippet such as `,,id`. Link as `[[ID]]` or `§ID`.
**Trade-offs**: Not meaningful as a position, by design. Titles can then change freely.

## Annotated Link (Link Context)
**When to use**: Every link.
**How**: Write the link inside a sentence that says why the target matters to this note ("…the reason liquidity comes first: [[ID]]").
**Trade-offs**: Slower than bare links, but the link becomes knowledge and the web stays trustworthy.

## Structure Note
**When to use**: Tag or search results become too large, or you need an overview or sandbox for a topic or a project.
**How**: Create a note that lists links in a meaningful order (nested headings, argument chains), each with a short context. Link every new relevant note into it. Let structure notes of structure notes become top-level, and mark designed hubs `##tag`.
**Trade-offs**: Needs ongoing curation. In return, you can order notes without forcing a single hierarchy.

## Link-First Note Creation
**When to use**: Starting out, or extending a structure note.
**How**: Add a link on the structure note to a note that doesn't exist yet, then create that note.
**Trade-offs**: Guarantees no orphan notes and keeps focus on one interest.

## New-Note Decision Tree
**When to use**: Before writing any note.
**How**: Search for related notes first. If nothing is related, write a new note. If related notes don't fit, write a new note and reuse their keywords. If a few roughly match, write a compilation note linked both ways. If one note covers it, extend that note. Always link.
**Trade-offs**: Takes a search each time, which pays back by preventing duplicates.

## Three-Way Split
**When to use**: A prose note takes too long to read or mixes concerns.
**How**: Extract two detail notes and repurpose the original as the connector that links to both. Keep the original ID as the trail.
**Trade-offs**: More notes, but each is reusable. Check that old incoming links still make sense.

## Object Tagging
**When to use**: Adding tags.
**How**: Tag only what the note is *about*, never everything it is relevant to.
**Trade-offs**: Fewer tags and less recall, with much higher precision.

## Barbell Reading
**When to use**: Any book or long article.
**How**: Pass 1: read swiftly and mark useful, interesting, or difficult passages. Pass 2: process only the marks, writing notes and linking them. Let quality decide how long pass 2 takes.
**Trade-offs**: Two passes, but weak books cost little and strong books get deep processing.

## Reading as Searching
**When to use**: Reading for the archive.
**How**: Look specifically for theories, models, definitions, arguments, counter-arguments, and facts. Use margin glyphs D / M / A / ⚡ for dense texts.
**Trade-offs**: Ignores style and narrative, which is intended for knowledge work.

## Collect → Cluster → Write
**When to use**: Turning reading notes into Zettel.
**How**: Dot the margin and write your own-words summaries on slips. Afterwards pull all slips and cluster them by your purpose, not by chapter. Per cluster, write a general note, then detail notes, then update the general note.
**Trade-offs**: Paper-first adds a transfer step, so budget up to 2 h of processing per 1 h of reading.

## Layered Evidence Notes
**When to use**: Processing studies or empirical claims.
**How**: Keep the pattern (with study conditions), the interpretation, and the synthesis in separate linked notes, or as three labelled sections. Check primary sources.
**Trade-offs**: More work up front, and notes stay trustworthy for years.

## Buffer Note
**When to use**: A project's draft is frozen but relevant notes keep coming, or you run many projects in parallel.
**How**: Make a note per project holding `[[ID title]]` plus one line of context per candidate note.
**Trade-offs**: Unstructured by design. Promote entries into the outline when you revise.

## Outline Assembly (Ease Into Writing)
**When to use**: Starting any text.
**How**: Survey the archive, sketch an outline in full sentences, attach note IDs to items, research the gaps, paste note contents in order, then rewrite.
**Trade-offs**: Rough first drafts need heavy editing. There is no blank page.

## Attach Every Note to an Outline
**When to use**: After writing any Zettel (indirectional work).
**How**: Search your outlines and structure notes for projects the note could serve. Link it there, or start a new outline.
**Trade-offs**: Small per-note overhead, and books grow in parallel without extra effort.

## Composing/Revising Split
**When to use**: Daily writing.
**How**: Compose in your best-focus hours and revise in a separate session with some distance. Track words per day.
**Trade-offs**: A growing backlog of unrevised drafts, in exchange for flow and volume.

## Short Research Cycles (Anti-Collector)
**When to use**: Researching a new topic.
**How**: Cap collecting (start at 1 h), process everything collected, review, and adjust the cap.
**Trade-offs**: Slower pile growth, and nothing goes unprocessed.

## Saved Search via Wiki Link
**When to use**: Bookmarking a complex query in tools where links run searches.
**How**: Write `[[#tag term NOT other]]` on a dashboard or home note. `AND` is implicit.
**Trade-offs**: Returns an unordered set and is not a substitute for structure notes.
