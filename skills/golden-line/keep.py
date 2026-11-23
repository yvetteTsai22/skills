#!/usr/bin/env python3
"""Shield golden-line keepers from ste80-humanizer.

  keep.py protect DRAFT              > protected.md   # keepers -> [[GL-KEEP-NN]]; map to DRAFT.keep.json
  keep.py restore MAP HUMANIZED      > final.md       # tokens -> original marked sentences
  keep.py check   DRAFT FINAL                         # exit 1 if any keeper changed or is missing

A keeper is `<!-- gl:keep -->sentence<!-- /gl:keep -->` (see SKILL.md step 4).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KEEP = re.compile(r"<!--\s*gl:keep\s*-->(.*?)<!--\s*/gl:keep\s*-->", re.S)
TOKEN = re.compile(r"\[\[GL-KEEP-(\d+)\]\]")


def protect(draft: Path) -> None:
    text = draft.read_text()
    keepers: dict[str, str] = {}

    def swap(m: re.Match) -> str:
        key = f"{len(keepers) + 1:02d}"
        keepers[key] = m.group(0)
        return f"[[GL-KEEP-{key}]]"

    out = KEEP.sub(swap, text)
    Path(f"{draft}.keep.json").write_text(json.dumps(keepers, ensure_ascii=False, indent=2))
    sys.stdout.write(out)
    print(f"protected {len(keepers)} keeper(s); map: {draft}.keep.json", file=sys.stderr)


def restore(map_file: Path, humanized: Path) -> None:
    keepers = json.loads(map_file.read_text())
    text = humanized.read_text()
    out = TOKEN.sub(lambda m: keepers.get(m.group(1), m.group(0)), text)
    lost = [k for k in keepers if f"[[GL-KEEP-{k}]]" not in text]
    sys.stdout.write(out)
    if lost:
        print(f"lost token(s): {', '.join(lost)}; place them by hand", file=sys.stderr)


def check(draft: Path, final: Path) -> int:
    want = [m.group(1).strip() for m in KEEP.finditer(draft.read_text())]
    final_text = final.read_text()
    have = {m.group(1).strip() for m in KEEP.finditer(final_text)}
    bad = [s for s in want if s not in have and s not in final_text]
    for s in bad:
        print(f"CHANGED OR MISSING: {s}")
    print(f"{len(want) - len(bad)}/{len(want)} keeper(s) intact")
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[1] == "protect":
        protect(Path(argv[2]))
        return 0
    if len(argv) == 4 and argv[1] == "restore":
        restore(Path(argv[2]), Path(argv[3]))
        return 0
    if len(argv) == 4 and argv[1] == "check":
        return check(Path(argv[2]), Path(argv[3]))
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
