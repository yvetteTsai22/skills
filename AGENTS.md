# Repository Guidelines

## Project Structure & Module Organization

This repository contains agent skills, prompts, and helper tooling. Put each skill in `skills/<name>/` with its main instructions in `SKILL.md`; keep supporting references and examples beside it. Slash commands live in `commands/`, subagent prompts in `agents/`, executable helpers in `bin/`, hooks in `hooks/`, and installable symlink logic in `scripts/`. `crew/LINEAR-PROFILES.example.md` is a safe template; keep real workspace identifiers out of the repository. There is no separate test or asset tree.

## Build, Test, and Development Commands

There is no build step or automated test suite. Preview installation links with `scripts/link.sh --dry-run`; run `scripts/link.sh` to install or refresh them. Existing target files are backed up by the script. After adding a new top-level skill, command, agent, helper, or hook, rerun the installer. When changing existing files, inspect the relevant prompt references and helper behavior directly.

## Coding Style & Naming Conventions

Use Markdown with descriptive headings, concise instructions, and concrete examples. Name skill directories in lowercase kebab-case and use `SKILL.md` as the entry point. Preserve the existing conventions of each helper: Python scripts use clear snake_case names, and shell helpers should remain portable and quote paths. Keep skills harness-neutral where possible. Helper scripts are expected to report an unavailable result and exit successfully when an optional dependency or external service fails. If you rename a command, agent, or helper, update all references in `commands/`, `agents/`, and `bin/`.

## Testing Guidelines

No test framework or coverage threshold is configured. For changes to installation behavior, run `scripts/link.sh --dry-run` and inspect the planned links. For helper changes, run the affected script with representative inputs and error conditions; for prompt changes, check linked filenames and instructions for consistency.

## Commit & Pull Request Guidelines

Recent history uses short emoji-prefixed subjects such as `✨feat: add crew planning skills` and `📝doc: clarify setup`. Keep changes focused; the project recommends one skill per commit so regressions are easy to trace. Pull requests should describe the user-facing change, list affected paths, and include verification steps. Add screenshots only when a change affects rendered visual output.

## Security & Configuration

Do not commit credentials, private Linear identifiers, or local configuration. Review changes to `hooks/ro_bash_guard.py` and `bin/ro-gh` carefully: they constrain the review agents’ shell and GitHub access. Keep those allowlists narrow.
