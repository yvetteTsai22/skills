#!/usr/bin/env bash
set -euo pipefail

# Links everything in this repo into the directories each agent harness reads:
#   skills/*   -> ~/.claude/skills/ and ~/.agents/skills/
#   commands/* -> ~/.claude/commands/
#   agents/*   -> ~/.claude/agents/
#   bin/*      -> ~/.claude/bin/
#   hooks/*    -> ~/.claude/hooks/
# Each entry is a symlink into this repo, so edits here take effect at once.
#
# An existing real file or directory at a target path is moved to
# ~/.claude/.link-backup/<timestamp>/ before it is replaced, never deleted.
# Run with --dry-run to see what would change.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1
BACKUP="$HOME/.claude/.link-backup/$(date +%Y%m%d-%H%M%S)"

link() {
  local src="$1" dest="$2"
  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    return
  fi
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    echo "backup  $dest"
    if [ "$DRY_RUN" = 0 ]; then
      # Mirror the parent path so ~/.claude/skills and ~/.agents/skills don't collide.
      local parent
      parent="$(dirname "$dest")"
      mkdir -p "$BACKUP${parent#"$HOME"}"
      mv "$dest" "$BACKUP${parent#"$HOME"}/"
    fi
  fi
  echo "link    $dest -> $src"
  [ "$DRY_RUN" = 0 ] && ln -s "$src" "$dest"
  return 0
}

for skill in "$REPO"/skills/*/; do
  skill="${skill%/}"
  [ -f "$skill/SKILL.md" ] || continue
  for dest_dir in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
    mkdir -p "$dest_dir"
    link "$skill" "$dest_dir/$(basename "$skill")"
  done
done

for kind in commands agents bin hooks; do
  mkdir -p "$HOME/.claude/$kind"
  for file in "$REPO/$kind"/*; do
    [ -f "$file" ] || continue
    link "$file" "$HOME/.claude/$kind/$(basename "$file")"
  done
done

[ "$DRY_RUN" = 1 ] && echo "(dry run, nothing changed)"
exit 0
