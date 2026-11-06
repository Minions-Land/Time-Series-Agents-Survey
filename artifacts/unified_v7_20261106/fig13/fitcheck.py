"""Text-fit check for a built figure: flags text wider than its box, type below 11.5 pt, and overlapping text extents.

usage: python3 fitcheck.py Figure.pptx
"""
import sys
from PIL import ImageFont
from pptx import Presentation

FONTS = {False: '/System/Library/Fonts/Supplemental/Comic Sans MS.ttf',
         True: '/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf'}
_cache = {}


def width_in(t, pt, bold):
    k = (pt, bool(bold))
    if k not in _cache: _cache[k] = ImageFont.truetype(FONTS[bool(bold)], int(round(pt * 10)))
    return _cache[k].getlength(t) / 10 / 72


def walk(shapes):
    for s in shapes:
        if s.shape_type == 6: yield from walk(s.shapes)
        else: yield s


def check(path):
    p = Presentation(path)
    boxes, bad = [], 0
    for s in walk(p.slides[0].shapes):
        if not s.has_text_frame or not s.text_frame.text.strip(): continue
        tf = s.text_frame
        x, y, w, h = s.left / 914400, s.top / 914400, s.width / 914400, s.height / 914400
        ml, mr = (tf.margin_left or 0) / 914400, (tf.margin_right or 0) / 914400
        lines = []
        for para in tf.paragraphs:
            t = ''.join(r.text for r in para.runs)
            if not t: continue
            wd = sum(width_in(r.text, r.font.size.pt, r.font.bold) for r in para.runs)
            pt = max(r.font.size.pt for r in para.runs)
            if pt < 11.5: print(f'SMALL {pt}pt: {t!r}'); bad += 1
            lines.append((t, wd, pt, para.alignment))
        if not lines: continue
        avail = w - ml - mr
        tw = max(l[1] for l in lines)
        if tw > avail + 0.03 and not s.rotation:
            print(f'OVERFLOW {tw:.2f}>{avail:.2f} in: {lines[0][0]!r}'); bad += 1
        if s.rotation: continue
        th = sum(l[2] for l in lines) * 1.25 / 72
        al = lines[0][3]
        cx = x + w / 2
        lx = x + ml if al == 1 else (x + w - mr - tw if al == 3 else cx - tw / 2)
        boxes.append((lx, y + h / 2 - th / 2, tw, th, lines[0][0]))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
            oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
            if ox > 0.02 and oy > 0.02:
                print(f'COLLIDE {a[4]!r} / {b[4]!r}  ({ox:.2f} x {oy:.2f} in)'); bad += 1
    print('fitcheck:', 'clean' if not bad else f'{bad} issue(s)')


if __name__ == '__main__':
    check(sys.argv[1])
