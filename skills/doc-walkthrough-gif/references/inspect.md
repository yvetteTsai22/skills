# Inspecting a recording: events, coordinates, dim, size

## Scale rule

Spec coordinates are **SOURCE px** (e.g. 3024x1964 Retina). Previews (756 wide), contact-sheet tiles and output frames (1300 wide) are all scaled. Never read a coordinate off a scaled image by eye: run `grid.py` with `--source-width` (from `ffprobe`) and read the labels, which are already source px. `find_events.py --box` is the one tool that takes **preview** px. A rect that lands 2x or 4x off is this mistake.

## Finding events

1. Previews with real pts: `ffmpeg -v error -i SRC.mov -vf "fps=4,scale=756:-2" -frame_pts 1 lo/p_%05d.png`.
2. Whole-frame diff: `find_events.py 'lo/p_*.png' 0 0.25`. Catches page changes, menus, scrolling.
3. **Region probes**, always, for every place an automatic change can land: each board column's card area (counts), the status chip, the chat/Slack bottom, the activity log tail. `find_events.py 'lo/p_*.png' 0 0.25 --box=x0,y0,x1,y1`. A card moving columns or a chip changing colour is invisible to step 2.
4. Scan candidates on a contact sheet: `sheet.py sheet.png 'lo/p_%05d.png' 0.25 T1 T2 ...` (one Read for many moments), then Read single frames where it matters.
5. Coordinates: `grid.py lo/p_00123.png g.png --source-width=3024`, and `--zoom=x0,y0,x1,y1` (source px) for tight rects around small targets.
6. End of recording: macOS dims/overlays the screen in the last moments of a capture. Find where it starts and end the last segment before it.

`timeline.json` is written by `render.py` (also on `--preview`) next to `frames_dir`: per segment `{event, kind, sub, source_t, output_t, bbox}` plus the privacy regions from `blur`.

## Dim check

On the final GIF, inside a spotlight segment (not fast-forward):
`ffmpeg -v error -ss T -i out.gif -frames:v 1 f.png` then `dimcheck.py f.png x0,y0,x1,y1 --source-width=3024` on a named plain white area outside the cut-out. Expect ~155/255 at dim 0.35. Busy or non-white areas read higher (stddev tells you); fast-forward (dim 0.20) reads ~200.

## Size budget

Real outputs: GIF 7.8–14.5 MB for 26–39 s at 1300 wide; busy Slack/board recordings sit at the top. MP4 ~2 MB, always produced alongside. Over budget, in this order, re-checking size after each:

1. Crop to the relevant pane(s).
2. Reduce width (e.g. `out_width: 1100`).
3. Shorten holds / raise fast-forward speed.
4. Lower fps in fast-forward segments.
5. Only then gifski `--quality 80`.

gifski lossy/motion flags stay off at every rung.
