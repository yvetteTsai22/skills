---
name: vent
description: Use when the user invokes /vent, OR when you (the agent) hit genuine friction during a task — broken tool, silent failure, missing param, confusing API, or anything that blocked progress.
---

# Vent

## Overview

A cathartic outlet for logging friction, bugs, and frustrations persistently so they're searchable later. Both the user AND the agent can vent. Inspired by Lovable's vent tool — complaints are data that improves the system.

## Who Vents

### User vents
Triggered explicitly: `/vent [complaint]`, or user expresses frustration.

### Agent vents (autonomous)
Triggered by the agent when hitting genuine friction **during a task** — without the user asking. Examples:
- A tool silently failed or returned unexpected output
- A parameter was missing or undocumented
- An API behaved inconsistently with its docs
- A file operation failed in a non-obvious way
- Something caused an unnecessary retry loop

**One vent per message.** Do not chain or retract vents.

**Do NOT vent about:** normal task complexity, things you resolved in under one retry, or subjective preferences.

## Workflow

1. **Acknowledge** (user vents only) — one short empathetic line. Skip for agent-initiated vents.
2. **Categorize** — infer from content:
   - `tooling` — broken CLI, silent failure, bad DX, encoding issue
   - `workflow` — friction, inefficiency, missing shortcut
   - `blocker` — external dependency, waiting on something
   - `cathartic` — user just needed to say it; no action expected
3. **Extract action items** — what could be fixed? Skip if `cathartic`.
4. **Save** — append to `vents_log.md` (see below).
5. **Confirm** (user vents) — max 2 sentences. Agent vents: save silently, continue task.

## Storage: vents_log.md

The markdown file is the only storage.

Read the existing `vents_log.md` first (it may not exist yet — that's fine), then Write the full file back with the new entry appended.

**File:** `~/.claude/projects/<project-slug>/memory/vents_log.md`

**Entry format:**
```markdown
### [YYYY-MM-DD] [CATEGORY] — short title
**Vent:** what happened
**Source:** user | agent
**Actionable:** extracted items, or "cathartic — no action"

---
```

Also ensure `MEMORY.md` has a pointer:
```markdown
- [Vents log](vents_log.md) — logged friction, tooling issues, and actionable complaints
```

## Retrieval

Grep `vents_log.md`, e.g. by category:
```bash
grep -n '\[tooling\]' vents_log.md
```

## Response Style

**User vents:** Max 2 sentences — acknowledge → confirmed saved → action item if any. Never lecture.

**Agent vents:** No user-facing message. Save silently, continue task. Only mention in passing if it explains a delay.

## Examples

**User vent:**
`/vent file copy tool silently fails when filenames have spaces`
→ Appends `### [YYYY-MM-DD] [tooling] — file copy silent fail on spaces` with `**Source:** user`.
> That's the worst kind of failure — silent. Logged to vents_log.md as `tooling`; action item: investigate file copy tool for space handling in filenames.

**Agent vent (silent):**
Agent hits a CLI that hangs with no output when a path has a space → Logged to vents_log.md:
```markdown
### [YYYY-MM-DD] [tooling] — CLI hangs on paths with spaces
**Vent:** CLI exited with no output or error when path contained a space.
**Source:** agent
**Actionable:** quote all paths; report to tool maintainer.

---
```
→ Continues task silently.
