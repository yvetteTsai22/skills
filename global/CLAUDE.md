# Global Claude Code Instructions

## Language

- When replying in Chinese, use Mandarin (台灣／大陸普通話書面語), preferably Traditional characters. Never use Cantonese (no 嘅、咗、喺、睇、佢、唔、嘢 etc.).

## Git Conventions

- Do NOT append `Co-Authored-By` lines to commit messages
- Use emoji prefixes from `~/.gitmessage` (e.g., `✨feat:`, `🐛fix:`, `📝doc:`, `🔧build:`)
- Committing, pushing, and opening PRs on feature branches is allowed without asking (never push directly to `main`, never force-push shared branches)
- Merging PRs: only in repos that opt in to autonomy mode (a repo-level `AUTONOMY.md`); everywhere else the user merges

## Python Conventions

- When creating a new Python virtual environment, use `uv venv` (not `python3 -m venv`)
- If a repo already uses `uv` (has `uv.lock` or `.python-version`), continue using `uv` for all dependency management
- Never use `--break-system-packages` — create a venv instead
