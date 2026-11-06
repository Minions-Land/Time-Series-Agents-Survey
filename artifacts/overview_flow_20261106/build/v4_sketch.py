"""V4 Sketch Notebook: sticky notes on plain paper, hand-drawn outlines, cycle around the agent."""
import math
from common import *
from pptx.enum.dml import MSO_LINE

ST, F = 'clay', 'Comic Sans MS'
H = 7.45   # slide height: notes area + time-series band
NOTE = dict(llm='FFE8A3', gh='CFE0FF', gts='C9F0E4', tsk='FFD3CC', ev='E3DCFF')


def _smooth(t):
    return 0.5 * math.sin(2 * math.pi * t * 5.2) + 0.2 * math.sin(2 * math.pi * t * 17.3 + 1.1) + 0.4 * t


def _y(t):
    """Deterministic seasonal series with a trend; t in [0, 1]."""
    noise = 0.16 * math.sin(97.1 * t + 0.3) + 0.11 * math.sin(211.7 * t + 2.0) + 0.07 * math.sin(353.9 * t)
    return 0.5 * math.sin(2 * math.pi * t * 5.2) + 0.2 * math.sin(2 * math.pi * t * 17.3 + 1.1) + 0.4 * t + noise


def poly(sh, pts, color, lw=1.6, dash=None, fill=None, alpha=None, closed=False):
    ff = sh.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    ff.add_line_segments([(Inches(x), Inches(y)) for x, y in pts[1:]], close=closed)
    s = ff.convert_to_shape()
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
        if alpha is not None:
            clr = s.fill._xPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
            etree.SubElement(clr, qn('a:alpha')).set('val', str(int(alpha * 1000)))
    else:
        s.fill.background()
    if color:
        s.line.color.rgb = rgb(color); s.line.width = Pt(lw)
        if dash: s.line.dash_style = dash
    else:
        s.line.fill.background()
    return s


def sparkline(sh, x, y, w, h, color):
    n = 120
    pts = [(x + w * k / n, y + h / 2 - h / 2.4 * _y(k / n)) for k in range(n + 1)]
    poly(sh, pts, color, lw=1.5)


def fanline(sh, x, y, w, h):
    """Noisy observed history, then a smooth dashed forecast with a widening band."""
    n, cut = 120, 78
    py = lambda v: y + h / 2 - h / 2.4 * v
    hist = [(x + w * k / n, py(_y(k / n))) for k in range(cut + 1)]
    trend = lambda k: 0.5 * math.sin(2 * math.pi * k / n * 5.2) + 0.4 * k / n
    d = _y(cut / n) - trend(cut)
    fut = [(x + w * k / n, py(trend(k) + d)) for k in range(cut, n + 1)]
    m = n - cut
    up = [(px, q - 0.02 - 0.12 * i / m) for i, (px, q) in enumerate(fut)]
    lo = [(px, q + 0.02 + 0.12 * i / m) for i, (px, q) in enumerate(fut)]
    poly(sh, up + lo[::-1], None, fill=C['tsk'], alpha=25, closed=True)
    poly(sh, hist, '333333', lw=1.4)
    poly(sh, fut, C['tsk'], lw=1.4, dash=MSO_LINE.DASH)


GLYPHS = dict(   # icon row per note: (icon, one- or two-word caption); words kept to a minimum
    llm=[('llm', 'model'), ('encode', 'encode'), ('reason', 'reasoning'), ('policy', 'actions')],
    gh=[('chat', 'interaction'), ('memory', 'memory'), ('tools', 'tools'), ('planning', 'planning')],
    gts=[('calendar', 'timestamps'), ('window', 'windows'), ('cutoff', 'cutoff'), ('hourglass', 'chronology')],
    tsk=[('forecast', 'forecast'), ('synthesis', 'synthesis'), ('anomaly', 'anomaly'), ('decision', 'decision')],
    ev=[('process', 'process'), ('time_check', 'temporal'), ('benchmark', 'task score'), ('utility', 'utility')],
)
SHADOW = ('<a:outerShdw xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" blurRad="76200" dist="50800" '
          'dir="3600000" algn="tl" rotWithShape="0"><a:srgbClr val="3A3020"><a:alpha val="32000"/></a:srgbClr></a:outerShdw>')


def shadow(shape):
    sp = shape._element.spPr
    ef = sp.find(qn('a:effectLst'))
    if ef is None:
        ef = etree.SubElement(sp, qn('a:effectLst'))
    ef.append(etree.fromstring(SHADOW))
    return shape


def rich(sh, x, y, w, h, runs, size=10, align='r'):
    """One line of text with differently coloured runs: runs = [(text, colour, bold)]."""
    tb = sh.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    para = tf.paragraphs[0]
    para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
    for t, col, b in runs:
        r = para.add_run(); r.text = t
        f = r.font; f.size = Pt(size); f.bold = b; f.name = F; f.color.rgb = rgb(col)
    return tb


def rotate_group(g, deg):
    g._element.grpSpPr.get_or_add_xfrm().set('rot', str(int(deg * 60000)))


def time_band(slide):
    """History up to the information cutoff t0, then a forecast with widening uncertainty."""
    g = group(slide); sh = g.shapes
    x0, x1, t0, yc, amp = 0.55, 12.25, 9.35, 6.92, 0.2
    n = 220; kc = int(n * (t0 - x0) / (x1 - x0))
    xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    ys = [yc - amp * _y(k / n) for k in range(n + 1)]
    off = ys[kc] - (yc - amp * _smooth(kc / n))
    for k in range(kc + 1, n + 1):
        ys[k] = yc - amp * _smooth(k / n) + off
    ka = int(n * 0.3)                       # injected anomaly in the observed history
    ys[ka] -= 0.26
    box(sh, x0 - 0.1, 6.42, t0 - x0 + 0.1, 0.86, fill='EEF1F6', line=None, radius=0.15)
    text(sh, x0, 6.45, 1.0, 0.2, 'history', size=8, bold=True, color='555555', font=F, align='l')
    text(sh, t0 + 0.12, 6.45, 1.2, 0.2, 'forecast', size=8, bold=True, color=C['tsk'], font=F, align='l')
    up = [(xs[k], ys[k] - 0.03 - 0.2 * (k - kc) / (n - kc)) for k in range(kc, n + 1)]
    lo = [(xs[k], ys[k] + 0.03 + 0.2 * (k - kc) / (n - kc)) for k in range(kc, n + 1)]
    poly(sh, up + lo[::-1], None, fill=C['tsk'], alpha=22, closed=True)
    poly(sh, list(zip(xs[:kc + 1], ys[:kc + 1])), '2B2B2B', lw=1.8)
    poly(sh, list(zip(xs[kc:], ys[kc:])), C['tsk'], lw=1.8, dash=MSO_LINE.DASH)
    cut = arrow(sh, t0, 6.4, t0, 7.3, color=C['gts'], lw=2, head=None, dash=MSO_LINE.DASH); sketchy(cut)
    tl = box(sh, t0 - 0.22, 7.12, 0.44, 0.26, fill=C['gts'], radius=0.5)
    label_in(tl, 't', size=9.5, font=F)
    r0 = tl.text_frame.paragraphs[0].add_run(); r0.text = '0'
    r0.font.size = Pt(9.5); r0.font.bold = True; r0.font.name = F; r0.font.color.rgb = rgb('FFFFFF')
    r0.font._rPr.set('baseline', '-25000')
    an = box(sh, xs[ka] - 0.17, ys[ka] - 0.12, 0.34, 0.3, line=C['tsk'], lw=1.6, shape=MSO_SHAPE.OVAL); sketchy(an)
    icon(sh, ST, 'anomaly', xs[ka] + 0.2, ys[ka] - 0.2, 0.36)
    icon(sh, ST, 'decision', 12.38, 6.72, 0.46)
    arrow(sh, x1 + 0.02, ys[-1], 12.4, 6.95, color=C['ev'], lw=1.4)
    ax = arrow(sh, x0, 7.36, 12.95, 7.36, color='555555', lw=1.4); sketchy(ax)
    text(sh, 12.35, 7.16, 0.6, 0.2, 'time', size=7.6, italic=True, color='555555', font=F, align='r')
    return g


def note(slide, st, x, y, w, h, rot):
    g = group(slide); sh = g.shapes; k = st['key']
    n = box(sh, x, y, w, h, fill=NOTE[k], line='3A3A3A', lw=1.3, shape=MSO_SHAPE.RECTANGLE)
    sketchy(n); shadow(n)
    tape = box(sh, x + w / 2 - 0.38, y - 0.11, 0.76, 0.22, fill='F4F1E4', line='C9C4B0', lw=0.5, shape=MSO_SHAPE.RECTANGLE)
    tape.rotation = -4
    text(sh, x + 0.14, y + 0.12, w - 0.75, 0.34, st['name'], size=11.5 if len(st['name']) < 20 else 10.5, bold=True, color=C[k], font=F, align='l')
    stamp = box(sh, x + w - 0.62, y - 0.16, 0.86, 0.32, fill=C[k], line='3A3A3A', lw=1, radius=0.5)
    sketchy(stamp); stamp.rotation = 6
    label_in(stamp, st['verb'], size=8.5, font=F)
    row = GLYPHS[k]; m = len(row); cw = (w - 0.2) / m; isz = 0.56
    for i, (ic, cap) in enumerate(row):
        cx = x + 0.1 + i * cw
        icon(sh, ST, ic, cx + (cw - isz) / 2, y + 0.55, isz)
        text(sh, cx - 0.04, y + 1.15, cw + 0.08, 0.22, cap, size=7.2, color='333333', font=F)
    rotate_group(g, rot)
    return g


def hand_arrow(sh, x1, y1, x2, y2, color='333333', lw=2, label=None, lx=None, ly=None, curve=True, lwid=1.2):
    a = arrow(sh, x1, y1, x2, y2, color=color, lw=lw, curve=curve)
    sketchy(a)
    if label:
        text(sh, lx, ly, lwid, 0.24, label, size=8, bold=True, color=color, font=F)
    return a


def card(sh, x, y, w, h, rot):
    c = box(sh, x, y, w, h, fill='FFFFFF', line='3A3A3A', lw=1.2, shape=MSO_SHAPE.RECTANGLE)
    sketchy(c); shadow(c); c.rotation = rot
    t = box(sh, x + w / 2 - 0.34, y - 0.1, 0.68, 0.2, fill='F4F1E4', line='C9C4B0', lw=0.5, shape=MSO_SHAPE.RECTANGLE)
    t.rotation = rot + 3
    return c


def build(out):
    p, slide = new_pres(h=H)
    box(slide.shapes, 0, 0, 13.333, H, fill='FFFEF9', shape=MSO_SHAPE.RECTANGLE)
    tg = group(slide)
    hl = poly(tg.shapes, [(2.66, 0.3), (5.45, 0.27), (5.47, 0.51), (2.64, 0.54)], None, fill='FFD54F', alpha=55, closed=True)
    text(tg.shapes, 0.5, 0.1, 6, 0.5, TITLE, size=21, bold=True, color='2B2B2B', font=F, align='l')
    g_, m_ = '555555', ' what is '
    rich(tg.shapes, 6.0, 0.24, 6.85, 0.3, [('Reuse', C['gh'], True), (m_ + 'general  ·  ', g_, False),
                                           ('adapt', C['gts'], True), (m_ + 'temporal  ·  ', g_, False),
                                           ('rebuild', C['tsk'], True), (m_ + 'task-bound', g_, False)], size=11)
    w, h = 2.9, 1.5
    pos = dict(llm=(5.2, 0.85, -1), gh=(9.75, 1.2, 1.2), gts=(9.75, 3.75, -0.8), tsk=(5.2, 4.45, 0.8), ev=(0.75, 2.55, -1.2))
    for k, (x, y, r) in pos.items():
        note(slide, S[k], x, y, w, h, r)
    ag = group(slide); a = ag.shapes
    hand_arrow(a, 8.15, 1.35, 9.7, 1.65, color=C['llm'], label=FLOW['act'], lx=8.3, ly=1.05)
    hand_arrow(a, 9.7, 2.3, 8.15, 2.05, color=C['gh'], label=FLOW['obs'], lx=8.3, ly=2.25)
    hand_arrow(a, 11.2, 2.75, 11.2, 3.7, color=C['gh'], curve=False)
    hand_arrow(a, 9.7, 4.55, 8.15, 5.0, color=C['gts'])
    hand_arrow(a, 5.15, 5.25, 3.7, 4.0, color=C['tsk'])
    hand_arrow(a, 3.72, 3.05, 5.55, 2.42, color=C['ev'], lw=2.8, label='revise', lx=4.33, ly=3.2, lwid=0.55)
    icon(a, ST, 'feedback', 3.95, 3.12, 0.4)
    # centre agent thinking about a series
    box(slide.shapes, 5.95, 4.0, 1.6, 0.3, fill='E9E3D3', line=None, shape=MSO_SHAPE.OVAL)
    icon(slide.shapes, 'clay', 'robot', 5.85, 2.45, 1.75)
    bg = group(slide)
    bub = bg.shapes.add_shape(MSO_SHAPE.CLOUD_CALLOUT, Inches(7.6), Inches(2.5), Inches(1.95), Inches(1.05))
    bub.fill.solid(); bub.fill.fore_color.rgb = rgb('FFFFFF'); bub.line.color.rgb = rgb('333333'); bub.line.width = Pt(1.2)
    bub.adjustments[0], bub.adjustments[1] = -0.7, 0.45
    fanline(bg.shapes, 7.93, 2.86, 1.3, 0.3)
    # input / output index cards
    ig = group(slide); i = ig.shapes
    card(i, 0.6, 0.85, 2.4, 1.15, 2)
    icon(i, ST, 'timeseries', 0.72, 0.93, 0.62); icon(i, ST, 'request', 1.36, 0.93, 0.62)
    text(i, 2.0, 0.95, 0.95, 0.3, 'series + task', size=8.5, bold=True, color='2B2B2B', font=F, align='l')
    sparkline(i, 0.75, 1.6, 2.1, 0.28, C['gh'])
    hand_arrow(i, 3.05, 1.35, 5.15, 1.35, color='333333', curve=False)
    card(i, 0.6, 4.85, 2.4, 1.15, -2)
    icon(i, ST, 'validate', 0.72, 4.95, 0.55)
    text(i, 1.32, 5.0, 1.6, 0.3, 'accepted output', size=8.5, bold=True, color='2B2B2B', font=F, align='l')
    fanline(i, 0.8, 5.5, 2.0, 0.34)
    hand_arrow(i, 2.45, 4.12, 2.45, 4.8, color=C['ev'], curve=False)
    lead = arrow(slide.shapes, 9.85, 5.3, t0x := 9.38, 6.42, color=C['gts'], lw=1.2, dash=MSO_LINE.ROUND_DOT)
    time_band(slide)
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
