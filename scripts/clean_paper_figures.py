#!/usr/bin/env python3
"""Remove captions and surrounding page text from reproduced paper figures."""

from pathlib import Path
from PIL import Image, ImageChops, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "artifacts" / "paper_figures"

# Coordinates are expressed as fractions of the checked-in source crops.  The
# source images already contain the PDF figure at high resolution; these crops
# remove captions and body text without inventing or redrawing content.
CROPS = {
    "aion_principles.png": (0.02, 0.18, 0.98, 0.94),
    "anomamind_workflow.png": (0.01, 0.00, 0.99, 0.76),
    "chatts_overview.png": (0.02, 0.10, 0.98, 0.78),
    "merit_augmentation.png": (0.01, 0.00, 0.99, 0.98),
    "timeclaw_runtime.png": (0.01, 0.00, 0.99, 0.54),
    "timeseriesgym_benchmark.png": (0.01, 0.00, 0.99, 0.60),
    "tsagent_trace.png": (0.01, 0.05, 0.99, 0.36),
}


def trim_white(im: Image.Image, pad: int = 10) -> Image.Image:
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, "white")
    diff = ImageChops.difference(rgb, bg)
    bbox = diff.getbbox()
    if not bbox:
        return rgb
    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(rgb.width, right + pad)
    bottom = min(rgb.height, bottom + pad)
    return rgb.crop((left, top, right, bottom))


for name, frac in CROPS.items():
    path = FIG_DIR / name
    im = Image.open(path).convert("RGB")
    w, h = im.size
    box = tuple(int(v * s) for v, s in zip((w, h, w, h), frac))
    cropped = trim_white(im.crop(box), pad=8)
    # A light contrast pass restores the thin lines lost in rasterization while
    # leaving the original colors and labels unchanged.
    cropped = ImageEnhance.Contrast(cropped).enhance(1.08)
    cropped.save(path, dpi=(300, 300), optimize=True)
    print(f"cleaned {name}: {im.size} -> {cropped.size}")
