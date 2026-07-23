#!/usr/bin/env python3
"""Render a ~15s Intra Flow product demo GIF (pt speech → EN text at cursor)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Brand tokens (approx sRGB from DESIGN.md electric indigo / graphite / paper)
GRAPHITE = (28, 30, 40)
GRAPHITE_2 = (40, 43, 56)
PAPER = (244, 242, 236)
PAPER_2 = (230, 227, 218)
SIGNAL = (108, 92, 231)       # electric indigo
SIGNAL_HOT = (148, 130, 245)
SIGNAL_DEEP = (72, 62, 170)
INK_DIM = (160, 162, 175)
LINE = (55, 58, 72)
WHITE = (250, 249, 246)
GREEN_OK = (90, 200, 140)     # only for tiny success check — keep rare

W, H = 720, 720
FPS = 12
DURATION = 15.0
N = int(FPS * DURATION)

OUT = Path(__file__).resolve().parents[1] / "docs" / "brand" / "intra-flow-demo-15s.gif"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size=size, index=1 if bold and p.endswith(".ttc") else 0)
        except OSError:
            continue
    return ImageFont.load_default()


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def clamp01(t: float) -> float:
    return max(0.0, min(1.0, t))


def ease(t: float) -> float:
    t = clamp01(t)
    return 1 - (1 - t) ** 3


def rounded(draw: ImageDraw.ImageDraw, box, r: int, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def waveform(draw: ImageDraw.ImageDraw, cx: int, cy: int, w: int, h: int, t: float, live: bool):
    bars = 22
    gap = 4
    bw = max(3, (w - gap * (bars - 1)) // bars)
    for i in range(bars):
        # funnel: taller on the left, taper toward cursor (right)
        funnel = 1.0 - (i / (bars - 1)) ** 1.35
        phase = t * 10 + i * 0.55
        amp = (0.35 + 0.65 * abs(math.sin(phase))) if live else 0.18
        bh = max(4, int(h * funnel * amp))
        x0 = cx - w // 2 + i * (bw + gap)
        y0 = cy - bh // 2
        color = SIGNAL if i % 2 == 0 else SIGNAL_HOT
        draw.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=2, fill=color)


def typewriter(full: str, t: float) -> str:
    n = int(len(full) * clamp01(t))
    return full[:n]


def draw_frame(i: int) -> Image.Image:
    t = i / FPS
    img = Image.new("RGB", (W, H), GRAPHITE)
    d = ImageDraw.Draw(img)

    # soft signal wash
    for y in range(H):
        k = y / H
        r = int(lerp(GRAPHITE[0], GRAPHITE_2[0], k * 0.4))
        g = int(lerp(GRAPHITE[1], GRAPHITE_2[1], k * 0.4))
        b = int(lerp(GRAPHITE[2], 70, k * 0.35))
        d.line([(0, y), (W, y)], fill=(r, g, b))

    f_brand = font(15, bold=True)
    f_mono = font(12)
    f_ui = font(14)
    f_body = font(18)
    f_body_sm = font(15)
    f_phase = font(13, bold=True)
    f_big = font(22, bold=True)

    # top brand
    d.text((28, 22), "INTRA FLOW", font=f_brand, fill=SIGNAL_HOT)
    d.text((150, 24), "voice → ordered language at the cursor", font=f_mono, fill=INK_DIM)

    # app window
    win = [36, 56, W - 36, H - 110]
    rounded(d, win, 16, fill=(34, 36, 48), outline=LINE, width=2)
    # title bar
    rounded(d, [win[0], win[1], win[2], win[1] + 40], 16, fill=(42, 44, 58))
    d.rectangle([win[0], win[1] + 24, win[2], win[1] + 40], fill=(42, 44, 58))
    for j, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([win[0] + 16 + j * 18, win[1] + 14, win[0] + 28 + j * 18, win[1] + 26], fill=c)
    d.text((win[0] + 80, win[1] + 12), "Claude  ·  Dev Mode", font=f_ui, fill=PAPER)

    # composer card
    card = [win[0] + 22, win[1] + 58, win[2] - 22, win[3] - 70]
    rounded(d, card, 12, fill=PAPER, outline=PAPER_2, width=1)
    d.text((card[0] + 18, card[1] + 14), "COMPOSER", font=f_mono, fill=(120, 118, 110))
    d.text((card[2] - 110, card[1] + 14), "⌥ hold", font=f_mono, fill=(120, 118, 110))

    # phase machine
    # 0-1.8 idle | 1.8-5.5 capturing | 5.5-8.5 partial pt | 8.5-11 rewrite | 11-15 final EN
    if t < 1.8:
        phase = "Pronto"
        phase_color = (120, 118, 110)
        live = False
        show_partial = False
        show_final = False
        partial_t = 0.0
        final_t = 0.0
    elif t < 5.5:
        phase = "Ouvindo"
        phase_color = SIGNAL
        live = True
        show_partial = False
        show_final = False
        partial_t = 0.0
        final_t = 0.0
    elif t < 8.5:
        phase = "Transcrevendo"
        phase_color = SIGNAL_HOT
        live = True
        show_partial = True
        show_final = False
        partial_t = ease((t - 5.5) / 3.0)
        final_t = 0.0
    elif t < 11.0:
        phase = "Reescrevendo"
        phase_color = SIGNAL_DEEP
        live = False
        show_partial = True
        show_final = False
        partial_t = 1.0
        final_t = 0.0
    else:
        phase = "Injetando" if t < 12.2 else "Pronto"
        phase_color = GREEN_OK if t >= 12.2 else SIGNAL
        live = False
        show_partial = False
        show_final = True
        partial_t = 1.0
        final_t = ease((t - 11.0) / 2.2)

    # Flow Bar chip
    chip_w = 200
    chip = [W // 2 - chip_w // 2, win[3] - 52, W // 2 + chip_w // 2, win[3] - 22]
    rounded(d, chip, 14, fill=GRAPHITE_2, outline=SIGNAL if live else LINE, width=2)
    d.text((chip[0] + 18, chip[1] + 6), phase, font=f_phase, fill=phase_color)
    # mini bars in chip
    if live or (5.5 <= t < 11):
        waveform(d, chip[2] - 48, (chip[1] + chip[3]) // 2, 56, 16, t, live)

    # text area
    text_top = card[1] + 48
    text_left = card[0] + 22
    cursor_x = text_left
    cursor_y = text_top

    pt = "então tipo preciso de um prompt forte pro Claude — arquitetura do Intra Flow, modos e por que BYOK"
    en = (
        "Write a concise product brief for Intra Flow: macOS voice dictation that "
        "rewrites speech into ordered text at the cursor. Cover Modes, Surface-aware "
        "Dev Mode, and why BYOK with lean OpenAI models beats a monthly subscription."
    )

    if t < 5.5:
        # empty composer + living I-beam
        blink = (i // 6) % 2 == 0
        if blink or live:
            # I-beam caret
            x = text_left
            d.rectangle([x - 1, text_top, x + 2, text_top + 28], fill=SIGNAL)
            d.rectangle([x - 5, text_top, x + 6, text_top + 3], fill=SIGNAL)
            d.rectangle([x - 5, text_top + 25, x + 6, text_top + 28], fill=SIGNAL)
        if live:
            # waveform funneling into cursor (Composer × Waveform)
            waveform(d, text_left + 130, text_top + 50, 200, 40, t, True)
            d.text((text_left + 250, text_top + 40), "→", font=f_big, fill=SIGNAL_HOT)
            # glow at caret
            for r in (18, 12, 6):
                alpha_box = [text_left - r, text_top + 14 - r, text_left + r, text_top + 14 + r]
                # approximate glow with indigo rings
                d.ellipse(alpha_box, outline=SIGNAL_HOT if r < 12 else SIGNAL_DEEP, width=1)
            d.text((text_left, text_top + 90), "Hold ⌥  ·  speak freely in Portuguese", font=f_body_sm, fill=(110, 108, 100))
    elif show_partial and not show_final:
        shown = typewriter(pt, partial_t)
        # wrap manually
        words = shown.split(" ")
        lines: list[str] = []
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=f_body_sm) > (card[2] - card[0] - 48):
                lines.append(cur)
                cur = w
            else:
                cur = trial
        if cur:
            lines.append(cur)
        y = text_top
        for line in lines[:6]:
            d.text((text_left, y), line, font=f_body_sm, fill=(90, 88, 82))
            y += 24
        # dim label
        d.text((text_left, card[3] - 36), "Partial (pt-BR brain dump)", font=f_mono, fill=(150, 148, 140))
        if t >= 8.5:
            d.text((text_left + 260, card[3] - 36), "→ ordering…", font=f_mono, fill=SIGNAL)
    else:
        shown = typewriter(en, final_t)
        words = shown.split(" ")
        lines = []
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=f_body_sm) > (card[2] - card[0] - 48):
                lines.append(cur)
                cur = w
            else:
                cur = trial
        if cur:
            lines.append(cur)
        y = text_top
        for line in lines[:8]:
            d.text((text_left, y), line, font=f_body_sm, fill=GRAPHITE)
            y += 24
        # caret at end
        if final_t < 1.0 or (i // 6) % 2 == 0:
            last = lines[-1] if lines else ""
            cx = text_left + int(d.textlength(last, font=f_body_sm)) + 2
            cy = text_top + 24 * max(0, len(lines) - 1)
            d.rectangle([cx, cy, cx + 2, cy + 22], fill=SIGNAL)
        d.text((text_left, card[3] - 36), "Final at cursor  ·  English prompt", font=f_mono, fill=SIGNAL_DEEP)
        if t >= 12.2:
            d.text((card[2] - 120, card[3] - 36), "✓ injected", font=f_mono, fill=SIGNAL)

    # bottom story beats
    beats = [
        (0.0, "1 Trigger"),
        (1.8, "2 Capture"),
        (5.5, "3 Transcript"),
        (8.5, "4 Rewrite"),
        (11.0, "5 Injection"),
    ]
    bx = 40
    for start, label in beats:
        on = t >= start
        d.text((bx, H - 48), label, font=f_mono, fill=SIGNAL_HOT if on else INK_DIM)
        bx += 130

    d.text((40, H - 28), "pt-BR speech  →  ordered English at the cursor", font=f_mono, fill=INK_DIM)

    # Option key badge during capture
    if 1.8 <= t < 5.5:
        badge = [W - 170, 64, W - 48, 100]
        rounded(d, badge, 8, fill=SIGNAL_DEEP, outline=SIGNAL_HOT, width=2)
        d.text((badge[0] + 14, badge[1] + 8), "⌥  HOLD", font=f_phase, fill=WHITE)

    return img


def main() -> None:
    frames = [draw_frame(i) for i in range(N)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # duration per frame in ms
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / FPS),
        loop=0,
        optimize=True,
        disposal=2,
    )
    # recompress via ffmpeg for smaller palette GIF if available
    tmp = OUT.with_suffix(".mp4")
    import subprocess

    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(OUT),  # won't work from gif well — rebuild from pngs instead
        ],
        check=False,
        capture_output=True,
    )
    # Write PNG sequence then ffmpeg palette GIF for quality/size
    seq = OUT.parent / "_gif_frames"
    seq.mkdir(exist_ok=True)
    for i, fr in enumerate(frames):
        fr.save(seq / f"f{i:04d}.png")
    palette = seq / "palette.png"
    final = OUT
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(seq / "f%04d.png"),
            "-vf", "palettegen=max_colors=128",
            str(palette),
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(seq / "f%04d.png"),
            "-i", str(palette),
            "-lavfi", "paletteuse=dither=bayer:bayer_scale=3",
            "-loop", "0",
            str(final),
        ],
        check=True,
        capture_output=True,
    )
    # cleanup frames
    for p in seq.glob("*"):
        p.unlink()
    seq.rmdir()
    print(f"Wrote {final} ({final.stat().st_size / 1024:.0f} KB, {N} frames, {DURATION}s)")


if __name__ == "__main__":
    main()
