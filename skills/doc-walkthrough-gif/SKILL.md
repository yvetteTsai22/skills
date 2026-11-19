---
name: doc-walkthrough-gif
description: Turn a screen recording (.mov) into an annotated walkthrough GIF + MP4 for docs, Supademo style (spotlight, step cards, automatic-event cards, fast-forward). Use for "turn this screen recording into a GIF for docs", "annotate a recording", "make a walkthrough GIF", 錄影轉 gif, 動圖.
---

# Doc walkthrough GIF

Turns a user's screen recording into `<name>.gif` + `<name>.mp4` for a docs page. Scripts live in `scripts/`; the worked example is `examples/stack-start.json`.

## Guardrails

- The source `.mov` is **read-only**: never move, rename, overwrite or delete it.
- Intermediates go in a user-approved **work dir** (e.g. `~/Documents/screenshots/_work/<name>/`), never in the repo. Ask for one if none is given.
- Final outputs: docs assets dir, plain `<name>.gif` / `<name>.mp4`. Drafts carry a suffix (`.v2`, `.plain`) and are moved out of the repo to a drafts folder, never deleted.

## Steps

1. **Tools.** `ffmpeg`, `ffprobe`, `gifski` (`brew install ffmpeg gifski`). Python only via `uv run --with pillow`. Homebrew ffmpeg has no `drawtext`, so every graphic is drawn in Pillow. Done when all three answer `-version`.
2. **Timeline.** macOS recordings are variable frame rate with gaps: `-ss` + one frame mis-times events by seconds. Decode low-res previews with real pts and run `scripts/find_events.py`; whole-frame diff misses small changes, so also **probe the column counts, status chip and chat bottom** with `--box`. Scan on a contact sheet (`sheet.py`), read coordinates with `grid.py`. **Scale rule:** spec coordinates are SOURCE px; never eyeball them off a preview. macOS dims the screen at the end of a recording: end the last segment before it. Recipes: `references/inspect.md`. Quote `-ss` args in zsh. Done when you have every event (user or auto, source time, source-px bbox) and every privacy region (assignee/member lists, emails: region + time range).
3. **Truth check.** Compare the recording with what the docs claim. If it differs (ticket moves unexpectedly, change happens off-screen or only after a manual reload), report it to the user with a cut-vs-re-record recommendation; never hide it. List colleagues' names visible in chat history (Slack @mentions, authors) with region + time so the user decides on blur. Recording tips: `references/recording-tips.md`.
4. **Spec.** Write `<work dir>/spec.json` (schema: `references/spec.md`) with segments, speeds, overlays and blur. Design rules (step vs automatic, pacing, placement): `references/design.md`. Done when every event from step 2 is in it: every `user` event a numbered step, every `auto` event is an automatic card, and the planned duration is 30–40 s.
5. **Preview.** `uv run --with pillow python scripts/render.py spec.json --preview 0,3,7` renders one settled frame per listed segment into `frames_dir` and writes `timeline.json` (per segment `{event, kind, sub, source_t, output_t, bbox}` + privacy) next to it. Read every frame; fix placement and text until clean. A plain cut with no overlays uses `scripts/cut.sh` instead.
6. **Render.** Run `render.py spec.json` with suffixed draft outputs first. It decodes only the needed ranges from the `.mov`, composites at source resolution, lanczos-downscales to 1300 wide, encodes once: `gifski --fps 12 --width 1300 --quality 90` (no lossy/motion flags; without `--width` gifski silently caps at 650 px) and `libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart`. Expect GIF 8–15 MB for 26–39 s (busy Slack/board views at the top), MP4 ~2 MB. Over budget: follow the ladder in `references/inspect.md`.
7. **Verify.** Extract frames from the final GIF at every overlay midpoint and read them: placement, crispness, blur covering every private region, cards not covering the target or the line above it, dim ~155/255 on a plain white unlit area (`dimcheck.py`, not during fast-forward). `ffprobe` both outputs. Done when width matches `out_width` and every overlay checked.
8. **Finish.** Promote the approved draft to the plain names, move other drafts out of the repo, delete frame folders (keep spec and timeline). Report dimensions, size, duration, peak and final work-dir size, and any truth-check findings.

## Known failure

Grainy output came from building off a 0.17 Mbps downscaled intermediate plus gifski lossy. Always decode straight from the `.mov`, keep intermediates lossless (PNG/ffv1), compress once.
