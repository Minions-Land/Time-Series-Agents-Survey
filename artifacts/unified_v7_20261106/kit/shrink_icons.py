"""Make print-size copies of the clay icons for embedding (keeps the 512 px masters untouched).

Icons print at <= ~0.75 in, so 320 px with a 256-colour palette (alpha kept) is enough and makes each figure
several times smaller. Run again after adding icons:  python3 shrink_icons.py
"""
import glob, os
from PIL import Image
from v7kit import ICON_DIR

EMBED = ICON_DIR + '_print'
os.makedirs(EMBED, exist_ok=True)
for f in sorted(glob.glob(os.path.join(ICON_DIR, '*.png'))):
    im = Image.open(f).convert('RGBA').resize((320, 320), Image.LANCZOS)
    im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG).save(
        os.path.join(EMBED, os.path.basename(f)), optimize=True)
print(len(os.listdir(EMBED)), 'icons ->', EMBED)
