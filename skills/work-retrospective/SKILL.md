---
name: work-retrospective
description: Use when the user has finished implementing a feature, fixing a bug, or solving a problem and wants to capture a retrospective summary with lessons learned. Triggered by requests like "write a retro", "summarize what I did", "capture lessons learned", or "add a retrospective note".
---

# Work Retrospective

## Overview

Write a structured 1st-person retrospective summary of completed work and save it to the Zettl knowledge graph. The summary captures what you set out to do, what went wrong, why, how you fixed it, and what you learned.

## When to Use

- User says they finished a task and wants to capture a summary
- User asks to "write a retro", "log what I learned", "summarize this work"
- User wants to add retrospective notes to Zettl

**Not for:** Mid-work status updates, planning, or technical documentation.

## Process

### 1. Gather Context

Before writing, collect facts from the current session:

- **Conversation history**: What did the user describe doing? What problems came up?
- **Git history**: Run `git log --oneline -10` and `git diff main --stat` (or appropriate base branch) to see what actually changed.
- **Ask the user** if anything is unclear. Don't invent details.

### 2. Write the Summary

Use this exact structure, written entirely in **1st person** ("I wanted...", "I discovered...", "I learned..."):

```
## Goal
What I set out to accomplish and why.

## Issues Encountered
What went wrong or was unexpected during implementation. Be specific — name the actual errors, tools, or behaviors.

## Root Cause
Why the issues happened. Separate the underlying cause from the symptoms. This is the most important section — dig one level deeper than the obvious.

## Solution
What I actually did to fix it. Reference specific code, config, or architectural changes.

## Lessons Learned
What I'd do differently next time, or what I now understand that I didn't before.
```

### Writing Rules

- **1st person throughout.** "I tried...", "I found...", never "The developer..." or "We observed..."
- **Specific over generic.** Bad: "Always read the docs." Good: "The ddtrace auto-patching docs don't mention that ADK calls bypass the monkey-patching — I need to check framework compatibility before assuming auto-instrumentation works."
- **Name real things.** Mention actual function names, error messages, config keys, file paths. These make the retro searchable and useful later.
- **Root cause != symptom.** "model_dump() wasn't available" is a symptom. "The ADK response objects use a different serialization interface than Pydantic v2 models" is a root cause.

### 3. Add to Zettl

Use `mcp__zettl__add_note` with:

- **content**: The full retrospective text (all sections)
- **tags**: Use this convention:
  - `retro` (always — marks it as a retrospective)
  - 1-2 **domain tags** (the area of work, e.g. `tracing`, `auth`, `deployment`)
  - 1-2 **technology tags** (specific tools/libs, e.g. `datadog`, `fastapi`)
- **source**: Must be `"retrospective"` (not the default `"agent"`)

Keep tags to 3-5 total. Fewer precise tags beat many vague ones.

## Example

**Input context:** User implemented Datadog tracing for an ADK app, hit auto-patching issues, fixed with manual spans.

**Output:**

```
## Goal
I wanted to add Datadog LLM Observability tracing to our FastAPI + Google ADK supplier recommendation service so we could monitor LLM call latency, token usage, and error rates in production.

## Issues Encountered
- ddtrace's automatic patching (`patch_all()`) silently skipped Google ADK agent calls — no spans appeared for LLM interactions
- Response objects from ADK sessions didn't have `model_dump()`, causing AttributeError when I tried to serialize them for the Datadog span metadata
- Needed to support both Datadog and OpenTelemetry tracing without code duplication

## Root Cause
Google ADK doesn't use the standard HTTP/gRPC client libraries that ddtrace patches. ADK manages its own Vertex AI connections internally, so auto-instrumentation has no hooks to attach to. The response serialization failed because ADK returns custom response objects, not Pydantic v2 models.

## Solution
- Used `ddtrace.llmobs.LLMObs` SDK to manually create spans around `adk_service.run_recommendation()` calls
- Added defensive response handling: check for `model_dump` before calling, fall back to `dict()` or `str()`
- Gated all Datadog instrumentation behind `TRACING_TOOL=datadog` env var in `src/main.py` so the app can switch backends

## Lessons Learned
- I should check whether a framework's internal HTTP calls go through standard libraries before assuming auto-instrumentation will work. ADK abstracts Vertex AI calls away from the transport layer.
- When dealing with response objects from agent frameworks, never assume Pydantic — these frameworks often have their own serialization. Check the actual type first.
- The conditional instrumentation pattern (env var gating) was worth the small upfront cost — it already saved time when testing locally without Datadog.
```

**Zettl call:**
- content: (the full text above)
- tags: `["retro", "tracing", "datadog", "google-adk"]`
- source: `"retrospective"` (never use the default "agent")

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Generic lessons ("always test", "read docs") | Ask "what *specifically* did I not know before?" |
| Passive voice ("it was discovered that...") | Rewrite: "I discovered that..." |
| Symptom as root cause | Ask "but *why* did that happen?" one more time |
| Too many tags (8+) | Keep to 3-5: `retro` + domain + tech |
| Inventing details not in context | Ask the user or check git history |
