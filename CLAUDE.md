# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Personal Claude Code content: skills, slash commands, subagents, helper scripts and one hook. No build, no test suite. Everything is installed by symlink, so an edit here is live at once in `~/.claude/` (and `~/.agents/skills/`).

```bash
scripts/link.sh --dry-run   # preview links
scripts/link.sh             # link everything; existing files move to ~/.claude/.link-backup/<timestamp>/
```

Run `link.sh` again after you add a new top-level entry (new skill dir, command, agent, bin script, hook). Edits to existing files need no relink.

## Layout and how the parts connect

| Path | Linked to | Notes |
|---|---|---|
| `skills/<name>/SKILL.md` | `~/.claude/skills/`, `~/.agents/skills/` | Must stay harness-neutral (also used by Codex). Extra reference files sit beside `SKILL.md`. |
| `commands/*.md` | `~/.claude/commands/` | `/pr-review`, `/pre-pr-review`, `/review-pr`, `/address-pr-comments` |
| `agents/*.md` | `~/.claude/agents/` | `pr-review-*` subagents launched by the review commands |
| `bin/*` | `~/.claude/bin/` | Python/bash helpers the commands call by absolute path `~/.claude/bin/...` |
| `hooks/ro_bash_guard.py` | `~/.claude/hooks/` | PreToolUse guard |
| `rules/*.md` | `~/.claude/rules/` | Global rules loaded every session. Only rules written here; third-party rule sets (e.g. everything-claude-code `common/`) stay outside this repo. |
| `global/CLAUDE.md` | `~/.claude/CLAUDE.md` | Global instructions. Public: no emails, account ids, private repo names or paths. Private context goes in memory or a private repo. |
| `crew/LINEAR-PROFILES.example.md` | not linked | Template for `~/.agents/crew/LINEAR-PROFILES.md` (untracked, holds real Linear ids) used by `wayfinder-crew`, `to-spec-crew`, `to-tickets-crew`, `octa` |

PR review system (the most interconnected part):
- `commands/pr-review.md` and `commands/pre-pr-review.md` pre-extract context with `bin/pr-review-graph` (GitNexus call-graph digest), `bin/prepr-context` (external context, optional per-repo config at `~/.claude/review-context/<repo>.json`) and `bin/review-history` (past review sessions, for the miss retro). Agents read those files instead of fetching.
- The `pr-review-*` agents are MCP-free. Agents that keep Bash wire `hooks/ro_bash_guard.py` from their own `hooks:` frontmatter, so no `settings.json` change is needed. The guard denies raw `gh`; agents reach GitHub only through `bin/ro-gh`, a read-only allowlist wrapper over the user's normal `gh` login. Widening either allowlist widens what review agents can do.
- `bin/prepr-loop` runs `/pre-pr-review --loop` one round per fresh `claude -p` process.
- Renaming an agent or bin script means updating every command/agent that references it (`grep -r <name> commands agents bin`).

Helper scripts are written to never fail the caller: on error they write an "unavailable" note and exit 0. Keep that behavior.

## Conventions

- One skill per commit, so a regression traces to one change and can be reverted.
- When creating or editing a skill, `CLAUDE.md`, or an agent prompt, use the `writing-for-agents` skill (in this repo).
- Commit messages use emoji prefixes (`✨feat:`, `🐛fix:`, `📝doc:`, `🔧build:`).
