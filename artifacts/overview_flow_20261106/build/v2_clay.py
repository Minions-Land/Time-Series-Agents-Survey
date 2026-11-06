"""V2 Clay Pipeline: left-to-right card pipeline with 3D clay icons and a feedback return loop."""
from common import *
from pptx.enum.dml import MSO_LINE

ST, F = 'clay', 'Comic Sans MS'


def polyline(sh, pts, color, lw=2.5, dash=None, head=True):
    ff = sh.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    ff.add_line_segments([(Inches(x), Inches(y)) for x, y in pts[1:]], close=False)
    s = ff.convert_to_shape(); s.fill.background()
    s.line.color.rgb = rgb(color); s.line.width = Pt(lw)
    if dash: s.line.dash_style = dash
    if head:
        e = etree.SubElement(s.line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle')
    return s


def stage_card(slide, st, x, y, w, h):
    g = group(slide); sh = g.shapes
    box(sh, x, y, w, h, fill=C['white'], line=C[st['key']], lw=2.5, radius=0.1)
    pill = box(sh, x + 0.12, y + 0.1, w - 0.24, 0.42, fill=C[st['key']], radius=0.5)
    label_in(pill, st['name'], size=9.5 if len(st['name']) < 20 else 8.2, font=F)
    icon(sh, ST, st['icon'], x + w / 2 - 0.5, y + 0.58, 1.0)
    tag = box(sh, x + w / 2 - 0.5, y + 1.6, 1.0, 0.26, fill='FFFFFF', line=C[st['key']], lw=1.6, radius=0.5)
    label_in(tag, st['verb'], size=9, color=C[st['key']], font=F)
    text(sh, x + 0.1, y + 1.9, w - 0.2, 0.36, st['role'], size=7.6, italic=True, color=C['mute'], font=F)
    text(sh, x + 0.12, y + 2.3, w - 0.2, 0.8, ['• ' + i for i in st['items']], size=7.3, color=C['ink'], font=F, align='l', anchor='t')
    cl = box(sh, x + 0.1, y + h - 0.62, w - 0.2, 0.52, fill=C[st['key']], radius=0.25)
    label_in(cl, st['claim'], size=7.6, font=F)
    return g


def io_card(slide, d, x, y, w, h, color):
    g = group(slide); sh = g.shapes
    box(sh, x, y, w, h, fill='F7F5FF', line=color, lw=1.5, radius=0.15, dash=MSO_LINE.DASH)
    icon(sh, ST, d['icon'], x + w / 2 - 0.42, y + 0.15, 0.84)
    text(sh, x + 0.05, y + 1.05, w - 0.1, 0.5, d['name'], size=8.6, bold=True, color=C['ink'], font=F)
    text(sh, x + 0.05, y + 1.55, w - 0.1, 0.4, d['sub'], size=7, italic=True, color=C['mute'], font=F)
    return g


def build(out):
    p, slide = new_pres()
    box(slide.shapes, 0, 0, 13.333, 6.4, fill='F4F1FB', shape=MSO_SHAPE.RECTANGLE)
    text(slide.shapes, 0.3, 0.12, 12.7, 0.5, TITLE, size=20, bold=True, color=C['ink'], font=F)
    y, h, w, gap = 1.05, 3.75, 1.88, 0.2
    xs = [1.6 + k * (w + gap) for k in range(5)]
    io_card(slide, INPUT, 0.15, 1.75, 1.25, 2.0, C['ink'])
    for st, x in zip(STAGES, xs):
        stage_card(slide, st, x, y, w, h)
    io_card(slide, OUTPUT, 12.0, 1.75, 1.2, 2.0, C['ev'])
    fg = group(slide); fs = fg.shapes
    ay = 1.9
    arrow(fs, 1.4, 2.75, xs[0], 2.75, color=C['ink'], lw=2.2)
    # LLM <-> GH
    arrow(fs, xs[0] + w, ay - 0.12, xs[1], ay - 0.12, color=C['llm'], lw=2.2)
    arrow(fs, xs[1], ay + 0.18, xs[0] + w, ay + 0.18, color=C['gh'], lw=1.6, dash=MSO_LINE.DASH)
    for k, (a, col) in enumerate([(FLOW['ops'], C['gh']), (FLOW['cap'], C['gts']), (FLOW['cand'], C['tsk'])], start=1):
        arrow(fs, xs[k] + w, ay, xs[k + 1], ay, color=col, lw=2.2)
    arrow(fs, xs[4] + w, 2.75, 12.0, 2.75, color=C['ev'], lw=2.2)
    # feedback loop under the cards
    yb = 5.32
    polyline(fs, [(xs[4] + w / 2, y + h), (xs[4] + w / 2, yb), (xs[0] + w / 2, yb), (xs[0] + w / 2, y + h)], C['ev'], lw=3)
    fl = box(fs, 4.6, yb - 0.2, 4.1, 0.4, fill=C['ev'], radius=0.5)
    label_in(fl, '↺  feedback from validation: revise the plan, or terminate', size=8.6, font=F)
    # reuse axis above GH..TSK
    arrow(fs, xs[1] + 0.2, 0.85, xs[3] + w - 0.2, 0.85, color=C['mute'], lw=1.4)
    text(fs, xs[0], 0.6, xs[4] + w - xs[0], 0.22, MOTTO, size=8.4, bold=True, italic=True, color=C['gh'], font=F)
    # mascot
    icon(slide.shapes, ST, 'robot', 0.25, 4.45, 1.2)
    bub = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT, Inches(0.12), Inches(5.7), Inches(1.45), Inches(0.5))
    bub.fill.solid(); bub.fill.fore_color.rgb = rgb('FFFFFF'); bub.line.color.rgb = rgb(C['ink']); bub.line.width = Pt(1)
    bub.adjustments[0], bub.adjustments[1] = 0.15, -0.95
    label_in(bub, 'reuse, adapt, rebuild, verify', size=7, color=C['ink'], font=F, bold=False)
    text(slide.shapes, 5.6, 5.8, 7.6, 0.4, 'Key claim: ' + KEY, size=8.4, bold=True, color=C['ink'], font=F, align='r')
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
