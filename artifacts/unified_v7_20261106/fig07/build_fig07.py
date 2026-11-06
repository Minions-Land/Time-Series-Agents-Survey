"""Figure 7 (fig:temporal-harness-functions), V7 house style.

A temporal workspace connecting sources, operations, and the LLM:
  top    - Information Release: sources placed on an availability-time axis, split at the decision cutoff tau
  middle - Shared Temporal Workspace: the four General Time Series Harness functions (Section 5 headings)
  bottom - the LLM sends requests to every function and receives observations back.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit')))
from v7kit import *
from PIL import ImageFont

H = 7.65
MATH = 'Times New Roman'
GT, GTm, GTl = HUE['gts']
TK = HUE['tsk'][0]
AM = HUE['llm'][0]
SD, SDm, SDl = HUE['data']
FONTS = {False: '/System/Library/Fonts/Supplemental/Comic Sans MS.ttf',
         True: '/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf'}
WARN = []


def width(t, size, bold):
    return ImageFont.truetype(FONTS[bold], int(size * 20)).getlength(t) / (20 * 72)


def T(sh, x, y, w, h, t, size=13, bold=True, color=INK, align='c', anchor='m', italic=False):
    """kit text box + a width check against the box (all boxes are non-wrapping)."""
    assert size >= 11.5, (t, size)
    for ln in (t if isinstance(t, list) else [t]):
        if width(ln, size, bold) > w - 0.04: WARN.append(f'overflow {ln!r} {width(ln, size, bold):.2f} > {w:.2f}')
    return tx(sh, x, y, w, h, t, size=size, bold=bold, color=color, align=align, anchor=anchor, italic=italic)


def R(sh, x, y, w, h, parts, size, align='c'):
    """Styled runs: parts = [(text, colour, bold, sub, italic)]."""
    tb = sh.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
    for t, col, b, sub, it in parts:
        r = p.add_run(); r.text = t; f = r.font; f.size = Pt(size); f.bold = b; f.italic = it
        f.name = MATH if it else F          # italic runs are math symbols (v, tau, t, x, u)
        if it: f.size = Pt(size * 1.15); f.bold = False
        f.color.rgb = rgb(col)
        if sub: r.font._rPr.set('baseline', '-25000')
    return tb


def dot(sh, cx, cy, r, fill, line=None):
    return box(sh, cx - r, cy - r, 2 * r, 2 * r, fill=fill, line=line, lw=1.0, shape=MSO_SHAPE.OVAL)


def pline(sh, x, y, w, h, vals, color=INK, lw=1.6, dots=True, r=0.035, dash=None):
    """Polyline through normalised values (0 bottom .. 1 top) with optional point markers."""
    n = len(vals) - 1
    pts = [(x + w * k / n, y + h * (1 - v)) for k, v in enumerate(vals)]
    poly(sh, pts, color, lw=lw, dash=dash)
    if dots:
        for px, py in pts: dot(sh, px, py, r, color)
    return pts


def sheet(sh, x, y, w, h, line='B9A98A', lines=3):
    """A single document sheet with text lines."""
    s = box(sh, x, y, w, h, fill='FFFFFF', line=line, lw=1.3, shape=MSO_SHAPE.RECTANGLE); shadow(s)
    for k in range(lines):
        arrow(sh, x + 0.07, y + 0.12 + k * (h - 0.2) / max(lines - 1, 1), x + w - 0.07 - (0.06 if k == lines - 1 else 0),
              y + 0.12 + k * (h - 0.2) / max(lines - 1, 1), color=line, lw=1.2, head=None)
    return s


# ---------------------------------------------------------------- top: information release on an availability axis
AX_Y, AX0, AX1, TAU = 2.0, 0.5, 12.85, 9.3


def release(slide):
    zone(slide, 0.2, 0.42, 12.93, 2.0, 'Information Release', 'data')
    g = group(slide); sh = g.shapes
    # availability bands either side of the cutoff
    b = box(sh, AX0, AX_Y - 0.075, TAU - AX0, 0.15, fill=GT, shape=MSO_SHAPE.RECTANGLE); alpha_fill(b, 22)
    b = box(sh, TAU, AX_Y - 0.075, AX1 - 0.15 - TAU, 0.15, fill=TK, shape=MSO_SHAPE.RECTANGLE); alpha_fill(b, 20)
    arrow(sh, AX0, AX_Y, AX1, AX_Y, color=INK, lw=2.4)
    for k in range(int((AX1 - AX0 - 0.3) / 0.35) + 1):          # time ruler ticks
        xk = AX0 + 0.1 + k * 0.35
        arrow(sh, xk, AX_Y - 0.05, xk, AX_Y + 0.05, color=INK, lw=1.0, head=None)
    # observed series
    ic(sh, 'timeseries', 0.42, 0.72, 0.56)
    T(sh, 1.02, 0.76, 2.2, 0.42, 'Observed Series', size=15, align='l')
    vals = [0.35, 0.6, 0.45, 0.75, 0.5, 0.62, 0.4, 0.85, 0.6, 0.7, 0.45, 0.65]
    pline(sh, 0.62, 1.3, 2.55, 0.42, vals, INK, lw=1.6)
    v1 = 3.75
    curve(sh, [(3.25, 1.48), (3.6, 1.5), (v1 - 0.02, AX_Y - 0.1)], SD, lw=2.2)
    dot(sh, v1, AX_Y, 0.075, INK, 'FFFFFF')
    # known calendar with a future event, published before tau
    ic(sh, 'calendar', 4.3, 0.72, 0.56)
    T(sh, 4.9, 0.76, 2.2, 0.42, 'Known Calendar', size=15, align='l')
    p = box(sh, 4.5, 1.33, 1.75, 0.38, fill=SDl, line=SDm, lw=1.2, radius=0.5); shadow(p)
    label_in(p, 'Future Event', size=13.5, color=INK)
    v2 = 7.65
    curve(sh, [(6.3, 1.52), (7.3, 1.45), (v2 - 0.02, AX_Y - 0.1)], SD, lw=2.2)
    T(sh, 6.55, 1.08, 1.3, 0.3, 'Published', size=13, bold=True, italic=True, color=SD)
    dot(sh, v2, AX_Y, 0.075, INK, 'FFFFFF')
    # decision cutoff tau
    arrow(sh, TAU, 0.95, TAU, AX_Y + 0.3, color=INK, lw=1.8, dash=MSO_LINE.DASH, head=None)
    p = box(sh, TAU - 1.0, 0.64, 2.0, 0.36, fill=INK, radius=0.5); shadow(p)
    pt = R(sh, TAU - 1.0, 0.64, 2.0, 0.36, [('Decision Cutoff ', 'FFFFFF', True, False, False),
                                             ('τ', 'FFFFFF', True, False, True)], 14)
    # late report, released after tau
    ic(sh, 'late_report', 10.3, 0.7, 0.62)
    T(sh, 10.96, 0.76, 1.9, 0.42, 'Late Report', size=15, align='l')
    v3 = 11.45
    curve(sh, [(10.75, 1.38), (10.9, 1.75), (v3 - 0.08, AX_Y - 0.09)], SD, lw=2.2)
    dot(sh, v3, AX_Y, 0.075, TK, 'FFFFFF')
    # axis labels
    T(sh, TAU - 1.6, AX_Y + 0.1, 1.5, 0.28, 'Available', size=13.5, italic=True, color=GT, align='r')
    T(sh, TAU + 0.1, AX_Y + 0.1, 1.0, 0.28, 'Late', size=13.5, italic=True, color=TK, align='l')
    R(sh, AX1 - 2.2, AX_Y + 0.1, 2.2, 0.28, [('Availability Time ', MUTE, True, False, False),
                                             ('v', MUTE, True, False, True)], 13.5, align='r')
    return g


# ---------------------------------------------------------------- middle: the four shared functions
CW, CH, CY, GAP = 2.98, 2.85, 3.28, 0.2
X = [0.42 + k * (CW + GAP) for k in range(4)]


def fcard(slide, k, icon, title):
    g = group(slide); sh = g.shapes
    x = X[k]
    card(sh, x, CY, CW, CH, key='gts', lw=1.4)
    ic(sh, icon, x + 0.12, CY + 0.1, 0.62)
    T(sh, x + 0.82, CY + 0.07, CW - 0.86, 0.64, title, size=15, color=GT, align='l')
    arrow(sh, x + 0.15, CY + 0.8, x + CW - 0.15, CY + 0.8, color=GTm, lw=1.0, dash=MSO_LINE.ROUND_DOT, head=None)
    return g, sh, x


def data_card(slide):
    g, sh, x = fcard(slide, 0, 'data', ['Temporal Data', 'Management'])
    x0, y0, cw, rh = x + 0.2, CY + 0.92, 0.86, 0.28
    rows = [[('Time', 0), ('Value', 0), ('Unit', 0)],
            [('t', '1'), ('x', '1'), ('u', None)], [('t', '2'), ('—', None), ('u', None)], [('t', '3'), ('x', '3'), ('u', None)]]
    for r, row in enumerate(rows):
        for c, (t, sub) in enumerate(row):
            cell = box(sh, x0 + c * cw, y0 + r * rh, cw, rh, fill=GTl if r == 0 else 'FFFFFF', line=GTm, lw=0.9,
                       shape=MSO_SHAPE.RECTANGLE)
            if r == 0:
                R(sh, x0 + c * cw, y0, cw, rh, [(t, GT, True, False, False)], 13)
            else:
                parts = [(t, MUTE if t == '—' else INK, False, False, t in 'txu')]
                if sub: parts.append((sub, INK, False, True, False))
                R(sh, x0 + c * cw, y0 + r * rh, cw, rh, parts, 13.5)
    yb = CY + 2.27
    cylinder(sh, x + 0.28, yb - 0.04, 0.4, 0.46, key='gts')
    T(sh, x + 0.72, yb, 0.8, 0.36, 'Source', size=13, align='l')
    for k in (2, 1, 0):
        s = box(sh, x + 1.52 + 0.06 * k, yb + 0.04 - 0.06 * k, 0.32, 0.38, fill='FFFFFF', line=GTm if k else GT, lw=1.1,
                shape=MSO_SHAPE.RECTANGLE)
        if k == 2: shadow(s)
        if k == 0:
            for j in range(3):
                arrow(sh, x + 1.58, yb + 0.14 + j * 0.09, x + 1.78 - (0.05 if j == 2 else 0), yb + 0.14 + j * 0.09, color=GTm, lw=1.0, head=None)
    T(sh, x + 2.04, yb, 0.9, 0.36, 'Version', size=13, align='l')
    return g


def processing_card(slide):
    g, sh, x = fcard(slide, 1, 'window', ['Temporal', 'Processing'])
    gx, gw = x + 1.12, 1.72
    for i, lab in enumerate(['Window', 'Resample', 'Align']):
        ry = CY + 0.93 + i * 0.63
        T(sh, x + 0.12, ry, 1.0, 0.46, lab, size=13, align='l')
        gy, gh = ry + 0.04, 0.4
        if lab == 'Window':
            wx0, wx1 = gx + 0.42 * gw, gx + 0.75 * gw
            b = box(sh, wx0, gy - 0.04, wx1 - wx0, gh + 0.08, fill=GTm, shape=MSO_SHAPE.RECTANGLE); alpha_fill(b, 40)
            for xx in (wx0, wx1):
                arrow(sh, xx, gy - 0.06, xx, gy + gh + 0.06, color=GT, lw=1.2, dash=MSO_LINE.DASH, head=None)
            pline(sh, gx, gy, gw, gh, [0.4, 0.55, 0.3, 0.5, 0.75, 0.45, 0.65, 0.8, 0.6, 0.35, 0.55, 0.45], INK, lw=1.4, r=0.03)
        elif lab == 'Resample':
            pline(sh, gx, gy, 0.66, gh, [0.3, 0.55, 0.8, 0.4], INK, lw=1.4, r=0.03)
            arrow(sh, gx + 0.74, gy + gh / 2, gx + 1.0, gy + gh / 2, color=GT, lw=1.8)
            pline(sh, gx + 1.06, gy, 0.66, gh, [0.3, 0.42, 0.55, 0.7, 0.8, 0.6, 0.4, 0.45], INK, lw=1.4, r=0.026)
        else:
            a = pline(sh, gx, gy - 0.02, gw, 0.17, [0.2, 0.7, 0.4, 0.9, 0.5, 0.6, 0.3, 0.8, 0.45], INK, lw=1.4, r=0.028)
            b2 = pline(sh, gx, gy + 0.25, gw, 0.17, [0.5, 0.2, 0.7, 0.4, 0.9, 0.5, 0.6, 0.3, 0.6], GT, lw=1.4, r=0.028)
            for k in range(0, 9, 2):
                arrow(sh, a[k][0], a[k][1] + 0.04, b2[k][0], b2[k][1] - 0.04, color=MUTE, lw=0.9,
                      dash=MSO_LINE.ROUND_DOT, head=None)
    return g


def context_card(slide):
    g, sh, x = fcard(slide, 2, 'timeline', ['Temporal Context', 'and Memory'])
    # events aligned to the series
    vals = [0.3, 0.5, 0.35, 0.55, 0.4, 0.2, 0.5, 0.8, 0.45, 0.55, 0.35, 0.6]
    pts = pline(sh, x + 0.2, CY + 1.28, 2.58, 0.36, vals, INK, lw=1.4, r=0.03)
    for i, lab in ((3, 'Event A'), (8, 'Event B')):
        px, py = pts[i]
        arrow(sh, px, CY + 1.17, px, py - 0.05, color=GT, lw=1.3, dash=MSO_LINE.DASH, head=None)
        dot(sh, px, CY + 1.13, 0.06, 'FFFFFF', GT)
        T(sh, px - 0.6, CY + 0.84, 1.2, 0.26, lab, size=12.5, color=GT)
    # a retrieved past case matched to the current window
    T(sh, x + 0.12, CY + 1.8, 1.2, 0.28, 'Past Case', size=13, align='l')
    hx0, hx1 = x + 1.42, x + 2.2
    b = box(sh, hx0, CY + 1.84, hx1 - hx0, 0.9, fill=GTm, line=GT, lw=1.1, dash=MSO_LINE.DASH, shape=MSO_SHAPE.RECTANGLE)
    alpha_fill(b, 35)
    pline(sh, x + 0.2, CY + 1.98, 2.58, 0.22, [0.5, 0.3, 0.6, 0.4, 0.7, 0.3, 0.1, 0.4, 0.8, 0.5, 0.6, 0.45], MUTE, lw=1.3, r=0.026)
    pline(sh, x + 0.2, CY + 2.44, 2.58, 0.22, [0.4, 0.6, 0.35, 0.65, 0.45, 0.35, 0.1, 0.45, 0.85, 0.4, 0.55, 0.5], INK, lw=1.4, r=0.026)
    arrow(sh, (hx0 + hx1) / 2 - 0.1, CY + 2.2, (hx0 + hx1) / 2 - 0.1, CY + 2.45, color=GT, lw=1.8)
    return g


def validation_card(slide):
    g, sh, x = fcard(slide, 3, 'cutoff', ['Temporal', 'Validation'])
    R(sh, x, CY + 0.86, CW, 0.38, [('v', INK, True, False, True), (' ≤ ', INK, True, False, False),
                                   ('τ', INK, True, False, True)], 18)
    for i, (lab, res, cap, col) in enumerate([('Available', 'validate', 'Admit', GT), ('Late', 'reject', 'Exclude', TK)]):
        ry = CY + 1.35 + i * 0.75
        sheet(sh, x + 0.55, ry, 0.36, 0.42, line=col)
        T(sh, x + 0.13, ry + 0.43, 1.2, 0.25, lab, size=12.5, color=col)
        arrow(sh, x + 1.05, ry + 0.21, x + 1.85, ry + 0.21, color=col, lw=2.2)
        ic(sh, res, x + 2.0, ry - 0.02, 0.46)
        T(sh, x + 1.73, ry + 0.43, 1.0, 0.25, cap, size=12.5, color=col)
    return g


def workspace(slide):
    zone(slide, 0.2, 2.9, 12.93, 3.41, 'Shared Temporal Workspace', 'gts')
    data_card(slide); processing_card(slide); context_card(slide); validation_card(slide)
    g = group(slide)   # released sources enter the workspace through data management
    arrow(g.shapes, X[0] + CW - 0.45, AX_Y + 0.12, X[0] + CW - 0.45, CY - 0.04, color=SD, lw=3.0)


# ---------------------------------------------------------------- bottom: LLM requests and observations
YR, YO = 6.68, 7.1


def llm(slide):
    g = group(slide); sh = g.shapes
    halo(sh, 0.95, 6.86, 1.3, 1.1)
    pedestal(sh, 0.38, 7.2, 1.14, 0.28, 'llm')
    ic(sh, 'robot', 0.5, 6.38, 0.92)
    p = box(sh, 0.12, 6.42, 0.62, 0.34, fill=AM, radius=0.5); shadow(p)
    label_in(p, 'LLM', size=14)
    xs = [x + CW / 2 for x in X]
    x_start = 1.5
    arrow(sh, x_start, YR, xs[-1] - 0.18, YR, color=AM, lw=2.6, head=None)
    poly(sh, [(xs[-1] + 0.18, YO), (x_start, YO)], INK, lw=2.0, dash=MSO_LINE.DASH)
    e = etree.SubElement(sh[-1].line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle'); e.set('w', 'med'); e.set('len', 'med')
    for xc in xs:
        arrow(sh, xc - 0.18, YR, xc - 0.18, CY + CH + 0.04, color=AM, lw=2.6)
        arrow(sh, xc + 0.18, CY + CH + 0.04, xc + 0.18, YO, color=INK, lw=2.0, dash=MSO_LINE.DASH, head=None)
    lx = (xs[0] + xs[1]) / 2
    T(sh, lx - 1.0, YR - 0.33, 2.0, 0.3, 'Requests', size=14, italic=True, color=AM)
    T(sh, lx - 1.0, YO + 0.04, 2.0, 0.3, 'Observations', size=14, italic=True, color=INK)
    return g


def build(out):
    p, slide = new_slide(H)
    release(slide)
    workspace(slide)
    llm(slide)
    save(p, out)
    for w in WARN: print('WARN', w)


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figure07_V7.pptx'))
