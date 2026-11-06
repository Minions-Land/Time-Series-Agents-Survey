"""Generate new clay icons in the shared style with codex, key out the green background, save to ICON_DIR.

usage: python3 make_icons.py name1="subject one" name2="subject two" ...
Names must be new snake_case names (existing icons in ICON_DIR are never overwritten). Generation takes minutes.
If codex exits early (e.g. model at capacity) images may still be in ~/.codex/generated_images/<session>/; key them
with:  python3 make_icons.py --key <png> <name>
"""
import os, subprocess, sys, time, glob
import numpy as np
from PIL import Image
from v7kit import ICON_DIR, HERE

STYLE = ('cute glossy 3D clay render like modern app icons, soft rounded shapes, gentle studio lighting, limited palette of '
         'navy, cream, teal, warm orange and soft purple, thin dark navy outline, centered subject filling about 80% of the '
         'frame, NO text, NO letters, NO digits, NO shadow on background. Background must be a perfectly flat solid pure '
         'green #00FF00 (chroma key) filling the entire canvas, and the subject must not contain that green.')


def key(src, dst):
    im = np.asarray(Image.open(src).convert('RGB')).astype(np.int16)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    gr = g - np.maximum(r, b)
    alpha = np.clip(255 - (gr - 40) * 4, 0, 255).astype(np.uint8)
    out = im.copy(); out[..., 1] = np.where(gr > 0, np.maximum(r, b), g)
    img = Image.fromarray(np.dstack([out.astype(np.uint8), alpha]), 'RGBA')
    bbox = img.getchannel('A').point(lambda a: 255 if a > 24 else 0).getbbox()
    if bbox: img = img.crop(bbox)
    side = max(img.size); pad = int(side * 0.04)
    sq = Image.new('RGBA', (side + 2 * pad, side + 2 * pad), (0, 0, 0, 0))
    sq.paste(img, ((sq.width - img.width) // 2, (sq.height - img.height) // 2))
    sq.resize((512, 512), Image.LANCZOS).save(dst)


def main(args):
    if args[:1] == ['--key']:
        key(args[1], os.path.join(ICON_DIR, args[2] + '.png')); print('keyed', args[2]); return
    want = dict(a.split('=', 1) for a in args)
    for n in want:
        if os.path.exists(os.path.join(ICON_DIR, n + '.png')):
            sys.exit(f'icon {n} already exists; pick a new name')
    raw = os.path.join(HERE, 'raw_%d' % int(time.time() * 1000)); os.makedirs(raw)
    items = '; '.join(f'{n} ({s})' for n, s in want.items())
    prompt = (f'Use your image generation tool to create {len(want)} separate square icon images (1024x1024 each), one subject '
              f'per image, and save them as PNG files in {raw}/ named <name>.png using exactly the names below.\n'
              f'Style for ALL icons: {STYLE}\nIcons (name: subject): {items}.\nDo not do anything else.')
    subprocess.run(['codex', 'exec', '--skip-git-repo-check', '--sandbox', 'workspace-write', '-C', raw, '-'],
                   input=prompt.encode(), timeout=1500)
    for n in want:
        f = os.path.join(raw, n + '.png')
        if os.path.exists(f):
            key(f, os.path.join(ICON_DIR, n + '.png')); print('new icon', n)
        else:
            print('missing', n, '(look in ~/.codex/generated_images/ newest folder, then use --key)')


if __name__ == '__main__':
    main(sys.argv[1:])
