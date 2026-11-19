# skills

My own agent skills, slash commands, and subagents for Claude Code (skills also work in Codex and other Agent Skills-compatible harnesses).

## Layout

| Path | What | Linked into |
|---|---|---|
| `skills/<name>/SKILL.md` | Agent skills | `~/.claude/skills/`, `~/.agents/skills/` |
| `commands/*.md` | Slash commands (`/pr-review`, `/pre-pr-review`, `/review-pr`, `/address-pr-comments`) | `~/.claude/commands/` |
| `agents/*.md` | Subagents used by the PR review commands | `~/.claude/agents/` |
| `bin/*` | Helper scripts the PR review commands and agents call (`ro-gh`, `review-history`, `pr-review-graph`, `prepr-context`, `prepr-loop`) | `~/.claude/bin/` |
| `hooks/ro_bash_guard.py` | PreToolUse guard that keeps the review agents' Bash read-only | `~/.claude/hooks/` |

## Install

```bash
git clone https://github.com/yvetteTsai22/skills.git ~/projects/skills
~/projects/skills/scripts/link.sh --dry-run   # preview
~/projects/skills/scripts/link.sh
```

Everything is a symlink into the repo, so `git pull` updates it. An existing file at a target path is moved to `~/.claude/.link-backup/<timestamp>/<original path>` first, never deleted.

## Notes

- The `pr-review-*` agents wire `hooks/ro_bash_guard.py` from their own frontmatter, so no `settings.json` change is needed. The guard denies raw `gh`; agents reach GitHub through `bin/ro-gh`, which runs on your normal `gh` login and refuses anything outside its read-only allowlist.
- Changes to one skill go in their own commit, so a regression can be traced to one change and reverted.
