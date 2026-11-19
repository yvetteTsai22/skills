"""Print times where consecutive low-res preview frames change (candidate events).

Make previews from REAL pts (VFR-safe), e.g. every 0.25 s of source time, 756 wide:
  ffmpeg -v error -i SRC.mov -vf "fps=4,scale=756:-2" -frame_pts 1 lo/p_%05d.png
Then:
  uv run --with pillow python find_events.py 'lo/p_*.png' START_T STEP_S [THRESHOLD]
Output: time  mean_abs_diff  mean_luma. Re-run with a smaller STEP_S near changes.
Whole-frame diff misses small changes (a card moving columns, a status chip, a new chat line).
Region probe: --box=x0,y0,x1,y1 (PREVIEW px) prints every time that region's mean luma changes;
probe each column's card area, the status chip and the chat bottom separately.
"""
import glob
import sys

from PIL import Image, ImageChops, ImageStat


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--box")]
    box = next((tuple(int(v) for v in a.split("=", 1)[1].split(",")) for a in sys.argv[1:]
                if a.startswith("--box=")), None)
    pattern, t0, step = args[0], float(args[1]), float(args[2])
    thr = float(args[3]) if len(args) > 3 else 0.3
    files = sorted(glob.glob(pattern))
    if not files:
        sys.exit(f"no files match {pattern}")
    prev = None
    for i, f in enumerate(files):
        im = Image.open(f).convert("L")
        if box:
            v = round(ImageStat.Stat(im.crop(box)).mean[0])
            if v != prev:
                print(round(t0 + i * step, 3), v)
            prev = v
            continue
        im = im.resize((95, 62))
        if prev is not None:
            d = ImageStat.Stat(ImageChops.difference(im, prev)).mean[0]
            if d > thr:
                print(round(t0 + i * step, 3), round(d, 2), round(ImageStat.Stat(im).mean[0]))
        prev = im


if __name__ == "__main__":
    main()
