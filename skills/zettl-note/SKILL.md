---
name: zettl-note
description: "Use when the user asks to write a note, capture knowledge, save a learning, or document something to Zettl. Triggered by: 'write a note', 'save this to zettl', 'capture this', 'note this down', 'add a note about'. Not for retrospectives (use work-retrospective) or LinkedIn posts (use linkedin-post-writer)."
---

# Zettl Note Writer

## Overview

Write structured, searchable notes and save them to the Zettl knowledge graph. Notes capture knowledge worth retrieving later — technical learnings, architectural decisions, tool discoveries, workflow patterns, or reference material.

**Not for:** Retrospectives (use `work-retrospective`), LinkedIn posts (use `linkedin-post-writer`), or ephemeral task tracking.

## Process

### Phase 1: Understand the Knowledge

Before writing, determine what the user wants to capture:

1. **What's the core insight?** — The one thing that should surface when someone searches for this later.
2. **What's the context?** — Why does this matter? What triggered the learning?
3. **What type of note is this?** — Pick the best structure (see Phase 2).

If the user provides raw context (a conversation, code output, tool results), extract the insight and confirm: *"I'll capture a note about [X] — does that match what you want?"*

If the note content is already clear from the conversation, skip straight to writing.

### Phase 2: Pick the Right Structure

| Type | Best for | Structure |
|------|----------|-----------|
| **Technical reference** | Tool usage, API patterns, config recipes | Title → What → How → Example → Gotchas |
| **Decision record** | Why we chose X over Y | Title → Context → Decision → Rationale → Trade-offs |
| **Discovery** | Something learned through investigation | Title → What I found → Why it matters → How to apply |
| **Pattern** | Reusable approach to a recurring problem | Title → Problem → Pattern → When to use → Example |
| **Cheatsheet** | Quick-reference for commands, queries, syntax | Title → Sections with code blocks, tables, or lists |
| **TIL** | Small, single-concept learnings | Title → One-liner → Context → Example → See also |
| **Architecture snapshot** | System/component design at a point in time | Title → Overview → Components → Data flow (Mermaid) → Key decisions → Constraints |
| **Comparison** | Evaluating X vs Y | Title → Context → Comparison table → Verdict → When to use each |

Choose the type that best fits the content. When in doubt, use **Discovery** — it's the most flexible.

#### Type-Specific Guidelines

**TIL (Today I Learned)**
Short and punchy — one concept per note. The title should start with "TIL:" so they're easy to filter. The one-liner is the entire insight in a single sentence. Context explains where you encountered it. Example proves it. "See also" links to related concepts or docs.

```
# TIL: Qdrant collection_exists() returns False for empty collections

A collection that was created but has zero points returns `False` from `collection_exists()` — it only returns `True` when the collection has at least one indexed point.

## Context
Discovered while debugging `search_both_collections()` returning no site results for a new market.

## Example
​```python
# This returns False even though the collection was created
client.collection_exists("supplier_profiles_NZ")  # False (0 points)

# After inserting at least one point:
client.collection_exists("supplier_profiles_NZ")  # True
​```

## See also
- Qdrant `get_collection()` returns metadata regardless of point count
- `get_vector_store()` in `src/utils/qdrant.py` handles this with a fallback
```

Tag convention: `til` + 1-2 tech/domain tags. Example: `["til", "qdrant", "vector-search"]`

**Architecture Snapshot**
Captures system design at a specific point in time. Always include a Mermaid diagram for the data flow or component relationships. Date the snapshot in the title or first line so readers know when it was accurate.

```
# Supplier Recommendation Architecture (March 2026)

AI-powered recommendation service that matches audience segments to supplier profiles using vector similarity search and LLM-based ranking.

## Components

| Component | Role | Location |
|-----------|------|----------|
| FastAPI app | HTTP endpoints, Pub/Sub handler | `src/main.py` |
| ADK orchestrator | Agent session management | `src/adk_service.py` |
| Recommendation agent | Search + rank suppliers | `src/publisher_recommendation/` |
| Enrichment pipeline | Profile enrichment sub-agents | `src/publisher_enrichment/` |
| Qdrant | Vector storage, per-market collections | External service |

## Data Flow

​```mermaid
graph LR
    A[Client] -->|POST /recommend-suppliers| B[FastAPI]
    B -->|Pub/Sub| C[Queue]
    C --> D[ADK Orchestrator]
    D --> E[Recommendation Agent]
    E -->|vector search| F[Qdrant]
    E -->|LLM ranking| G[Vertex AI]
    D -->|callback| H[Client Webhook]
​```

## Key Decisions
- Market-based collections (`supplier_profiles_<ISO>`) for tenant isolation
- Async Pub/Sub pattern for long-running recommendations
- Google ADK over raw LangChain for multi-agent orchestration

## Constraints
- 24 supported markets (ISO 2-letter codes)
- Callback URLs must not be localhost
- Pub/Sub validation errors return HTTP 200 to prevent retries
```

Tag convention: `architecture` + system/domain tags. Example: `["architecture", "supplier-affinity", "recommendation"]`

**Comparison (X vs Y)**
Structured evaluation of alternatives. Always include a comparison table with clear criteria. End with a verdict and "when to use each" — avoid declaring an absolute winner since context matters.

```
# LangChain vs Google ADK for Multi-Agent Orchestration

We evaluated both frameworks for the supplier recommendation pipeline. ADK won for our use case, but LangChain remains better for simpler chains.

## Context
Needed multi-agent orchestration with state management, tool calling, and session persistence for the recommendation + enrichment pipelines.

## Comparison

| Criteria | LangChain | Google ADK |
|----------|-----------|------------|
| Multi-agent orchestration | Manual via LangGraph | Built-in agent hierarchy |
| State management | Custom memory classes | Session-based, automatic |
| Tool integration | Broad ecosystem | Vertex AI native |
| Learning curve | Moderate | Steep (newer framework) |
| Community/docs | Extensive | Growing, less mature |
| Observability | LangSmith, callbacks | OpenTelemetry, Cloud Trace |

## Verdict
**Google ADK** for this project — the built-in session management and agent hierarchy maps directly to our recommendation/enrichment pipeline structure.

## When to Use Each
- **LangChain**: Simple chains, broad tool ecosystem, rapid prototyping, teams already invested in LangSmith
- **Google ADK**: Multi-agent pipelines on GCP, Vertex AI integration, session-based state, production agent systems
```

Tag convention: `comparison` + the things being compared. Example: `["comparison", "langchain", "google-adk", "agent-frameworks"]`

### Phase 3: Write the Note

#### Content Rules

- **Lead with the insight, not the backstory.** The first line after the title should be the key takeaway. Context comes after.
- **Be specific.** Name real functions, tools, error messages, config keys, file paths. These make notes searchable.
- **Include working examples.** Code blocks with real examples from the user's project are 10x more useful than abstract descriptions.
- **Keep it scannable.** Use headers, short paragraphs (1-3 lines), tables, and code blocks. A reader should get the gist in 10 seconds.
- **Write for future retrieval.** Ask: "What would someone search for to find this?" Make sure those terms appear in the note.

#### Formatting

- Use `#` for the title, `##` for sections
- Code blocks with language tags (```python, ```cypher, ```bash)
- Tables for comparisons or quick-reference data
- Bold for key terms on first mention
- No emoji unless the user uses them

### Phase 4: Save to Zettl

Use `mcp__zettl__add_note` with:

- **content**: The full note text (all sections)
- **tags**: Follow this convention:
  - 1 **type tag**: `reference`, `decision`, `discovery`, `pattern`, `cheatsheet`, `til`, `architecture`, or `comparison`
  - 1-2 **domain tags**: the area of work (e.g., `vector-search`, `tracing`, `deployment`)
  - 1-2 **technology tags**: specific tools/libs (e.g., `qdrant`, `gitnexus`, `fastapi`)
- **source**: `"agent"`

Keep tags to 3-5 total. Fewer precise tags beat many vague ones.

### Phase 5: Confirm and Offer Next Steps

After saving, always:
1. Confirm the note was saved with its ID
2. Offer: *"Want me to search Zettl for related notes?"* (uses `search_knowledge`)
3. If the note could become a blog or LinkedIn post, mention: *"This could also work as a [blog/LinkedIn post] — want me to draft one?"*

## Pre-Save Checklist

Run silently before saving. Fix issues, don't report them.

- [ ] Title is descriptive and searchable (not "Note about stuff")
- [ ] First line after title states the key insight
- [ ] At least one code block or concrete example
- [ ] Specific names: functions, tools, files, error messages — not generic descriptions
- [ ] Scannable in 10 seconds: headers, short paragraphs, tables where appropriate
- [ ] Tags: 3-5 total, following the type + domain + tech convention
- [ ] No duplicate of existing Zettl note (search first if unsure)

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Vague title ("Useful thing I learned") | Make it searchable: "GitNexus Cypher — querying fan-in/fan-out in the code knowledge graph" |
| Wall of text with no structure | Add headers, break into sections, use the type templates |
| Generic advice ("always test your code") | Ask "what *specifically* is worth remembering here?" |
| Too many tags (6+) | Keep to 3-5: type + domain + tech |
| Saving without examples | Add at least one real code block or concrete reference |
| Duplicating an existing note | Use `search_knowledge` first to check for existing coverage |

## Example

**User says:** "write a note about the GitNexus cypher queries we just ran"

**Output note:**

```markdown
# GitNexus Cypher — Querying the Code Knowledge Graph

Cypher queries let you ask structural questions about your codebase that no text search can answer: "what has the most callers?", "which modules are biggest?", "are there circular dependencies?"

## Schema Essentials

- **Nodes:** File, Function, Class, Interface, Method, Community, Process
- **Edges:** All via single `CodeRelation` type with a `type` property
- **Edge types:** CALLS, IMPORTS, EXTENDS, IMPLEMENTS, HAS_METHOD, HAS_PROPERTY, MEMBER_OF, STEP_IN_PROCESS

## Key Queries

### Find most-called functions (highest fan-in)
​```cypher
MATCH (caller)-[:CodeRelation {type: 'CALLS'}]->(callee)
WITH callee, count(caller) AS incoming
ORDER BY incoming DESC LIMIT 10
RETURN callee.name AS function, callee.filePath AS file, incoming AS callers
​```

### Find orchestrator functions (highest fan-out)
​```cypher
MATCH (f)-[:CodeRelation {type: 'CALLS'}]->(g)
WITH f, count(g) AS outgoing
ORDER BY outgoing DESC LIMIT 10
RETURN f.name AS function, f.filePath AS file, outgoing AS dependencies
​```

## Concepts

- **Fan-in** (many callers) = shared utility, risky to change
- **Fan-out** (many callees) = orchestrator, breaks when deps change
- Always filter edges with `{type: 'CALLS'}` — single CodeRelation edge type
- Use `heuristicLabel` for readable community/process names
```

**Zettl call:**
- content: (the full text above)
- tags: `["cheatsheet", "gitnexus", "cypher", "code-intelligence"]`
- source: `"agent"`
