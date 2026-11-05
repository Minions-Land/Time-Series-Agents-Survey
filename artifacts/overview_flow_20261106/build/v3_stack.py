"""V3 Dark Architecture Stack: five stacked layers with a feedback rail, tech-poster look."""
from common import *
from v2_clay import polyline
from pptx.enum.dml import MSO_LINE

ST, F, M = 'clay', 'Avenir Next', 'Menlo'
BG, PANEL, EDGE, TXT, SUB = '0F172A', '1E293B', '334155', 'F1F5F9', '94A3B8'
NEON = dict(llm='FBBF24', gh='60A5FA', gts='2DD4BF', tsk='F87171', ev='A78BFA')


def layer(slide, st, x, y, w, h):
    g = group(slide); sh = g.shapes; col = NEON[st['key']]
    box(sh, x, y, w, h, fill=PANEL, line=EDGE, lw=1, radius=0.12)
    box(sh, x, y + 0.08, 0.09, h - 0.16, fill=col, radius=0.5)
    icon(sh, ST, st['icon'], x + 0.2, y + (h - 0.66) / 2, 0.66)
    text(sh, x + 0.95, y + 0.08, 2.6, 0.3, f"{st['name']}", size=11, bold=True, color=col, font=F, align='l')
    text(sh, x + 0.95, y + 0.36, 2.6, 0.18, st['sec'] + '  ·  ' + st['short'], size=7.5, color=SUB, font=M, align='l')
    text(sh, x + 0.95, y + 0.52, 2.3, 0.3, st['role'], size=7.4, italic=True, color=TXT, font=F, align='l', anchor='t')
    # module chips
    cx0, cy, gap = x + 3.3, y + 0.14, 0.07
    cx = cx0
    for it in st['items']:
        cw = 0.1 + 0.05 * len(it)
        if cx + cw > x + w - 1.55:
            cx = cx0; cy += 0.3
        c = box(sh, cx, cy, cw, 0.24, fill=BG, line=col, lw=1, radius=0.5)
        label_in(c, it, size=6.8, bold=False, color=TXT, font=F)
        cx += cw + gap
    # representative works (logo + name) at right edge
    for k, (name, lg) in enumerate(st['works'][:4]):
        wy = y + 0.07 + k * 0.17
        if lg:
            pl = box(sh, x + w - 1.47, wy, 0.15, 0.15, fill='FFFFFF', radius=0.2)
            logo(sh, lg, x + w - 1.46, wy + 0.01, 0.13)
        text(sh, x + w - 1.27, wy - 0.01, 1.25, 0.17, name, size=6.6, color=SUB, font=F, align='l')
    return g


def build(out):
    p, slide = new_pres()
    box(slide.shapes, 0, 0, 13.333, 6.4, fill=BG, shape=MSO_SHAPE.RECTANGLE)
    # faint grid
    gg = group(slide)
    for k in range(1, 27):
        arrow(gg.shapes, k * 0.5, 0, k * 0.5, 6.4, color='17213A', lw=0.5, head=None)
    for k in range(1, 13):
        arrow(gg.shapes, 0, k * 0.5, 13.333, k * 0.5, color='17213A', lw=0.5, head=None)
    text(slide.shapes, 0.3, 0.12, 9, 0.42, TITLE, size=19, bold=True, color=TXT, font=F, align='l')
    text(slide.shapes, 0.3, 0.52, 9, 0.24, '> layers ordered from general to specific; validation feeds back to the LLM', size=8.5, color=NEON['gts'], font=M, align='l')
    x, w, h, gap, y0 = 2.25, 8.55, 0.86, 0.22, 0.98
    ys = [y0 + k * (h + gap) for k in range(5)]
    for st, y in zip(STAGES, ys):
        layer(slide, st, x, y, w, h)
    fg = group(slide); fs = fg.shapes
    # input card
    ic = box(fs, 0.25, 0.98, 1.75, 0.86, fill=PANEL, line=EDGE, lw=1, radius=0.12)
    icon(fs, ST, INPUT['icon'], 0.3, 1.08, 0.66)
    text(fs, 0.98, 1.06, 1.0, 0.45, INPUT['name'], size=8, bold=True, color=TXT, font=F)
    text(fs, 0.98, 1.48, 1.0, 0.34, INPUT['sub'], size=6.2, color=SUB, font=F)
    arrow(fs, 2.0, ys[0] + h / 2, x, ys[0] + h / 2, color=TXT, lw=2)
    # inter-layer flows
    mx = x + 0.53
    arrow(fs, mx - 0.25, ys[0] + h, mx - 0.25, ys[1], color=NEON['llm'], lw=2)
    text(fs, mx - 1.3, ys[0] + h, 1.0, 0.2, FLOW['act'], size=7, color=NEON['llm'], font=M, align='r')
    arrow(fs, mx + 0.25, ys[1], mx + 0.25, ys[0] + h, color=NEON['gh'], lw=1.5, dash=MSO_LINE.DASH)
    text(fs, mx + 0.32, ys[0] + h, 1.2, 0.2, FLOW['obs'], size=7, color=NEON['gh'], font=M, align='l')
    for k, lab in [(1, FLOW['ops']), (2, FLOW['cap']), (3, FLOW['cand'])]:
        arrow(fs, mx, ys[k] + h, mx, ys[k + 1], color=NEON[STAGES[k]['key']], lw=2)
        text(fs, mx + 0.1, ys[k] + h, 2.4, 0.2, lab, size=7, color=NEON[STAGES[k]['key']], font=M, align='l')
    # feedback rail
    rx = x + w + 0.35
    polyline(fs, [(x + w, ys[4] + h / 2), (rx, ys[4] + h / 2), (rx, ys[0] + h / 2), (x + w, ys[0] + h / 2)], NEON['ev'], lw=3)
    rl = text(fs, rx - 1.3, 3.2, 2.6, 0.3, FLOW['fb'] + ' / terminate', size=8, bold=True, color=NEON['ev'], font=M)
    rl.rotation = 270
    # output
    oc = box(fs, 11.65, 4.35, 1.45, 1.9, fill=PANEL, line=NEON['ev'], lw=1.2, radius=0.12)
    icon(fs, ST, OUTPUT['icon'], 11.95, 4.42, 0.85)
    text(fs, 11.7, 5.3, 1.35, 0.5, OUTPUT['name'], size=8, bold=True, color=TXT, font=F)
    text(fs, 11.7, 5.82, 1.35, 0.3, OUTPUT['sub'], size=7, color=SUB, font=F)
    arrow(fs, rx, ys[4] + h / 2, 11.65, ys[4] + h / 2, color=NEON['ev'], lw=2)
    text(fs, 11.25, ys[4] + h / 2 - 0.27, 1.2, 0.2, 'accept', size=7, color=NEON['ev'], font=M, align='l')
    # agent badge top-right
    icon(fs, ST, 'robot', 11.75, 0.95, 1.25)
    text(fs, 11.45, 2.22, 1.85, 0.5, ['agent loop:', 'act · observe · check'], size=7.5, color=SUB, font=M)
    # reuse axis on the left
    arrow(fs, 1.1, ys[1] + 0.1, 1.1, ys[3] + h - 0.1, color=SUB, lw=1.5)
    for k, lab in [(1, 'general'), (2, 'temporal'), (3, 'task-specific')]:
        text(fs, 0.25, ys[k] + h / 2 - 0.12, 0.8, 0.24, lab, size=7.2, color=NEON[STAGES[k]['key']], font=M, align='r')
    text(fs, 0.2, ys[4] + 0.2, 1.8, 0.45, ['scope of reuse', 'narrows downward'], size=7, italic=True, color=SUB, font=F)
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
