#!/usr/bin/env python3
"""PreToolUse guard for review subagents: Bash may only read.

Wired from the `hooks:` frontmatter of the pr-review-* agents that keep Bash. Every segment of
the command must start with an allowlisted program, used in a read-only way. Anything not
understood is denied (exit 2), which Claude Code enforces in every permission mode.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
import time

LOG = os.path.expanduser("~/.claude/logs/ro-bash-guard.log")
SEPARATORS = {"|", "||", "&&", ";", "&", "\n"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>"}
SCRATCH_PREFIXES = ("/private/tmp/claude-", "/tmp/claude-")

PLAIN = {
    "cat",
    "head",
    "tail",
    "wc",
    "ls",
    "grep",
    "egrep",
    "fgrep",
    "uniq",
    "jq",
    "cut",
    "tr",
    "comm",
    "basename",
    "dirname",
    "echo",
    "printf",
    "nl",
    "true",
    "diff",
    "realpath",
}
FORBIDDEN_FLAGS = {
    "rg": ("--pre", "--pre-glob"),
    "sort": ("-o", "--output", "--compress-program"),
    "find": (
        "-exec",
        "-execdir",
        "-ok",
        "-okdir",
        "-delete",
        "-fprint",
        "-fprint0",
        "-fprintf",
        "-fls",
    ),
}
GIT_READ = {
    "log",
    "show",
    "diff",
    "blame",
    "grep",
    "rev-parse",
    "merge-base",
    "ls-files",
    "ls-tree",
    "status",
    "cat-file",
    "rev-list",
    "for-each-ref",
    "name-rev",
    "describe",
    "shortlog",
}
GIT_FORBIDDEN = ("--output", "--ext-diff", "-O", "--open-files-in-pager", "--exec")
RO_GH = {
    "ro-gh",
    os.path.expanduser("~/.claude/bin/ro-gh"),
    "~/.claude/bin/ro-gh",
    "$HOME/.claude/bin/ro-gh",
}
SED_PRINT = re.compile(r"^(\d+|\$)(,(\d+|\$))?p$")


class Denied(Exception):
    pass


def _check_flags(prog: str, args: list[str], forbidden: tuple[str, ...]) -> None:
    for a in args:
        for f in forbidden:
            if a == f or a.startswith(f + "="):
                raise Denied(f"{prog} {f} is not read-only")


def check_segment(words: list[str]) -> None:
    if not words:
        return
    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0]):
        raise Denied("environment assignments are not allowed")
    prog, args = words[0], words[1:]
    name = os.path.basename(prog)

    if prog in RO_GH:
        return  # ro-gh enforces its own read-only rules and uses a read-only token
    if name == "gh":
        raise Denied("use ~/.claude/bin/ro-gh instead of gh")
    if name in PLAIN:
        return
    if name in FORBIDDEN_FLAGS and name != "find":
        _check_flags(name, args, FORBIDDEN_FLAGS[name])
        return
    if name == "find":
        _check_flags(name, args, FORBIDDEN_FLAGS["find"])
        return
    if name == "sed":
        if len(args) < 2 or args[0] != "-n" or not SED_PRINT.match(args[1]):
            raise Denied("only `sed -n 'N,Mp' file` is allowed")
        return
    if name == "git":
        i = 0
        while i < len(args) and args[i].startswith("-"):
            if args[i] == "-C" and i + 1 < len(args):
                i += 2
            elif args[i] in ("--no-pager", "-P"):
                i += 1
            else:
                raise Denied(f"git global option {args[i]} is not allowed")
        if i >= len(args) or args[i] not in GIT_READ:
            raise Denied(f"git {args[i] if i < len(args) else ''} is not a read-only subcommand")
        _check_flags("git", args[i + 1 :], GIT_FORBIDDEN)
        return
    raise Denied(f"{name} is not on the read-only allowlist")


def check(command: str) -> None:
    if "$(" in command or "`" in command or "<(" in command or ">(" in command:
        raise Denied("command substitution is not allowed")
    command = command.replace("\\\n", " ")  # line continuation, as the shell reads it
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace = " \t\r"  # keep newlines as separators
    lex.whitespace_split = True
    lex.commenters = ""
    try:
        tokens = list(lex)
    except ValueError as e:
        raise Denied(f"could not parse command: {e}") from e

    segment: list[str] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in SEPARATORS:
            check_segment(segment)
            segment = []
        elif t in REDIRECTS:
            target = tokens[i + 1] if i + 1 < len(tokens) else ""
            if segment and segment[-1].isdigit():
                segment.pop()  # fd number, e.g. 2>
            if target != "/dev/null" and (
                "$" in target or not os.path.realpath(target).startswith(SCRATCH_PREFIXES)
            ):
                raise Denied(f"writing to {target!r} is not allowed (scratchpad or /dev/null only)")
            i += 1
        elif t == ">&":
            if segment and segment[-1].isdigit():
                segment.pop()
            if i + 1 >= len(tokens) or not tokens[i + 1].isdigit():
                raise Denied("only fd duplication like 2>&1 is allowed")
            i += 1
        elif t in ("<", "<<", "<<<"):
            i += 1  # reading input is fine; skip its operand
        elif set(t) <= set("|&;<>()"):
            raise Denied(f"shell operator {t!r} is not allowed")
        else:
            segment.append(t)
        i += 1
    check_segment(segment)


def _log(agent: str, decision: str, command: str, reason: str = "") -> None:
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a") as fh:
            stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
            fh.write(f"{stamp} {agent} {decision} {command[:300]!r} {reason}\n")
    except OSError:
        pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        command = payload["tool_input"]["command"]
        agent = payload.get("agent_type", "main")
    except (ValueError, KeyError, TypeError):
        sys.stderr.write("ro-bash-guard: unreadable hook input; denying\n")
        return 2
    try:
        check(command)
    except Denied as e:
        _log(agent, "DENY", command, str(e))
        sys.stderr.write(f"ro-bash-guard: {e}. Review agents may only read.\n")
        return 2
    _log(agent, "allow", command)
    return 0


if __name__ == "__main__":
    sys.exit(main())
