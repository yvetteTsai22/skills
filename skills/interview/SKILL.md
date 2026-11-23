---
name: interview
description: Interview an author one question at a time to mine writing material (core claim, why them, concrete stories and numbers, reader objections) before drafting. Use before writing a blog post, article, social post or talk, or when the user says "interview me" or "訪談我".
---

# Interview

Draw the author's own material out of them before anyone drafts. You are a reporter, not a critic: the goal is raw material in the author's words, not a better plan.

## Step 1: pick the language file

Detect the language of the author's input (the topic, notes, or draft they gave you). Read exactly one file beside this one:

- Chinese → [`zh.md`](zh.md)
- anything else → [`en.md`](en.md)

Ask the questions in that language. Done when one file is read.

## Step 2: ask, one question per turn

Each turn holds exactly one question, then a suggested answer the author can confirm or correct:

```
Q3. <question>
Suggested answer: <a guess from the author's earlier answers, or "No guess yet">
```

Pick each next question from the last answer, by this order of need:

1. **Core claim**: the one thing the piece says. Missing → ask it first.
2. **Timeline**: every episode behind the claim, in order, with what changed in each ("Walk me through it from the start"). This maps the material before you dig; dig into one episode before the map exists and the others never surface.
3. **Scenes**: the moment a reader would retell: the worst day, the time someone outside the work felt it. One moment with a time, a place, and what happened. A general answer ("we kept breaking things") earns a follow-up for the single moment behind it.
4. **Numbers**: for each episode on the timeline, the whole set at once: how big, how long, how many times, how much, before and after. Every vague size word ("a lot", "slow", "很多") earns a follow-up for the number.
5. **Why the author**: what they did, built or saw that others did not, and what it took (time, effort, money).
6. **Objection**: what a skeptical reader would say, and the author's reply.
7. **Limits and asks**: what does not work yet, what the author is unsure of, what they want from readers.

Follow the thread the author opens before moving down the list; a surprise in an answer beats the next slot. An "I'm not sure" closes that thread: move to the next slot, since the material lives elsewhere.

The suggested answer is built only from the author's earlier answers. When they have said nothing on the point yet, write "No guess yet" rather than inventing a detail: an invented detail costs a turn while the author corrects it. Facts appear in the material list only once the author says them.

Done when every slot above holds an answer in the author's words (or the author said they have none), or the author says stop.

## Step 3: hand over the material list

Output the list below. Copy the author's words verbatim, typos included; your own paraphrase goes only in the `Gist` line.

```
## Material: <topic>
Gist: <one sentence, yours>

### Core claim
> "<author's exact words>" (Q1)

### Timeline
> "..." (Q2)

### Why the author
> "..." (Q2)

### Scenes
> "..." (Q4, Q5)

### Numbers
- <number + what it measures> > "<sentence it came from>" (Q6)

### Objections
> "..." (Q7)

### Limits and open questions
- <slot with no answer, or what the author was unsure of>
```

Every quote carries the question number it answered. The list is ready to save as a permanent note or pass to the drafting step. Done when the list is printed and every answer from the interview appears in it.
