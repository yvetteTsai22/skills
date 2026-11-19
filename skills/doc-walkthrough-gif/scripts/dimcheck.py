"""Mean grey of a named unlit region in a decoded output frame (dim check).

  ffmpeg -v error -ss T -i OUT.gif -frames:v 1 frame.png      # T = output s inside a spotlight segment, not ff
  uv run --with pillow python dimcheck.py frame.png x0,y0,x1,y1 [--source-width=3024]
Box is OUTPUT px, or SOURCE px when --source-width is given. Pick a plain white area outside the
cut-out and away from cards. Expect ~155/255 at dim 0.35 on white UI (app "white" ~240 x 0.65, plus
GIF/lanczos softening); busy or non-white areas read higher, fast-forward (0.20) reads ~200.
"""
import sys

from PIL import Image, ImageStat


def main():
    opts = {a.split("=")[0]: a.split("=")[1] for a in sys.argv[1:] if a.startswith("--")}
    frame, box = [a for a in sys.argv[1:] if not a.startswith("--")][:2]
    im = Image.open(frame).convert("L")
    b = [float(v) for v in box.split(",")]
    if "--source-width" in opts:
        b = [v * im.width / float(opts["--source-width"]) for v in b]
    st = ImageStat.Stat(im.crop(tuple(int(v) for v in b)))
    print(f"mean {st.mean[0]:.1f}  stddev {st.stddev[0]:.1f}  (high stddev = busy area, reading unreliable)")


if __name__ == "__main__":
    main()
