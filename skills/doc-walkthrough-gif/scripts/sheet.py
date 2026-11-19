"""Contact sheet: tile frames in a grid, each labelled with its time, to scan many moments in one Read.

  uv run --with pillow python sheet.py OUT.png 'lo/p_%05d.png' STEP_S T1 T2 ...   # preview frames by source time
  uv run --with pillow python sheet.py OUT.png FILE1.png FILE2.png ...           # any frames, labelled by name
Options: --cols=N (default 2), --tile=W (tile width px, default 650).
Preview frames must come from the find_events.py recipe (frame i = START + i*STEP; %05d index from 1
when START is 0). Times map to index round(t/STEP)+1.
"""
import os
import sys

from PIL import Image, ImageDraw


def main():
    opts = {a.split("=")[0]: a.split("=")[1] for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cols, tw = int(opts.get("--cols", 2)), int(opts.get("--tile", 650))
    out, rest = args[0], args[1:]
    if "%" in rest[0]:
        pat, step = rest[0], float(rest[1])
        items = [(pat % (int(round(float(t) / step)) + 1), t) for t in rest[2:]]
    else:
        items = [(f, os.path.basename(f)) for f in rest]
    missing = [f for f, _ in items if not os.path.exists(f)]
    if missing:
        sys.exit(f"missing: {missing}")
    ims = [Image.open(f).convert("RGB") for f, _ in items]
    th = int(ims[0].height * tw / ims[0].width)
    sheet = Image.new("RGB", (tw * cols, th * ((len(ims) + cols - 1) // cols)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (im, (_, label)) in enumerate(zip(ims, items)):
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im.resize((tw, th)), (x, y))
        d.rectangle((x, y, x + 8 + 7 * len(str(label)), y + 16), fill="red")
        d.text((x + 4, y + 2), str(label), fill="white")
    sheet.save(out)
    print("wrote", out, sheet.size)


if __name__ == "__main__":
    main()
