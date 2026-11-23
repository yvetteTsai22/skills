---
name: hn-playbook
description: Writes a Hacker News submission (title, Show HN first comment, timing, reply plan) that follows HN's written and unwritten rules. Use when posting to Hacker News, writing a Show HN, launching a dev tool on HN, or answering HN comments on your own post.
---

# hn-playbook

Turn the author's project or article into a Hacker News **submission**: a title, a first comment (Show HN), a posting window, and a reply plan. HN readers are engineers who punish hype; the voice throughout is one engineer telling peers what they built and where it falls short.

Use only facts the author gave. A missing fact is asked for or left out, never invented.

## 1. Pick the branch

- **Show HN**: the author made something readers can try now (run, install, hold). Done when it passes the check in step 2.
- **Plain link**: an article, blog post, sign-up page or newsletter. These are not Show HN; submit with the original title.
- **Ask HN**: a question for the community, no link.

Done when one branch is named with one reason.

## 2. Show HN check

All must hold, or switch to a plain link:

- Something the author built personally and is around to discuss.
- Readers can try it without a sign-up or email gate (a repo, a demo, a binary).
- Not a landing page, a fundraiser, or a minor feature of an existing product.
- Non-trivial: not a quickly generated one-off.

## 3. Title

Rules from the HN guidelines:

- Plain and literal: say what the thing is and does. `Show HN: <Name> – <what it does, in concrete nouns>`.
- No uppercase for emphasis, no exclamation marks, no "amazing", "best", "fastest", "revolutionary".
- For a plain link, use the article's original title unless it is linkbait; then cut to the factual core.
- Under 80 characters. A concrete detail (language, size, the one hard case it handles) beats a slogan.

Write 3 candidates and pick the most literal one. Done when the pick passes every rule above.

## 4. First comment (Show HN)

Post it right after submitting. Order:

1. Who you are, one line.
2. What it does, one sentence.
3. The problem, told as the real incident that made you build it, with its numbers.
4. How it works: the technical choice that matters, and why.
5. Limits and what it does not do yet. Say them before readers find them.
6. Business model in one line ("free, MIT, nothing to sell"), so nobody has to ask.
7. One specific question you want feedback on.

Voice: first person, plain words, no marketing adjectives, no "we're excited to". Short paragraphs. Done when all 7 parts are present and every number traces to the author.

## 5. Timing

The `/newest` page is where a post lives or dies in its first hour. Submit when the author can stay online and answer for 2-3 hours; common advice is US weekday morning Pacific time. A post that died quietly may be rescued by moderators into the second-chance pool; resubmitting the same link soon after is discouraged.

## 6. Reply plan

Give the author 3 rules for the thread:

- Answer fast and in depth; HN rewards detail.
- On criticism, first agree with what is true, then answer. You are writing for the silent readers, not the critic.
- Thank, never argue about votes, never ask friends or coworkers to upvote or post praise. HN detects voting rings and buries the post.

## Output

Title pick (+2 alternates), first comment text, timing line, reply rules. Write in English.

## Sources (borrow tier)

- HN Guidelines, official: https://news.ycombinator.com/newsguidelines.html (titles, promotion, comments, voting)
- Show HN rules, official: https://news.ycombinator.com/showhn.html (what qualifies, sign-ups, landing pages)
- Max Woolf, "Hacker News undocumented" (well-known author): https://github.com/minimaxir/hacker-news-undocumented (second-chance pool, voting-ring detection, flame-war penalty)
- Markepear, dev-tool HN launch guide: https://www.markepear.dev/blog/dev-tool-hacker-news-launch (first-comment order, agree-then-answer). The first-comment order also appears in the Show HN rules' own advice to explain the backstory and be around to discuss: 2 independent sources.
