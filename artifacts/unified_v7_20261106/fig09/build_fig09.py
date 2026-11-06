"""Figure 9 (fig:merit-augmentation) in the V7 house style: MERIT's construction of positive samples.

Top row, one numbered Task-Specific Harness zone per agent named in the manuscript (Retrieval / Augmentation / Review Agent):
  target x -> similarity shortlist -> LLM relevance review -> reference set R -> transformation selection
  -> two schematic candidates (small jitter keeps the peak order, block permutation changes it)
  -> review compares each view with x (judgment + rationale) -> "Correct": retain in memory M,
  "Error": rejection restarts retrieval (dashed return path).
Lower band: x + M u R form the positive samples -> shared encoder -> learned representations.
"""
import math, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit')))
from v7kit import *

H = 7.4
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figure09_V7.pptx')
# Colour keeps its survey meaning: MERIT's retrieval, augmentation and review form one Task-Specific Harness module
# (tsk red); the contrastive learner downstream is neutral ink. Teal / red tags and stamps are pass / fail status.
GT, TK, LL, NV = HUE['gts'], HUE['tsk'], HUE['llm'], HUE['ink']
P1, P2 = LL[0], INK           # marker colours of the tall (1) and the small (2) peak
BLOCK2 = 'E6EAF2'             # tint of the block holding peak 2


# ---- schematic signals ----------------------------------------------------------------------------------
def g(t, m, s):
    return math.exp(-0.5 * ((t - m) / s) ** 2)


def target(t):            # tall peak then a smaller peak (the peak order the review checks)
    return 0.12 + 0.78 * g(t, 0.30, 0.065) + 0.42 * g(t, 0.70, 0.075) + 0.025 * math.sin(41 * t)


def jitter(t):
    return target(t) + 0.035 * math.sin(173 * t + 0.4) + 0.025 * math.sin(311 * t + 1.3) + 0.02 * math.sin(89 * t)


def neighbor(t):          # a retrieved neighbour with the same structure
    return 0.12 + 0.70 * g(t, 0.33, 0.075) + 0.48 * g(t, 0.68, 0.07) + 0.03 * math.sin(29 * t + 1)


def permuted(t):          # the two halves swapped
    return target((t + 0.5) % 1.0)


def sig(sh, x, y, w, h, f, color=INK, lw=1.7, n=120):
    pts = [(x + w * k / n, y + h - h * f(k / n)) for k in range(n + 1)]
    poly(sh, pts, color, lw=lw)
    return lambda t: (x + w * t, y + h - h * f(t))


def peak(sh, at, num, col, base, d=0.26):
    """Numbered marker under the baseline at a peak's time position (reads as the peak order)."""
    px = at[0]
    arrow(sh, px, at[1] + 0.05, px, base + 0.03, color=col, lw=1.0, dash=MSO_LINE.ROUND_DOT, head=None)
    b = box(sh, px - d / 2, base + 0.03, d, d, fill=col, line='FFFFFF', lw=1.0, shape=MSO_SHAPE.OVAL)
    label_in(b, str(num), size=12)
    b.text_frame.margin_left = b.text_frame.margin_right = 0


def italic_runs(sh, x, y, w, h, parts, size, align='l'):
    """parts = [(text, colour, bold, italic)]"""
    tb = sh.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.02); tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
    for t, col, b, it in parts:
        r = p.add_run(); r.text = t; f = r.font
        f.size = Pt(size); f.bold = b; f.italic = it; f.name = F; f.color.rgb = rgb(col)
    return tb


def rpath(sh, pts, color, lw=2.4, dash=None, r=0.16, head=True):
    """Polyline with rounded corners and an arrowhead at the end."""
    out = [pts[0]]
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        def towards(p, q, d):
            L = math.hypot(q[0] - p[0], q[1] - p[1]); k = min(d, L / 2) / L
            return (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
        s, e = towards(b, a, r), towards(b, c, r)
        out += bezier([s, b, e], n=10)
    out.append(pts[-1])
    s = poly(sh, out, color, lw=lw, dash=dash)
    if head:
        e = etree.SubElement(s.line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle'); e.set('w', 'med'); e.set('len', 'med')
    return s


def caption(sh, cx, y, lines, color=MUTE, size=13, w=1.6):
    return tx(sh, cx - w / 2, y, w, 0.22 * (len(lines) if isinstance(lines, list) else 1) + 0.04, lines, size=size,
              bold=True, color=color)


# ---- zone 1: retrieval agent ----------------------------------------------------------------------------
def retrieval(slide):
    g_ = group(slide); sh = g_.shapes
    paper(sh, 0.42, 0.95, 2.86, 1.2, 'B9A98A')
    ic(sh, 'timeseries', 0.5, 0.99, 0.44)
    italic_runs(sh, 0.98, 1.0, 2.2, 0.36, [('Target Sequence ', INK, True, False), ('x', INK, True, True)], 15)
    at = sig(sh, 0.62, 1.38, 2.45, 0.48, target)
    base = at(0.0)[1] + 0.02
    peak(sh, at(0.30), 1, P1, base, 0.24); peak(sh, at(0.70), 2, P2, base, 0.24)
    # similarity shortlist -> LLM relevance review
    c1, c2, yi = 1.12, 2.62, 2.4
    arrow(sh, c1, 2.17, c1, yi - 0.02, color=TK[0], lw=2.2)
    ic(sh, 'memory', c1 - 0.3, yi, 0.6)
    caption(sh, c1, yi + 0.62, ['Similarity', 'Shortlist'], color=TK[0], w=1.2)
    arrow(sh, c1 + 0.38, yi + 0.3, c2 - 0.38, yi + 0.3, color=TK[0], lw=2.2)
    ic(sh, 'llm', c2 - 0.3, yi, 0.6)
    caption(sh, c2, yi + 0.62, ['LLM Relevance', 'Review'], color=TK[0], w=1.5)
    arrow(sh, c2, yi + 1.1, c2, 3.66, color=TK[0], lw=2.2)
    # reference set R
    card(sh, 0.55, 3.7, 2.75, 0.86, key='tsk')
    italic_runs(sh, 0.66, 3.73, 2.0, 0.32, [('Reference Set ', TK[0], True, False), ('R', TK[0], True, True)], 15)
    sig(sh, 0.7, 4.06, 1.85, 0.42, neighbor, color=TK[0])
    ic(sh, 'validate', 2.72, 3.97, 0.44)
    return g_


# ---- zone 2: augmentation agent -------------------------------------------------------------------------
def chip(sh, x, y, w, label, kind):
    b = box(sh, x, y, w, 0.44, fill='FFFFFF', line=TK[1], lw=1.2, radius=0.5)
    gx, gy, gw, gh = x + 0.13, y + 0.09, 0.34, 0.26
    if kind == 'jitter':
        pts = [(gx + gw * k / 10, gy + gh / 2 + (0.11 if k % 2 else -0.11) * (0.5 + 0.5 * math.sin(k))) for k in range(11)]
        poly(sh, pts, TK[0], lw=1.6)
    elif kind == 'mask':
        sig(sh, gx, gy, gw, gh, lambda t: 0.5 + 0.4 * math.sin(2 * math.pi * 1.6 * t), color=TK[0], lw=1.5, n=30)
        m = box(sh, gx + 0.13, gy - 0.02, 0.13, gh + 0.04, fill='8C93A3', shape=MSO_SHAPE.RECTANGLE); alpha_fill(m, 75)
    else:   # permutation: two blocks trading places
        box(sh, gx, gy + 0.03, 0.14, 0.2, fill=TK[1], line=TK[0], lw=1.0, shape=MSO_SHAPE.RECTANGLE)
        box(sh, gx + 0.2, gy + 0.03, 0.14, 0.2, fill=TK[2], line=TK[0], lw=1.0, shape=MSO_SHAPE.RECTANGLE)
        curve(sh, [(gx + 0.06, gy + 0.01), (gx + 0.17, gy - 0.12), (gx + 0.28, gy + 0.01)], TK[0], lw=1.1)
    tx(sh, x + 0.5, y, w - 0.55, 0.44, label, size=13.5, bold=True, color=TK[0], align='l')
    return b


def candidate(sh, y, letter, title, f, tag, ok, blocks=False):
    x0, w = 3.84, 5.0
    card(sh, x0, y, w, 1.2, key='tsk')
    sx, sy, sw, shh = x0 + 0.2, y + 0.44, 2.95, 0.44
    if blocks:   # shade the two swapped halves (behind the series)
        for k, fill in enumerate((BLOCK2, LL[2])):
            box(sh, sx + k * sw / 2, sy - 0.02, sw / 2, shh + 0.28, fill=fill, shape=MSO_SHAPE.RECTANGLE)
        arrow(sh, sx + sw / 2, sy - 0.04, sx + sw / 2, sy + shh + 0.28, color='8C93A3', lw=1.0, dash=MSO_LINE.DASH, head=None)
    b = box(sh, x0 + 0.12, y + 0.1, 0.34, 0.34, fill=TK[0], shape=MSO_SHAPE.OVAL); label_in(b, letter, size=14)
    tx(sh, x0 + 0.54, y + 0.08, 2.4, 0.38, title, size=15, bold=True, align='l')
    at = sig(sh, sx, sy, sw, shh, f)
    base = sy + shh * 0.9
    if blocks:
        peak(sh, at(0.20), 2, P2, base); peak(sh, at(0.80), 1, P1, base)
    else:
        peak(sh, at(0.30), 1, P1, base); peak(sh, at(0.70), 2, P2, base)
    col = GT[0] if ok else TK[0]
    t = box(sh, x0 + 3.33, y + 0.34, 1.52, 0.62, fill=GT[2] if ok else TK[2], line=GT[1] if ok else TK[1], lw=1.0, radius=0.3)
    label_in(t, tag, size=13, color=col)


def augmentation(slide):
    g_ = group(slide); sh = g_.shapes
    ic(sh, 'synthesis', 3.84, 0.86, 0.5)
    tx(sh, 4.42, 0.9, 3.4, 0.4, 'Transformation Selection', size=15, bold=True, align='l')
    for k, (lab, kind, w) in enumerate([('Jittering', 'jitter', 1.36), ('Time Masking', 'mask', 1.79), ('Permutation', 'perm', 1.63)]):
        x = [3.84, 5.29, 7.17][k]
        chip(sh, x, 1.42, w, lab, kind)
    candidate(sh, 2.04, 'A', 'Small Jitter', jitter, ['Peak Order', 'Retained'], True)
    candidate(sh, 3.38, 'B', 'Block Permutation', permuted, ['Peak Order', 'Changed'], False, blocks=True)
    return g_


# ---- zone 3: review agent -------------------------------------------------------------------------------
def stamp(sh, x, y, ok):
    col, lt, md = (GT[0], GT[2], GT[1]) if ok else (TK[0], TK[2], TK[1])
    b = box(sh, x, y, 1.5, 0.5, fill=lt, line=md, lw=1.3, radius=0.5); shadow(b)
    d = box(sh, x + 0.08, y + 0.08, 0.34, 0.34, fill=col, shape=MSO_SHAPE.OVAL)
    label_in(d, '✓' if ok else '✕', size=14)
    d.text_frame.margin_left = d.text_frame.margin_right = 0
    tx(sh, x + 0.46, y, 1.0, 0.5, '“Correct”' if ok else '“Error”', size=15, bold=True, color=col)


def review(slide):
    g_ = group(slide); sh = g_.shapes
    ic(sh, 'reason', 9.4, 1.0, 0.72)
    italic_runs(sh, 10.2, 1.04, 2.8, 0.34, [('Compare with ', TK[0], True, False), ('x', TK[0], True, True)], 15)
    tx(sh, 10.2, 1.4, 2.8, 0.3, 'Judgment + Rationale', size=13.5, bold=True, color=MUTE, align='l')
    for y, ok, icon, cap in [(2.68, True, 'memory', ['Retain in', 'Memory M']), (4.02, False, 'feedback', ['Refine', 'Retrieval'])]:
        arrow(sh, 8.88, y, 9.3, y, color=TK[0], lw=2.4)
        stamp(sh, 9.34, y - 0.25, ok)
        arrow(sh, 10.88, y, 11.2, y, color=TK[0], lw=2.4, dash=None if ok else MSO_LINE.DASH)
        ic(sh, icon, 11.24, y - 0.31, 0.62)
        t = tx(sh, 11.9, y - 0.24, 1.15, 0.48, cap, size=13, bold=True, color=TK[0], align='l')
        if ok:   # italic M
            r = t.text_frame.paragraphs[1].runs[0]; r.text = 'Memory '
            r2 = t.text_frame.paragraphs[1].add_run(); r2.text = 'M'
            f = r2.font; f.size = Pt(13); f.bold = True; f.italic = True; f.name = F; f.color.rgb = rgb(TK[0])
    return g_


def reject_loop(slide):
    g_ = group(slide); sh = g_.shapes
    yb = 4.98
    rpath(sh, [(11.55, 4.36), (11.55, yb), (0.33, yb), (0.33, 2.7), (0.8, 2.7)], TK[0], lw=2.4,
          dash=MSO_LINE.DASH, r=0.2)
    b = box(sh, 1.0, yb - 0.17, 3.1, 0.34, fill='FFFFFF', line=TK[1], lw=1.0, radius=0.5)
    label_in(b, 'Rejection Restarts Retrieval', size=13.5, color=TK[0], italic=True)
    # R informs the transformation choice
    rpath(sh, [(3.31, 4.06), (3.575, 4.06), (3.575, 1.12), (3.84, 1.12)], TK[0], lw=2.4, r=0.16)
    return g_


# ---- lower band: contrastive learning -------------------------------------------------------------------
def learning(slide):
    g_ = group(slide); sh = g_.shapes
    y0, cy = 6.0, 6.4
    items = [('x', INK, target, 'B8C0D0'), ('M', TK[0], jitter, TK[1]), ('R', TK[0], neighbor, TK[1])]
    for (lab, col, f, line), x in zip(items, [0.6, 2.02, 3.46]):
        paper(sh, x, y0, 0.98, 0.78, line=line, n=2)
        italic_runs(sh, x + 0.06, y0 + 0.02, 0.4, 0.3, [(lab, col, True, True)], 15)
        sig(sh, x + 0.1, y0 + 0.3, 0.8, 0.4, f, color=col, lw=1.4)
    tx(sh, 1.64, y0 + 0.19, 0.4, 0.4, '+', size=20, bold=True, color=INK)
    ux, uy = 3.255, y0 + 0.27   # union sign drawn as a native stroke
    poly(sh, [(ux - 0.1, uy)] + [(ux + 0.1 * math.cos(math.pi * (1 - k / 16)), uy + 0.13 + 0.1 * math.sin(math.pi * k / 16))
                                for k in range(17)] + [(ux + 0.1, uy)], INK, lw=2.4)
    caption(sh, 2.53, y0 + 0.86, 'Positive Samples', color=INK, size=14, w=2.6)
    arrow(sh, 4.6, cy, 5.02, cy, color=INK, lw=2.6)
    # shared encoder: a narrowing block
    ex, ew = 5.08, 2.0
    shadow(poly(sh, [(ex, cy - 0.5), (ex + ew, cy - 0.3), (ex + ew, cy + 0.3), (ex, cy + 0.5)], INK, lw=1.4,
                fill='E3E8F1', closed=True))
    tx(sh, ex, cy - 0.33, ew, 0.66, ['Shared', 'Encoder'], size=15, bold=True, color=INK)
    arrow(sh, ex + ew + 0.08, cy, ex + ew + 0.58, cy, color=INK, lw=2.6)
    # representation space: each positive pair is pulled together
    rx, ry, rw, rh = 7.75, 5.9, 2.05, 1.0
    card(sh, rx, ry, rw, rh, key='ink')
    for (fx, fy), col in [((0.3, 0.27), LL[0]), ((0.68, 0.52), INK), ((0.33, 0.77), '8C93A3')]:
        px, py, half = rx + rw * fx, ry + rh * fy, 0.3
        for sgn in (-1, 1):
            box(sh, px + sgn * half - 0.085, py - 0.085, 0.17, 0.17, fill=col, shape=MSO_SHAPE.OVAL)
            arrow(sh, px + sgn * (half - 0.11), py, px + sgn * 0.04, py, color=col, lw=1.8)
    tx(sh, 10.05, 6.0, 3.0, 0.4, 'Learn Representations', size=16, bold=True, color=INK, align='l')
    tx(sh, 10.05, 6.43, 3.0, 0.34, 'Bring Positive Pairs Together', size=13.5, bold=True, color=MUTE, align='l')
    return g_


def stage_zone(slide, x, w, num, title, text_w, y=0.42, h=4.27):
    """Task-Specific Harness zone with a numbered banner (same pattern as Figure 10)."""
    g_ = zone(slide, x, y, w, h, None, 'tsk'); sh = g_.shapes
    bw = text_w + 0.6
    b = box(sh, x + w / 2 - bw / 2, y - 0.25, bw, 0.5, fill=TK[0], radius=0.5); shadow(b)
    runs(b, [(num + '  ', TK[1], True, False), (title, 'FFFFFF', True, False)], 19)
    return g_


def build(out=OUT):
    p, slide = new_slide(H)
    stage_zone(slide, 0.2, 3.27, '1', 'Retrieval Agent', 2.38)
    stage_zone(slide, 3.65, 5.38, '2', 'Augmentation Agent', 2.95)
    stage_zone(slide, 9.18, 3.95, '3', 'Review Agent', 2.09)
    zone(slide, 0.2, 5.5, 12.93, 1.72, 'Contrastive Learning', 'ink', bw=3.3)
    retrieval(slide)
    augmentation(slide)
    review(slide)
    learning(slide)
    reject_loop(slide)
    save(p, out)
    return out


if __name__ == '__main__':
    print(build(sys.argv[1] if len(sys.argv) > 1 else OUT))
