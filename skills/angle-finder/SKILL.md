---
name: angle-finder
description: Finds 5-10 fresh angles for a writing topic by role-switching and forced combination, tuned to the emotion in top-voted comments (Weibo, HN, Reddit). Use when choosing an angle, 找角度, 切入角度, 選題角度, 換角色, 硬組合, or when a draft's angle is the one everyone already wrote.
---

# angle-finder

Turn one topic into 5-10 angles, drop the **default angle** (the one every other post on the topic takes), and pick one the author's own material can carry.

**Skip** this skill when the author already states an angle that is not the default angle. Say "angle given, skipping angle-finder" and move on.

## 1. Pick the language file

Detect the language of the topic or draft. Read only one file:

- Chinese: [`zh.md`](zh.md)
- English or anything else: [`en.md`](en.md)

The file holds the method names, where to find comments, and examples for that language. Write the angles in that language.

## 2. Name the default angle

Write one line: the angle a reader expects from this topic's headline. Every angle you produce must differ from it. Done when the line exists.

## 3. Read the comments for emotion

Find top-voted comments on the topic, on the platforms the language file lists. From them, note 2-4 **emotions** (what readers already feel: resentment, guilt, relief, envy, smugness), each with the comment that shows it, quoted short, plus source.

No web access, or nothing found: take emotions from what the author said, and mark the source `author` or `assumed`. Never invent a quote and present it as a real comment.

## 4. Generate angles

Use both methods from the language file:

- **Role switch**: list every party in the story, including the quiet ones (the person who pays, the person left out, the tool, the bystander). Write from a party nobody writes from.
- **Forced combination**: pair the topic with something unrelated or opposite, then explain why the pair holds.

Produce 5-10 angles. Each angle must rest on a fact, number or opinion the author actually gave; an angle the material cannot support is cut.

## 5. Output

A table, one row per angle:

| # | Angle (one sentence, headline-ready) | Method | Role or pair | Emotion + comment source | Author material it uses |

Then: the default angle, which angle you recommend and why (fresh, and the author's material carries it), and one runner-up.

Done when: 5-10 rows; every row names its method and its emotion source; none repeats the default angle; one pick is made.

When a piece is written next, state the picked angle in its first lines and keep the whole piece on it.
