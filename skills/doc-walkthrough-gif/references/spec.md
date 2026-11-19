# render.py spec schema

Coordinates are **source pixels**; times are **source pts seconds**. See `../examples/stack-start.json`.

| key | meaning |
|---|---|
| `source` | `.mov` path (read-only) |
| `source_size` | `[W, H]`; probed with ffprobe if omitted |
| `out_width` / `fps` | default 1300 / 12 |
| `product` | name in the automatic header, `AUTOMATIC · <PRODUCT>` |
| `dim` / `ff_dim` | spotlight dim (0.35) / fast-forward dim (0.20) |
| `hold_last_s` / `transition_s` | final-frame hold (2.5) / spotlight + card ease (0.3) |
| `frames_dir` | PNG frames, inside the work dir; deleted after encode unless `--keep-frames`. `timeline.json` is written to its parent |
| `outputs` | `{gif, mp4}`; refuses to overwrite without `--force` |
| `blur` | `[{what, bbox:[x0,y0,x1,y1], t:[a,b]}]`, applied before overlays |
| `segments` | ordered list, below |

Segment: `{t:[a,b], speed, kind, ...}`

- `kind: "user"`: `rect`, `step` (N of N is the max step), `text` (≤8 words), optional `done` ("Done: …" line, lavender; `sub` is accepted as an alias), `side` left|right|above|below, optional `anchor_y` (card centre y), `marks:[{pt:[x,y], from:src_t}]` click beacons.
- `kind: "auto"`: `rect`, `text`, `side`, `anchor_y`, `marks` (breathing teal rings), optional `sub` (second line in light teal, e.g. "They keep their delegation"; fades in when it first appears, so add it on a later segment of the same event to reveal it).
- `kind: "plain"`: no overlay (dim fades off).
- `kind: "ff"`: 20% dim + centred chip; optional `text` overrides the chip.

Consecutive segments with the same `rect` keep the spotlight still; a new `rect` slides the cut-out there. Same `kind`+`text` keeps the card without re-fading, so split one event across speeds by repeating it. Output time per segment = `(b-a)/speed`; render prints the resulting timeline.

Flags: `--preview i,j` (one settled mid-segment frame per index), `--frames-only`, `--keep-frames`, `--force`.
