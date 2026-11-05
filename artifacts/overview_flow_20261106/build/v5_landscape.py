"""V5 Logo Landscape: AI4AI-style side panels of logo tiles around a pixel-robot centre with the flow ribbon."""
from common import *
from v2_clay import polyline

ST, HF, F = 'pixel', 'Menlo', 'Avenir Next'
NAVY, GREEN, CREAM = '1B2A4A', '1F4D3A', 'FBF3E4'


def panel(slide, x, y, w, h, title, col):
    g = group(slide); sh = g.shapes
    box(sh, x, y, w, h, fill='FFFFFF', line=col, lw=2.2, radius=0.03)
    t = box(sh, x, y, w, 0.38, fill=col, radius=0.1)
    label_in(t, title, size=11, font=HF)
    return g


def section(slide, st, x, y, w, col):
    g = group(slide); sh = g.shapes
    bar = box(sh, x, y, w, 0.26, fill='FFFFFF', line=col, lw=1.2, radius=0.5)
    label_in(bar, f"{st['sec']}  {st['name'].upper()}", size=7.8, color=col, font=HF)
    text(sh, x, y + 0.27, w, 0.2, ' · '.join(st['items']), size=5.8, italic=True, color=C['mute'], font=F)
    tw, gap = (w - 0.08 * 3) / 4, 0.08
    for k, (name, lg) in enumerate(st['works'][:4]):
        tx = x + k * (tw + gap); ty = y + 0.5
        box(sh, tx, ty, tw, 0.66, fill='FFFFFF', line=C[st['key']], lw=1.2, radius=0.15)
        if lg:
            logo(sh, lg, tx + tw / 2 - 0.15, ty + 0.06, 0.3)
        else:
            m = box(sh, tx + tw / 2 - 0.15, ty + 0.06, 0.3, 0.3, fill=C[st['key']], shape=MSO_SHAPE.OVAL)
            label_in(m, name[0], size=9, font=HF)
        text(sh, tx + 0.02, ty + 0.4, tw - 0.04, 0.22, name, size=6 if len(name) > 12 else 6.6, bold=True, color=C['ink'], font=F)
    return g


def build(out):
    p, slide = new_pres()
    box(slide.shapes, 0, 0, 13.333, 6.4, fill='F6F4EF', shape=MSO_SHAPE.RECTANGLE)
    lx, cx0, rx, pw = 0.15, 4.3, 9.03, 4.15
    panel(slide, lx, 0.15, pw, 6.1, 'MODELS & EVALUATION', NAVY)
    section(slide, S['llm'], lx + 0.15, 0.68, pw - 0.3, NAVY)
    section(slide, S['ev'], lx + 0.15, 2.02, pw - 0.3, NAVY)
    # left: evaluation evidence ladder
    eg = group(slide); es = eg.shapes
    steps = ['process validity', 'temporal validity', 'task performance', 'decision utility']
    text(es, lx + 0.15, 3.42, pw - 0.3, 0.22, 'WHAT EVALUATION MUST SEPARATE', size=7.8, bold=True, color=NAVY, font=HF)
    for k, s in enumerate(steps):
        b = box(es, lx + 0.25 + k * 0.12, 3.72 + k * 0.42, pw - 0.6 - k * 0.24, 0.34, fill=['E8EEF9', 'E3F4F0', 'FBE7E3', 'EEEAFB'][k], line=C[['gh', 'gts', 'tsk', 'ev'][k]], lw=1, radius=0.4)
        label_in(b, f'{k + 1}  {s}', size=8, color=C['ink'], font=HF)
    text(es, lx + 0.15, 5.5, pw - 0.3, 0.6, 'Benchmarks expose the information, actions and output requirements the deployed workflow will meet (§7).', size=7, italic=True, color=C['mute'], font=F)
    # right panel
    panel(slide, rx, 0.15, pw, 6.1, 'HARNESS: GENERAL → SPECIFIC', GREEN)
    for k, key in enumerate(['gh', 'gts', 'tsk']):
        section(slide, S[key], rx + 0.15, 0.68 + k * 1.34, pw - 0.3, GREEN)
    hg = group(slide); hs = hg.shapes
    text(hs, rx + 0.15, 4.75, pw - 0.3, 0.22, 'EACH WORK MAY CONTRIBUTE TO SEVERAL LAYERS', size=7, bold=True, color=GREEN, font=HF)
    text(hs, rx + 0.15, 5.0, pw - 0.45, 1.1, ['Layer = scope implied by a module’s inputs, state and assumptions.', 'Modules are tested from the most specific layer to the most general (Table 2).'], size=7.2, italic=True, color=C['mute'], font=F, align='l', anchor='t')
    # centre
    cg = group(slide); cs = cg.shapes
    box(cs, cx0, 0.15, 4.58, 6.1, fill=CREAM, line='E6DCC6', lw=1, radius=0.03)
    text(cs, cx0, 0.25, 4.58, 0.6, ['The Time Series Agent loop:', 'how the parts work together'], size=12.5, bold=True, color=C['ink'], font='Comic Sans MS')
    for sx, sy in [(4.5, 0.4), (8.6, 0.45), (4.55, 2.4), (8.65, 2.6), (6.05, 1.05), (7.45, 1.1)]:
        text(cs, sx, sy, 0.25, 0.25, '✦', size=11, color=C['llm'])
    # badges around robot
    ring = [('memory', 'MEMORY', 4.55, 1.05), ('tools', 'TOOLS', 4.55, 2.15), ('planning', 'PLANNING', 7.95, 1.05), ('timeline', 'TIME', 7.95, 2.15)]
    for ic, lab, bx, by in ring:
        b = box(cs, bx, by, 0.72, 0.84, fill='FFFFFF', line=C['ink'], lw=1.6, radius=0.18)
        icon(cs, ST, ic, bx + 0.11, by + 0.05, 0.5)
        text(cs, bx, by + 0.56, 0.72, 0.24, lab, size=6.5, bold=True, color=C['ink'], font=HF)
    icon(cs, ST, 'robot', 5.75, 0.95, 1.85)
    banner = box(cs, cx0 + 0.25, 3.05, 4.08, 0.34, fill=NAVY, radius=0.1)
    label_in(banner, 'LLM  ×  HARNESS  ×  TIME  ×  EVALUATION', size=9, font=HF)
    # flow ribbon
    keys = ['llm', 'gh', 'gts', 'tsk', 'ev']
    tw, gap, ty = 0.74, 0.1, 3.75
    x0 = cx0 + (4.58 - (5 * tw + 4 * gap)) / 2
    for k, key in enumerate(keys):
        tx = x0 + k * (tw + gap)
        tile = box(cs, tx, ty, tw, 1.05, fill=C[key], line=C['ink'], lw=1.2, radius=0.08)
        icon(cs, ST, S[key]['icon'], tx + 0.15, ty + 0.06, 0.44)
        text(cs, tx, ty + 0.52, tw, 0.5, [S[key]['short'], S[key]['sec']], size=8, bold=True, color='FFFFFF', font=HF)
        if k < 4:
            arrow(cs, tx + tw, ty + 0.3, tx + tw + gap, ty + 0.3, color=C['ink'], lw=1.6)
    polyline(cs, [(x0 + 4 * (tw + gap) + tw / 2, ty + 1.05), (x0 + 4 * (tw + gap) + tw / 2, ty + 1.32), (x0 + tw / 2, ty + 1.32), (x0 + tw / 2, ty + 1.05)], C['ev'], lw=2.4)
    text(cs, x0 + 0.9, ty + 1.32, 2.6, 0.22, '↺ ' + FLOW['fb'] + ' · or terminate', size=7.5, bold=True, color=C['ev'], font=HF)
    # input / output tags
    for (lab, d, yy) in [('IN', INPUT, 5.45), ('OUT', OUTPUT, 5.82)]:
        b = box(cs, cx0 + 0.3, yy, 0.55, 0.28, fill=C['ink'], radius=0.3)
        label_in(b, lab, size=7.5, font=HF)
        text(cs, cx0 + 0.92, yy, 3.4, 0.28, d['name'] + ' — ' + d['sub'], size=7.4, color=C['ink'], font=F, align='l')
    p.save(out)


if __name__ == '__main__':
    import sys; build(sys.argv[1])
