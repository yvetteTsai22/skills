# GitNexus for blast radius; grep for the rest (repos with a `.gitnexus/` index)

**Rule.** Use GitNexus where it measurably wins; default to grep/Read otherwise.

| Question | First call |
|---|---|
| What breaks if I change X? / depth-2 dependents | `mcp__gitnexus__impact` (upstream) |
| What does my diff touch? (pre-commit / PR) | `mcp__gitnexus__detect_changes` |
| How does A reach B? (plain static calls) | `mcp__gitnexus__trace`, then confirm with Read |
| How does A reach B? (injected callables, Protocols, registries) | Read the code — `trace` returns no_path |
| Who calls X? | grep, then Read — GitNexus can merge call sites into one edge |
| Where is X? / literal strings, log messages, config keys | grep |

**How.**
- MCP tools are deferred (`ENABLE_TOOL_SEARCH=true` in settings): load via ToolSearch before the first call.
  CLI equivalents for contexts without MCP: `gitnexus impact|detect-changes|trace|context <...>`.
- Check `gitnexus status` first; a stale index gives wrong line numbers. Reindex: `gitnexus analyze --index-only`.
- Treat GitNexus output as a lead, not an answer: confirm file:line with Read.

**Why.** A/B on one work repo (2026-11-12, 14 questions × 3 reps, Opus, `claude -p`): gitnexus-first ≈ grep overall —
cost $10.10 vs $9.28, accuracy 0.989 vs 0.983, time 830s vs 774s (with deferred schemas). Clear wins only on
impact (433k→240k tokens) and static multi-hop paths (513k→385k).
