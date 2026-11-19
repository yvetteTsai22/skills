"""Render an annotated ("Supademo style") walkthrough GIF + MP4 from a screen recording.

Usage:
  uv run --with pillow python render.py SPEC.json              # full render + encode
  uv run --with pillow python render.py SPEC.json --preview 0,6 # first frame of segments 0 and 6 only
  uv run --with pillow python render.py SPEC.json --frames-only # render PNGs, skip encoding

All coordinates in the spec are SOURCE pixels (e.g. 3024x1964 for a Retina capture).
Times are SOURCE pts seconds. See ../references/spec.md for the schema.
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
INDIGO = (79, 70, 229)
TEAL = (20, 184, 166)
SLATE = (30, 41, 59)
LAVENDER = (199, 210, 254)
TEAL_LIGHT = (153, 246, 228)


class Ctx:
    """Per-render geometry, fonts and settings derived from the spec."""

    def __init__(self, spec):
        self.src = os.path.expanduser(spec["source"])
        self.W, self.H = spec.get("source_size") or probe_size(self.src)
        self.OW = spec.get("out_width", 1300)
        self.OH = int(round(self.H * self.OW / self.W / 2)) * 2
        self.fps = spec.get("fps", 12)
        self.K = self.W / self.OW  # source px per output px
        self.dim = spec.get("dim", 0.35)
        self.ff_dim = spec.get("ff_dim", 0.20)
        self.ff_text = spec.get("ff_text", "Fast-forward · a few minutes later")
        self.hold = spec.get("hold_last_s", 2.5)
        self.trans = spec.get("transition_s", 0.3)
        self.product = spec.get("product", "").upper()
        self.blur = spec.get("blur", [])
        self.nsteps = max([s.get("step", 0) for s in spec["segments"]] + [0])
        k = self.K
        self.f_head = ImageFont.truetype(FONT, int(11.5 * k), index=1)
        self.f_body = ImageFont.truetype(FONT, int(16.5 * k), index=10)
        self.f_pill = ImageFont.truetype(FONT, int(11.5 * k), index=10)
        self.f_sub = ImageFont.truetype(FONT, int(12.5 * k), index=10)
        self.f_chip = ImageFont.truetype(FONT, int(18 * k), index=10)
        self._masks = {}


def probe_size(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height", "-of", "csv=p=0", path], text=True)
    w, h = out.strip().split(",")[:2]
    return int(w), int(h)


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp_rect(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(4))


def decode(c, a, b, speed, limit=None):
    """Yield (src_t, frame) every speed/fps seconds of real source pts (VFR-safe: fps filter on pts)."""
    rate = c.fps / speed
    n = int(round((b - a) * rate))
    if limit:
        n = min(n, limit)
    pre = max(0.0, a - 3.0)
    cmd = ["ffmpeg", "-v", "error", "-copyts", "-ss", f"{pre:.3f}", "-i", c.src,
           "-vf", f"fps=fps={rate}:start_time={a}", "-frames:v", str(n),
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    size = c.W * c.H * 3
    last = None
    try:
        for i in range(n):
            buf = proc.stdout.read(size)
            if len(buf) == size:
                last = Image.frombytes("RGB", (c.W, c.H), buf)
            if last is None:
                raise RuntimeError(f"no frame decoded for segment {a}-{b}")
            yield a + i / rate, last
    finally:
        proc.stdout.close()
        proc.kill() if limit else proc.wait()


# ---------- drawing primitives ----------

def spot_mask(c, rect):
    """Rounded cut-out, tightly feathered (~2.5 px at output)."""
    key = tuple(int(v) for v in rect)
    if key in c._masks:
        return c._masks[key]
    s = 4
    m = Image.new("L", (c.W // s, c.H // s), 0)
    x0, y0, x1, y1 = (v / s for v in key)
    ImageDraw.Draw(m).rounded_rectangle((x0, y0, x1, y1), radius=12 / s * c.K, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(2.5 * c.K / s)).resize((c.W, c.H), Image.BILINEAR)
    if len(c._masks) > 64:
        c._masks.clear()
    c._masks[key] = m
    return m


def draw_beacon(c, d, pt, phase):
    """Click beacon: two staggered expanding rings + solid dot. Redraw every frame."""
    x, y = pt
    k = c.K
    r = 7 * k
    for off in (0.0, 0.5):
        u = (phase + off) % 1.0
        rr = r + u * 16 * k
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=INDIGO + (int(200 * (1 - u) ** 1.5),),
                  width=int(2.2 * k))
    d.ellipse((x - r - 2 * k, y - r - 2 * k, x + r + 2 * k, y + r + 2 * k), fill=(255, 255, 255, 235))
    d.ellipse((x - r, y - r, x + r, y + r), fill=INDIGO + (255,))


def draw_changed(c, d, pt, phase):
    """Automatic-change marker: soft breathing teal ring, no click dot."""
    x, y = pt
    s = 0.5 + 0.5 * math.sin(phase * 2 * math.pi)
    rr = (11 + 3 * s) * c.K
    d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=TEAL + (int(140 + 80 * s),), width=int(2.4 * c.K))
    r2 = rr + 5 * c.K
    d.ellipse((x - r2, y - r2, x + r2, y + r2), outline=TEAL + (int(50 + 40 * s),), width=int(2 * c.K))


def draw_outline(c, layer, rect, alpha, auto):
    k = c.K
    if auto:  # teal outline + glow
        g = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle(rect, radius=12 * k, outline=TEAL + (int(200 * alpha),),
                                            width=int(5 * k))
        layer.alpha_composite(g.filter(ImageFilter.GaussianBlur(4 * k)))
        ImageDraw.Draw(layer).rounded_rectangle(rect, radius=12 * k, outline=TEAL + (int(235 * alpha),),
                                                width=int(1.8 * k))
    else:  # thin indigo edge
        ImageDraw.Draw(layer).rounded_rectangle(rect, radius=12 * k, outline=INDIGO + (int(210 * alpha),),
                                                width=int(1.6 * k))


def draw_bolt(d, x, y, s, col):
    pts = [(0.55, 0), (0.1, 0.55), (0.45, 0.55), (0.3, 1), (0.9, 0.4), (0.52, 0.4), (0.75, 0)]
    d.polygon([(x + px * s, y + py * s) for px, py in pts], fill=col)


def place(c, rect, side, anchor_y, cw, ch):
    gap = 16 * c.K
    x0, y0, x1, y1 = rect
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2 if anchor_y is None else anchor_y
    if side == "left":
        bx, by = x0 - gap - cw, cy - ch / 2
    elif side == "right":
        bx, by = x1 + gap, cy - ch / 2
    elif side == "above":
        bx, by = cx - cw / 2, y0 - gap - ch
    else:
        bx, by = cx - cw / 2, y1 + gap
    m = 12 * c.K
    return max(m, min(c.W - m - cw, bx)), max(m, min(c.H - m - ch, by)), cx, cy


def pointer(c, d, side, bx, by, cw, ch, cx, cy, col):
    t = 9 * c.K
    if side in ("left", "right"):
        ay = max(by + 2 * t, min(by + ch - 2 * t, cy))
        if side == "left":
            d.polygon([(bx + cw, ay - t), (bx + cw + t, ay), (bx + cw, ay + t)], fill=col)
        else:
            d.polygon([(bx, ay - t), (bx - t, ay), (bx, ay + t)], fill=col)
    else:
        ax = max(bx + 2 * t, min(bx + cw - 2 * t, cx))
        if side == "above":
            d.polygon([(ax - t, by + ch), (ax, by + ch + t), (ax + t, by + ch)], fill=col)
        else:
            d.polygon([(ax - t, by), (ax, by - t), (ax + t, by)], fill=col)


def spaced(c, d, x, y, text, font, fill):
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + 1.2 * c.K
    return x


def spaced_width(c, d, text, font):
    return sum(d.textlength(ch, font=font) + 1.2 * c.K for ch in text)


def shadow(c, layer, box, alpha):
    k = c.K
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 4 * k, x1, y1 + 4 * k), radius=10 * k,
                                         fill=(0, 0, 0, int(100 * alpha)))
    layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8 * k)))


def draw_next_pill(c, d, px, y, ph, pw, col, a):
    k = c.K
    d.rounded_rectangle((px, y, px + pw, y + ph), radius=ph / 2, fill=(255, 255, 255, a))
    tx = px + 10 * k
    d.text((tx, y + ph / 2), "Next", font=c.f_pill, fill=col, anchor="lm")
    ax0 = tx + d.textlength("Next", font=c.f_pill) + 5 * k
    ax1, ay = ax0 + 10 * k, y + ph / 2
    lw = max(2, int(1.6 * k))  # arrow drawn as lines: the font lacks the glyph
    for seg in ((ax0, ay, ax1, ay), (ax1 - 4 * k, ay - 4 * k, ax1, ay), (ax1 - 4 * k, ay + 4 * k, ax1, ay)):
        d.line(seg, fill=col, width=lw)


def draw_user_card(c, layer, rect, seg, alpha, a2):
    k = c.K
    d = ImageDraw.Draw(layer)
    pad, ph = 14 * k, 22 * k
    head = f"STEP {seg['step']} OF {c.nsteps}"
    text, done = seg["text"], seg.get("done") or seg.get("sub")
    w2 = d.textlength(done, font=c.f_sub) if done else 0
    cw = max(spaced_width(c, d, head, c.f_head), d.textlength(text, font=c.f_body), w2) + 2 * pad
    ch = pad + 21 * k + 18 * k + (22 * k if done else 0) + 12 * k + ph + pad
    side = seg.get("side", "left")
    bx, by, cx, cy = place(c, rect, side, seg.get("anchor_y"), cw, ch)
    a = int(255 * alpha)
    col = INDIGO + (a,)
    shadow(c, layer, (bx, by, bx + cw, by + ch), alpha)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((bx, by, bx + cw, by + ch), radius=10 * k, fill=col)
    pointer(c, d, side, bx, by, cw, ch, cx, cy, col)
    y = by + pad
    spaced(c, d, bx + pad, y, head, c.f_head, LAVENDER + (a,))
    y += 21 * k
    d.text((bx + pad, y), text, font=c.f_body, fill=(255, 255, 255, a))
    y += 18 * k
    if done:
        y += 6 * k
        d.text((bx + pad, y), done, font=c.f_sub, fill=LAVENDER + (int(a * a2),))
        y += 16 * k
    y += 12 * k
    pw = d.textlength("Next", font=c.f_pill) + 10 * k + 26 * k
    draw_next_pill(c, d, bx + cw - pad - pw, y, ph, pw, col, a)


def draw_auto_card(c, layer, rect, seg, alpha, a2=1.0):
    k = c.K
    d = ImageDraw.Draw(layer)
    pad, bar, icon = 14 * k, 5 * k, 18 * k
    head = f"AUTOMATIC · {c.product}" if c.product else "AUTOMATIC"
    text, sub = seg["text"], seg.get("sub")
    hw = icon + 7 * k + spaced_width(c, d, head, c.f_head)
    w2 = d.textlength(sub, font=c.f_sub) if sub else 0
    cw = max(hw, d.textlength(text, font=c.f_body), w2) + 2 * pad + bar
    ch = pad + 21 * k + 18 * k + (22 * k if sub else 0) + pad + 4 * k
    side = seg.get("side", "below")
    bx, by, cx, cy = place(c, rect, side, seg.get("anchor_y"), cw, ch)
    a = int(255 * alpha)
    col = SLATE + (int(245 * alpha),)
    shadow(c, layer, (bx, by, bx + cw, by + ch), alpha)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((bx, by, bx + cw, by + ch), radius=10 * k, fill=col,
                        outline=TEAL + (int(160 * alpha),), width=int(1.2 * k))
    d.rounded_rectangle((bx, by, bx + bar + 10 * k, by + ch), radius=10 * k, fill=TEAL + (a,))
    d.rectangle((bx + bar, by + 1.2 * k, bx + bar + 10 * k, by + ch - 1.2 * k), fill=col)
    pointer(c, d, side, bx, by, cw, ch, cx, cy, col)
    x, y = bx + bar + pad, by + pad - 2 * k
    draw_bolt(d, x, y, icon * 0.95, TEAL + (a,))
    spaced(c, d, x + icon + 7 * k, y + 2 * k, head, c.f_head, TEAL + (a,))
    d.text((x, y + 23 * k), text, font=c.f_body, fill=(255, 255, 255, a))
    if sub:  # optional second line, light teal
        d.text((x, y + 47 * k), sub, font=c.f_sub, fill=TEAL_LIGHT + (int(a * a2),))


def draw_chip(c, layer, text):
    d = ImageDraw.Draw(layer)
    cw, ch = d.textlength(text, font=c.f_chip) + 44 * c.K, 44 * c.K
    x0, y0 = (c.W - cw) / 2, (c.H - ch) / 2
    d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=ch / 2, fill=(17, 24, 39, 225))
    d.text((c.W / 2, c.H / 2), text, font=c.f_chip, fill=(255, 255, 255, 255), anchor="mm")


# ---------- frame composition ----------

def apply_blur(c, img, src_t):
    for b in c.blur:
        if b["t"][0] <= src_t <= b["t"][1]:
            box = tuple(int(v) for v in b["bbox"])
            img.paste(img.crop(box).filter(ImageFilter.GaussianBlur(14 * c.K)), box)
    return img


def compose(c, frame, src_t, out_t, seg, st):
    img = apply_blur(c, frame.copy(), src_t)
    layer = Image.new("RGBA", (c.W, c.H), (0, 0, 0, 0))
    kind = seg["kind"]
    if st["cur"] is not None:
        u = ease((out_t - st["rect_start"]) / c.trans)
        r = lerp_rect(st["prev"], st["cur"], u) if st["prev"] is not None else st["cur"]
        fade = 1.0 if st["prev"] is not None else u
        dark = ImageEnhance.Brightness(img).enhance(1 - c.dim * fade)
        img = Image.composite(img, dark, spot_mask(c, r))
        ca = ease((out_t - st["card_start"]) / c.trans)
        auto = kind == "auto"
        draw_outline(c, layer, r, fade, auto)
        d = ImageDraw.Draw(layer)
        for m in seg.get("marks", []):
            if src_t >= m["from"]:
                if auto:
                    draw_changed(c, d, m["pt"], (out_t * 0.6) % 1.0)
                else:
                    draw_beacon(c, d, m["pt"], (out_t * 0.9) % 1.0)
        a2 = ease((out_t - st["done_start"]) / c.trans)
        if auto:
            draw_auto_card(c, layer, r, seg, ca, a2)
        else:
            draw_user_card(c, layer, r, seg, ca, a2)
    elif kind == "ff":
        img = ImageEnhance.Brightness(img).enhance(1 - c.ff_dim * ease((out_t - st["rect_start"]) / c.trans))
        draw_chip(c, layer, seg.get("text") or c.ff_text)
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    return img.resize((c.OW, c.OH), Image.LANCZOS)


def render(spec, frames_dir, preview=None):
    c = Ctx(spec)
    os.makedirs(frames_dir, exist_ok=True)
    st = {"prev": None, "cur": None, "rect_start": 0.0, "card_start": 0.0, "done_start": 0.0}
    card_key, done_key = None, None
    idx, out_t, last = 0, 0.0, None
    timeline = []
    for i, seg in enumerate(spec["segments"]):
        a, b = seg["t"]
        speed = seg.get("speed", 1)
        target = tuple(seg["rect"]) if seg["kind"] in ("user", "auto") else None
        if target != st["cur"]:
            st["prev"], st["cur"], st["rect_start"] = st["cur"], target, out_t
        if (seg["kind"], seg.get("text")) != card_key:
            card_key, st["card_start"] = (seg["kind"], seg.get("text")), out_t
        second = seg.get("done") or seg.get("sub")
        if second != done_key:
            done_key, st["done_start"] = second, out_t
        n = int(round((b - a) * c.fps / speed))
        timeline.append({"seg": i, "event": seg.get("text") or seg["kind"], "kind": seg["kind"],
                         "sub": second, "source_t": [a, b], "speed": speed,
                         "output_t": [round(out_t, 2), round(out_t + n / c.fps, 2)],
                         "bbox": seg.get("rect")})
        if preview is not None:
            if i in preview:
                # Mid-segment sample with transitions settled.
                src_t, frame = next(decode(c, a + (b - a) / 2, b, speed, limit=1))
                img = compose(c, frame, src_t, out_t + c.trans * 2, seg, st)
                img.save(f"{frames_dir}/preview_seg{i:02d}.png")
            out_t += n / c.fps
            continue
        for src_t, frame in decode(c, a, b, speed):
            last = compose(c, frame, src_t, out_t, seg, st)
            last.save(f"{frames_dir}/f{idx:05d}.png", compress_level=1)
            idx += 1
            out_t += 1 / c.fps
        print(f"seg {i} {a}-{b} x{speed} -> out {out_t:.2f}s", flush=True)
    if preview is None:
        for _ in range(int(c.hold * c.fps)):
            last.save(f"{frames_dir}/f{idx:05d}.png", compress_level=1)
            idx += 1
    total = out_t + (0 if preview is not None else c.hold)
    result = {"duration_s": round(total, 2), "events": timeline,
              "privacy": [{"what": b.get("what"), "bbox": b["bbox"], "t": b["t"]} for b in c.blur]}
    # timeline.json sits next to frames_dir (the work dir) and is kept after the render.
    tl_path = os.path.join(os.path.dirname(os.path.normpath(frames_dir)), "timeline.json")
    with open(tl_path, "w") as f:
        json.dump(result, f, indent=1)
    print(json.dumps({"frames": idx, **result}, indent=1))
    print("wrote", tl_path)
    return c


def encode(c, frames_dir, outputs, force):
    gif, mp4 = (os.path.expanduser(outputs[k]) for k in ("gif", "mp4"))
    for p in (gif, mp4):
        if os.path.exists(p) and not force:
            sys.exit(f"refusing to overwrite {p} (pass --force, or write a suffixed draft)")
    frames = sorted(f for f in os.listdir(frames_dir) if f.startswith("f") and f.endswith(".png"))
    # --width is mandatory: without it gifski silently caps at 650 px. No lossy/motion flags.
    subprocess.check_call(["gifski", "--fps", str(c.fps), "--width", str(c.OW), "--quality", "90",
                           "-o", gif] + [os.path.join(frames_dir, f) for f in frames])
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-framerate", str(c.fps), "-i",
                           os.path.join(frames_dir, "f%05d.png"), "-c:v", "libx264", "-crf", "18",
                           "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4])
    for p in (gif, mp4):
        info = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                        "stream=width,height:format=duration,size", "-of", "compact", p],
                                       text=True)
        print(p, info.strip().replace("\n", " | "))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--preview", help="comma list of segment indexes; renders one mid-segment frame each")
    ap.add_argument("--frames-only", action="store_true")
    ap.add_argument("--keep-frames", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs")
    args = ap.parse_args()
    with open(args.spec) as f:
        spec = json.load(f)
    frames_dir = os.path.expanduser(spec["frames_dir"])
    preview = [int(x) for x in args.preview.split(",")] if args.preview else None
    c = render(spec, frames_dir, preview)
    if preview is not None or args.frames_only:
        return
    encode(c, frames_dir, spec["outputs"], args.force)
    if not args.keep_frames:
        shutil.rmtree(frames_dir)


if __name__ == "__main__":
    main()
