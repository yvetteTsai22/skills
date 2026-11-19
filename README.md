# Agent skills and workflow tools

A collection of reusable instructions and tools for AI coding assistants. It includes writing and planning skills, pull request review workflows, helper scripts, and a few Linear-oriented workflows.

The skills use the Agent Skills format and can be used with Claude Code, Codex, and other compatible tools. The slash commands, subagents, hooks, and installer in this repository are currently set up for Claude Code.

This is a personal, evolving collection. You’re welcome to browse it, adapt the pieces that are useful to you, and suggest improvements.

## What’s here

| Directory | Contents |
|---|---|
| [`skills/`](skills/) | Standalone skills, each documented in its own `SKILL.md`. Topics include writing, note-taking, planning, and review workflows. |
| [`commands/`](commands/) | Claude Code slash commands for pull request review and follow-up. |
| [`agents/`](agents/) | Subagent instructions used by the pull request review commands. |
| [`bin/`](bin/) | Helper scripts used by review workflows. |
| [`hooks/`](hooks/) | A Bash guard used to keep review-agent shell access read-only. |
| [`crew/`](crew/) | Example configuration for workflows that use Linear. |
| [`scripts/link.sh`](scripts/link.sh) | Optional installer that symlinks repository files into Claude Code and Agent Skills directories. |

Some workflows depend on external tools or account setup. Check the relevant `SKILL.md` or command before using one; the Linear profile file in `crew/` is an example, and should be copied and configured for your own workspace.

## Browse and use a skill

Open any skill’s `SKILL.md` and follow its instructions in a compatible assistant. You can also copy a skill into your assistant’s configured skills directory. Skills are independent, so you can use only the ones that fit your workflow.

## Install the Claude Code workflows

The installer links skills into `~/.claude/skills/` and `~/.agents/skills/`, and links commands, agents, helper scripts, and hooks into their corresponding `~/.claude/` directories.

```bash
git clone https://github.com/yvetteTsai22/skills.git
cd skills
./scripts/link.sh --dry-run  # preview the planned changes
./scripts/link.sh           # create or refresh the links
```

If a target already contains a file or directory, the installer moves it to `~/.claude/.link-backup/` before creating the link. Review the dry-run output first. The links point to your checkout, so changes pulled into that checkout are reflected immediately.

## Contribute

Issues and pull requests are welcome. For a focused change, update the relevant skill or workflow and check that its referenced files and setup instructions still match the repository. There is no build step or automated test suite. If you change installation behavior, use `./scripts/link.sh --dry-run` and review the planned links.

Please don’t include credentials, private workspace identifiers, or local configuration in contributions. Use `crew/LINEAR-PROFILES.example.md` as the safe template for Linear workspace setup.

## License

No license is currently specified. Please open an issue if you’d like to reuse or redistribute this collection and need licensing terms clarified.
