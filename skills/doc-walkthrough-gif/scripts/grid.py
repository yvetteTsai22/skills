"""Draw labelled gridlines in SOURCE pixels on a (preview or source) frame, to read spec coordinates.

  uv run --with pillow python grid.py FRAME.png OUT.png --source-width=3024 [--every=100] [--zoom=x0,y0,x1,y1]
Labels are SOURCE px whatever the frame's size: read a coordinate off the labels and put it straight
in the spec. --zoom crops to a SOURCE-px box (and upscales) for precise rects around small targets.
"""
import sys

from PIL import Image, ImageDraw


def main():
    opts = {a.split("=")[0]: a.split("=")[1] for a in sys.argv[1:] if a.startswith("--")}
    src, out = [a for a in sys.argv[1:] if not a.startswith("--")][:2]
    if "--source-width" not in opts:
        sys.exit("--source-width is required (ffprobe the .mov); it sets the source/frame scale")
    im = Image.open(src).convert("RGB")
    s = im.width / float(opts["--source-width"])  # frame px per source px
    every = int(opts.get("--every", 100))
    x0, y0, x1, y1 = 0, 0, im.width / s, im.height / s
    if "--zoom" in opts:
        x0, y0, x1, y1 = (float(v) for v in opts["--zoom"].split(","))
        im = im.crop(tuple(int(v * s) for v in (x0, y0, x1, y1)))
        z = max(1.0, 1300 / im.width)
        im = im.resize((int(im.width * z), int(im.height * z)), Image.LANCZOS)
        s *= z
    d = ImageDraw.Draw(im, "RGBA")
    for v in range(int(x0 // every + 1) * every, int(x1), every):
        x = (v - x0) * s
        major = v % (every * 5) == 0
        d.line((x, 0, x, im.height), fill=(255, 0, 0, 200 if major else 90), width=1)
        d.text((x + 2, 2), str(v), fill=(255, 0, 0, 255))
    for v in range(int(y0 // every + 1) * every, int(y1), every):
        y = (v - y0) * s
        major = v % (every * 5) == 0
        d.line((0, y, im.width, y), fill=(0, 0, 255, 200 if major else 90), width=1)
        d.text((2, y + 2), str(v), fill=(0, 0, 255, 255))
    im.save(out)
    print("wrote", out, "labels in SOURCE px")


if __name__ == "__main__":
    main()
