# Chapter 2: Folgezettel, Links, and Structure Notes — Implementing Connectivity and Hierarchy

Sources: https://zettelkasten.de/folgezettel/ · https://zettelkasten.de/posts/luhmann-folgezettel-truth/ · https://zettelkasten.de/posts/understanding-hierarchy-translating-folgezettel/ · https://zettelkasten.de/posts/kinds-of-ties/

## Core Idea
"Principles are higher than techniques" (Ido Portal, quoted by Sascha). Folgezettel (note sequences) are one *technique* for two *principles*: **hierarchy** and **direct connection**. Digitally, explicit links plus **Structure Notes** implement both principles better. Folgezettel give you one meaningless hierarchy, while structure notes allow unlimited *meaningful* ones. Trying to collect connections now and "discover their meaning later" is the Collector's Fallacy applied to links.

## Frameworks Introduced
- **Principles over techniques**: copy Luhmann's *principles*, not his paper-bound *techniques*. "A punch is different from a choke while both follow the principles of combat."
  - When to use: whenever someone argues for a feature only because Luhmann used it.
  - How: name the principle the technique serves, then pick the lightest technique in your medium that serves it.
- **The Great Folgezettel Debate** (timeline on /folgezettel/):
  1. Lüdecke: Folgezettel are essential to how Luhmann worked.
  2. Sascha: they are one technique among many.
  3. Lüdecke: they provide context that links cannot.
  4. Sascha: links provide *richer* context; Folgezettel cannot by design.
- **What a Folgezettel is**: a child note filed under its parent, meaning an *intended connection realised through position*. It can mean "continue this thought", "add to it", or "mark a dead end". Its intent is not stated on the note, so an annotated link improves on it.
- **Two achievements of the Folgezettel technique**: (1) it assigns a place in *one* hierarchy; (2) it connects automatically. Structure Zettel replace (1) and direct links replace (2) "with no loss of functionality".
- **Meaningless vs. meaningful hierarchy**:
  - Folgezettel minimise the meaning of position by making it arbitrary. There is a single hierarchy, and where a note sits "is not important as long as you link to it".
  - Structure Zettel remove the meaning of position by allowing *unlimited hierarchies*. Within one structure note, though, the order *is* meaningful.
  - "You'll have order without limiting yourself to *one order*."
- **Kinds of ties between notes** (Christian), from weakest to strongest:
  1. **Juxtaposition / sort order**: neighbouring items seem related, and your brain invents a reason.
  2. **Categories**: exclusive sets (rejected on the site).
  3. **Tags / keywords**: overlapping sets with indirect coupling.
  4. **Folgezettel**: the sub-branch of one note in a linearised tree, with a precise scope (stop reading at the first sibling).
  5. **Hyperlinks**: direct coupling. Full-text search for an ID also finds its backlinks.

## Key Concepts
- **Folgezettel**: literally "following note". In practice, the notes *in a note's sub-branch*, not every note that comes later. `1a` and `1k7` are Folgezettel of `1`; `2` is not.
- **Luhmann-ID**: alternating numbers and letters (`1`, `1a`, `1a1`). It makes branching possible on paper.
- **Structure Zettel / Structure Note**: a note that makes a hierarchy explicit. It is the descendant of Luhmann's **hub notes**.
- **Master Structure Zettel**: one structure note covering everything. It is functionally the same as a full Luhmann-ID tree.
- **§-link convention**: the early site convention of prefixing a target ID with `§`. Searching `§<ID>` lists everything that links there, which works as a "children" view.
- **Unfolding a paradox**: Luhmann's move of drawing a new distinction. It resolves "position matters / position doesn't matter".
- **Juxtaposition**: information carried only by adjacency in a list.

## Mental Models
- Think of every tie as a **breadcrumb of a certain colour**. "The journey is about the breadcrumbs and not about their colour", though some colours mark harder paths.
- Treat Folgezettel as **a physical-medium workaround**: valuable on paper because following links meant flipping cards by hand, and accidental in software.
- Use **sort order deliberately**. Sorting by timestamp ID gives a chronological view you can query (Noguchi filing: people remember *when*). Sorting by title rebuilds brittle categories.
- See **tags as sets, structure notes as sets with added structure, and links as single directed decisions**.

## Anti-patterns
- **Treating Folgezettel as categories**: one parent per note is category logic in disguise.
- **Postponing meaning**: filing a note next to something "because it's related somehow" and hoping the reason appears later. "Folgezettel is to connection what the Collector's Fallacy is to content."
- **Epic-length sequences**: a Folgezettel "story" of thousands of notes needs notes about your own notes before you can read it.
- **Imitating a dead person's constraints**: paper-era workflows in a tool with full-text search.

## Worked Example
**One note, two hierarchies** (from "Understanding Hierarchy"):

- Structure note **Self-Development** links to *The concept of the future self*, because the concept models the self in time and space.
- Structure note **Time** links to the *same* note, because the concept maps the subjective nature of time.

With Folgezettel the note would sit under only one parent, and the other relationship would need a separate link that has no place in the tree. With structure notes, each parent states in its own words *why* the child belongs. That is two meaningful orders, and the note is never moved.

**Reading a branch** (from "Kinds of Ties"): the linearised order is `0, 1, 1a, 1b, 2, 3`. To read the Folgezettel of `1`, start at `1` and continue until you reach `2`. Everything in between (`1a`, `1b`, and any `1k7`) is in scope.

## Key Takeaways
1. Ask "which principle does this technique serve?" before adopting any Luhmann practice.
2. Digitally, use time-based IDs for addresses, annotated links for connection, and structure notes for hierarchy.
3. Allow a note to belong to as many structure notes as make sense. Order is local to each structure note.
4. State the meaning of a connection when you make it. Never collect connections to interpret later.
5. Rank ties: direct link > tag > shared words in full-text search > adjacency.

## Connects To
- **Ch 1**: link context and the structure-note definition.
- **Ch 3**: tags vs. categories, and why manual links beat search alone.
- **Ch 4**: structural layers that appear as structure notes multiply.
- **Ch 8**: Luhmann's numbering and register in historical context.
- **Collector's Fallacy** (Ch 3): the same fallacy applied to content.
