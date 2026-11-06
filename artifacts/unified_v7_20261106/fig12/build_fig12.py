"""Figure 12 (fig:benchmark-landscape), V7 house style: executable evaluation in TimeSeriesGym.

Left (data sand): the challenge package, i.e. resources, a task-defined data split and the task description.
Centre (ink): the workspace in which the Agent edits code, executes it, inspects the output and saves an artifact;
execution leaves an execution record. Right (ev indigo): the challenge grader, i.e. validity checks and task score.
Top: the shared challenge contract (task requirements) feeds both the package and the grader.
Wording follows the caption, the TimeSeriesGym paragraph of Section 9 and the old figure.
"""
import math, os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *

H = 7.25
EV, EVM, EVL = HUE['ev']
DK, DM, DL = HUE['data']
GH = HUE['gh'][0]
AMB = HUE['llm'][0]
SAND = 'B9A98A'
ARR = 'A49A86'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figure12_V7.pptx')

ZY = 1.2                      # top of the three zones
ZB = 7.07                     # bottom of the three zones
PKG = (0.2, 3.62)             # x, w
WSP = (4.0, 5.33)
GRD = (9.51, 3.62)


def caption(sh, cx, y, t, color=MUTE, size=13, w=1.2):
    return tx(sh, cx - w / 2, y, w, 0.28, t, size=size, bold=True, color=color, anchor='t')


def contract(slide):
    """The shared challenge contract at the top feeds both the package and the grader."""
    g = group(slide); sh = g.shapes
    cw, ch = 3.3, 0.6
    x, y = W / 2 - cw / 2, 0.12
    c = card(sh, x, y, cw, ch, key='data', fill='FFFFFF')
    c.line.color.rgb = rgb(SAND)
    ic(sh, 'request', x + 0.1, y + 0.04, 0.52)
    tx(sh, x + 0.66, y + 0.05, cw - 0.75, ch - 0.1, 'Task Requirements', size=17, bold=True, align='l')
    curve(sh, [(x - 0.02, y + ch / 2), (PKG[0] + PKG[1] / 2, y + ch / 2), (PKG[0] + PKG[1] / 2, ZY - 0.28)], ARR, lw=2.6)
    curve(sh, [(x + cw + 0.02, y + ch / 2), (GRD[0] + GRD[1] / 2, y + ch / 2), (GRD[0] + GRD[1] / 2, ZY - 0.28)], ARR, lw=2.6)
    return g


def package(slide):
    g = group(slide); sh = g.shapes
    x0, w0 = PKG
    px, pw = x0 + 0.2, w0 - 0.48
    # resources
    py = ZY + 0.55
    paper(sh, px, py, pw, 1.42, SAND)
    tx(sh, px + 0.12, py + 0.04, 2.0, 0.36, 'Resources', size=16, bold=True, align='l')
    for k, (nm, cap) in enumerate([('data', 'Data'), ('code', 'Code'), ('papers', 'Papers'), ('document', 'Docs')]):
        cx = px + pw * (k + 0.5) / 4
        ic(sh, nm, cx - 0.27, py + 0.43, 0.54)
        caption(sh, cx, py + 1.0, cap, w=0.85)
    # task-defined data split
    sy = ZY + 2.25
    card(sh, px, sy, pw + 0.14, 1.12, key='data')
    tx(sh, px + 0.1, sy + 0.06, pw, 0.32, 'Task-Defined Data Split', size=15, bold=True, align='l')
    bx, bw = px + 0.16, pw - 0.18
    fills = [DM, DM, EVM]
    for k, f in enumerate(fills):
        box(sh, bx + k * bw / 3 + 0.02, sy + 0.46, bw / 3 - 0.04, 0.22, fill=f, line=None, radius=0.3)
    tx(sh, px + 0.1, sy + 0.74, pw, 0.3, 'Availability and Evaluation Rules', size=12.5, color=MUTE, align='l')
    # task description
    ty = ZY + 3.72
    paper(sh, px, ty, pw, 1.95, SAND)
    ic(sh, 'request', px + 0.06, ty + 0.04, 0.5)
    tx(sh, px + 0.6, ty + 0.08, 2.3, 0.4, 'Task Description', size=16, bold=True, align='l')
    rows = [('Output', 'Task-Defined Artifact'), ('Budget', 'Time and Resources'), ('Grader', 'Task-Specific Criteria')]
    for k, (a, b) in enumerate(rows):
        y = ty + 0.62 + k * 0.42
        tx(sh, px + 0.12, y, 0.9, 0.36, a, size=14, bold=True, color=DK, align='l')
        tx(sh, px + 0.95, y, pw - 1.0, 0.36, b, size=12.5, color=INK, align='l')
    return g


def step(sh, x, y, w, h, title, icon=None):
    card(sh, x, y, w, h, key='gh')
    if icon:
        ic(sh, icon, x + 0.08, y + (h - 0.54) / 2, 0.54)
        tx(sh, x + 0.62, y, w - 0.66, h, title, size=15, bold=True, color=GH, align='l')
    else:
        tx(sh, x, y + 0.04, w, 0.32, title, size=15, bold=True, color=GH)


def workspace(slide):
    g = group(slide); sh = g.shapes
    x0, w0 = WSP
    sx, sw, sh_ = 5.86, 1.74, 0.84       # step column
    ys = [ZY + 0.5, ZY + 1.72, ZY + 2.94]
    # access resources
    tx(sh, x0 + 0.1, ys[0] - 0.02, 1.75, 0.3, 'Access Resources', size=13.5, bold=True, italic=True, color=DK, align='l')
    arrow(sh, PKG[0] + PKG[1] - 0.12, ys[0] + 0.5, sx - 0.04, ys[0] + 0.5, color=ARR, lw=2.6)
    # steps: edit code -> execute -> inspect output
    step(sh, sx, ys[0], sw, sh_, ['Edit', 'Code'], 'code')
    step(sh, sx, ys[1], sw, sh_, 'Execute', 'runtime')
    step(sh, sx, ys[2], sw, sh_ + 0.36, 'Inspect Output')
    # inspect output: output vs reference
    n = 40; ax, ay, aw, ah = sx + 0.18, ys[2] + 0.42, sw - 0.36, 0.66
    f_ref = lambda t: math.sin(2 * math.pi * t * 1.7 + 0.4)
    f_out = lambda t: 0.85 * math.sin(2 * math.pi * t * 1.7 + 0.15) + 0.08
    poly(sh, [(ax + aw * k / n, ay + ah / 2 - ah * 0.42 * f_ref(k / n)) for k in range(n + 1)], EV, lw=1.6, dash=MSO_LINE.DASH)
    poly(sh, [(ax + aw * k / n, ay + ah / 2 - ah * 0.42 * f_out(k / n)) for k in range(n + 1)], INK, lw=1.8)
    for k in range(2):
        arrow(sh, sx + sw / 2, ys[k] + sh_ + 0.03, sx + sw / 2, ys[k + 1] - 0.05, color=GH, lw=2.4)
    # revise loop: inspect output -> edit code
    curve(sh, [(sx - 0.03, ys[2] + 0.6), (sx - 0.7, ys[1] + 0.4), (sx - 0.04, ys[0] + 0.66)], AMB, lw=2.6, dash=MSO_LINE.DASH)
    # the Agent
    rs = 1.3
    rx, ry = x0 + 0.13, ZY + 2.05
    halo(sh, rx + rs / 2, ry + rs / 2 + 0.05, 1.32, 1.45)
    pedestal(sh, rx + 0.05, ry + rs - 0.2, rs - 0.1, 0.32, 'llm')
    ic(sh, 'robot', rx, ry - 0.08, rs)
    tx(sh, rx - 0.1, ry + rs + 0.16, rs + 0.2, 0.32, 'Agent', size=16, bold=True, color=AMB)
    # default budget of the reported protocol (Section 9: four hours and 50 steps)
    bx, by, bw, bh = x0 + 0.18, ZB - 1.17, 1.62, 0.95
    card(sh, bx, by, bw, bh, key='data')
    ic(sh, 'hourglass', bx + 0.06, by + 0.17, 0.6)
    t = tx(sh, bx + 0.66, by + 0.08, bw - 0.7, bh - 0.16, ['Budget', '4 Hours', '50 Steps'], size=12.5, bold=True, color=MUTE, align='l')
    t.text_frame.paragraphs[0].runs[0].font.size = Pt(14); t.text_frame.paragraphs[0].runs[0].font.color.rgb = rgb(DK)
    # execution record
    rcx, rcw = sx + sw + 0.32, x0 + w0 - (sx + sw + 0.32) - 0.22
    ry1 = ys[1] - 0.62
    paper(sh, rcx, ry1, rcw, 1.86, HUE['gh'][1], n=2)
    ic(sh, 'logs', rcx + rcw / 2 - 0.28, ry1 + 0.08, 0.56)
    tx(sh, rcx, ry1 + 0.66, rcw, 0.6, ['Execution', 'Record'], size=14, bold=True, color=GH, anchor='t')
    tx(sh, rcx, ry1 + 1.22, rcw, 0.56, ['Calls · Status', 'Logs · Errors'], size=12.5, color=INK, anchor='t')
    arrow(sh, sx + sw + 0.03, ys[1] + sh_ / 2, rcx - 0.04, ys[1] + sh_ / 2, color=GH, lw=2.4)
    # saved artifact
    ay2 = ys[2] + sh_ + 0.75
    paper(sh, sx + 0.08, ay2, sw - 0.16, 1.02, EVM, n=2)
    ic(sh, 'document', sx + sw / 2 - 0.27, ay2 + 0.06, 0.54)
    caption(sh, sx + sw / 2, ay2 + 0.63, 'Saved Artifact', color=EV, size=13.5, w=1.6)
    arrow(sh, sx + sw / 2, ys[2] + sh_ + 0.39, sx + sw / 2, ay2 - 0.16, color=EV, lw=2.4)
    # submit
    y = ay2 + 0.5
    arrow(sh, sx + sw + 0.04, y, GRD[0] + 0.12, y, color=EV, lw=2.8)
    tx(sh, sx + sw + 0.2, y - 0.36, 1.4, 0.3, 'Submit', size=14, bold=True, italic=True, color=EV)
    return g


def grader(slide):
    g = group(slide); sh = g.shapes
    x0, w0 = GRD
    cx, cw = x0 + 0.26, w0 - 0.46
    # validity
    vy, vh = ZY + 0.5, 2.0
    card(sh, cx, vy, cw, vh, key='ev')
    ic(sh, 'validate', cx + 0.1, vy + 0.08, 0.56)
    tx(sh, cx + 0.72, vy + 0.1, 2.0, 0.5, 'Validity', size=16, bold=True, color=EV, align='l')
    for k, t in enumerate(['File Format and Structure', 'Required Outputs', 'Executable Output']):
        y = vy + 0.74 + k * 0.4
        b = box(sh, cx + 0.16, y + 0.04, 0.26, 0.26, fill=EV, shape=MSO_SHAPE.OVAL)
        poly(sh, [(cx + 0.22, y + 0.17), (cx + 0.27, y + 0.23), (cx + 0.36, y + 0.11)], 'FFFFFF', lw=1.6)
        tx(sh, cx + 0.52, y, cw - 0.56, 0.34, t, size=13, color=INK, align='l')
    # task score
    sy, shh = ZY + 2.78, 2.92
    card(sh, cx, sy, cw, shh, key='ev')
    ic(sh, 'benchmark', cx + 0.1, sy + 0.08, 0.56)
    tx(sh, cx + 0.72, sy + 0.1, 2.0, 0.5, 'Task Score', size=16, bold=True, color=EV, align='l')
    ax, ay, aw, ah = cx + 0.25, sy + 0.72, cw - 0.5, 1.0
    arrow(sh, ax, ay, ax, ay + ah, color=MUTE, lw=1.2, head=None)
    arrow(sh, ax, ay + ah, ax + aw, ay + ah, color=MUTE, lw=1.2)
    n = 50
    f_ref = lambda t: math.sin(2 * math.pi * t * 1.6 + 0.3) * (1 - 0.3 * t)
    f_out = lambda t: math.sin(2 * math.pi * t * 1.6 + 0.12) * (1 - 0.35 * t) + 0.06
    poly(sh, [(ax + 0.06 + (aw - 0.2) * k / n, ay + ah * 0.48 - ah * 0.36 * f_ref(k / n)) for k in range(n + 1)], EV, lw=1.8, dash=MSO_LINE.DASH)
    poly(sh, [(ax + 0.06 + (aw - 0.2) * k / n, ay + ah * 0.48 - ah * 0.36 * f_out(k / n)) for k in range(n + 1)], INK, lw=2.0)
    ly = ay + ah + 0.22
    lx = cx + 0.3
    arrow(sh, lx, ly, lx + 0.32, ly, color=INK, lw=2.0, head=None)
    tx(sh, lx + 0.38, ly - 0.15, 1.0, 0.3, 'Output', size=13, bold=True, align='l')
    lx = cx + 1.5
    arrow(sh, lx, ly, lx + 0.32, ly, color=EV, lw=2.0, dash=MSO_LINE.DASH, head=None)
    tx(sh, lx + 0.38, ly - 0.15, 1.2, 0.3, 'Reference', size=13, bold=True, color=EV, align='l')
    tx(sh, cx + 0.1, sy + 2.2, cw - 0.2, 0.3, 'Task-Specific Evaluation', size=13.5, bold=True, color=EV)
    tx(sh, cx + 0.1, sy + 2.5, cw - 0.2, 0.3, 'Metrics Follow the Challenge', size=12.5, color=MUTE)
    # bracket: the grader checks the submitted artifact as a whole
    bx = x0 + 0.13
    poly(sh, [(bx + 0.07, vy + 0.15), (bx, vy + 0.15), (bx, sy + shh - 0.15), (bx + 0.07, sy + shh - 0.15)], EVM, lw=1.6)
    return g


def build(out=OUT):
    p, slide = new_slide(H)
    zone(slide, PKG[0], ZY, PKG[1], ZB - ZY, 'Challenge Package', key='data', bw=3.1, size=18)
    zone(slide, WSP[0], ZY, WSP[1], ZB - ZY, 'Workspace', key='ink', bw=2.3, size=18)
    zone(slide, GRD[0], ZY, GRD[1], ZB - ZY, 'Challenge Grader', key='ev', bw=3.1, size=18)
    contract(slide)
    package(slide)
    workspace(slide)
    grader(slide)
    save(p, out)
    return out


if __name__ == '__main__':
    print(build(sys.argv[1] if len(sys.argv) > 1 else OUT))
