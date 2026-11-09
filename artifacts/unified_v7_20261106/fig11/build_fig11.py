"""Figure 11 (fig:evaluation-stack), V7 house style.

Upper zone: one evaluation episode, Contract -> Resources -> Execution -> Artifact (stacked papers).
Lower zones (ev hue): the three forms of evidence. Their left-to-right order follows the episode and the
evaluation funnel of the overview figure (process first, task performance last), so the evidence links from
Execution and Artifact do not cross: Execution -> Execution Record; Artifact -> Artifact Validity, Task Performance.
Wording follows the caption and Section 9 (Evaluation contract) of main.tex.
"""
import math, os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *

H = 7.35
EV, EVM, EVL = HUE['ev']
SAND = 'B9A98A'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figure11_V7.pptx')

# ---- upper episode geometry ----------------------------------------------------------------------------------
PY, PH, PW = 1.0, 1.82, 2.6          # paper top, height, width
PX = [0.47, 3.73, 6.99, 10.25]         # paper left edges (stack offset adds 0.14 to the right)
ICS = 0.58                             # icon size in the stages


def caption(sh, cx, y, t, color=MUTE, size=13, w=1.2):
    return tx(sh, cx - w / 2, y, w, 0.24 * (len(t) if isinstance(t, list) else 1) + 0.04, t, size=size, bold=True,
              color=color, anchor='t')


def stage_title(sh, x, y, t):
    tx(sh, x + 0.14, y + 0.06, PW - 0.2, 0.4, t, size=17, bold=True, align='l')


def icon_row(sh, x, y, items, color=MUTE):
    """Three icons with captions spread across a paper."""
    n = len(items)
    for k, (nm, cap) in enumerate(items):
        cx = x + PW * [0.2, 0.5, 0.8][k]
        ic(sh, nm, cx - ICS / 2, y, ICS)
        caption(sh, cx, y + ICS + 0.04, cap, color=color, w=PW / n + 0.25)


def episode(slide):
    g = group(slide); sh = g.shapes
    # 1 Contract
    x = PX[0]; paper(sh, x, PY, PW, PH, SAND); stage_title(sh, x, PY, 'Contract')
    icon_row(sh, x, PY + 0.5, [('schema', ['Output', 'Spec']), ('cutoff', ['Time', 'Cutoff']), ('hourglass', 'Budget')])
    # 2 Resources
    x = PX[1]; paper(sh, x, PY, PW, PH, SAND); stage_title(sh, x, PY, 'Resources')
    icon_row(sh, x, PY + 0.5, [('data', 'Data'), ('code', 'Code'), ('papers', 'Documents')])
    # 3 Execution: a tool call ends in a result or a failure
    x = PX[2]; paper(sh, x, PY, PW, PH, HUE['gh'][1]); stage_title(sh, x, PY, 'Execution')
    tcx, tcy = x + 0.5, PY + 0.88
    ic(sh, 'tools', tcx - 0.33, tcy - 0.33, 0.66)
    caption(sh, tcx, tcy + 0.38, ['Tool', 'Call'], color=HUE['gh'][0], w=0.9)
    rx = x + 1.16
    pr = pill(sh, rx, PY + 0.62, 0.86, 0.38, 'Result', key='gts', size=14, light=True)
    pf = pill(sh, rx, PY + 1.28, 0.86, 0.38, 'Failure', key='tsk', size=14, light=True)
    arrow(sh, tcx + 0.36, tcy - 0.08, rx - 0.04, PY + 0.81, color=HUE['gts'][0], lw=2.2)
    arrow(sh, tcx + 0.36, tcy + 0.1, rx - 0.04, PY + 1.47, color=HUE['tsk'][0], lw=2.2)
    ic(sh, 'failure', rx + 0.92, PY + 1.26, 0.4)
    # 4 Artifact: the submitted prediction and output file
    x = PX[3]; paper(sh, x, PY, PW, PH, EVM); stage_title(sh, x, PY, 'Artifact')
    # output file on the left (checked for validity), prediction on the right (scored for performance)
    mini_forecast(sh, x + 1.04, PY + 0.62, 1.34, 0.52, cut=0.62)
    caption(sh, x + 1.71, PY + 1.42, "Prediction", color=EV, w=1.3)
    fcx = x + 0.52
    ic(sh, 'document', fcx - ICS / 2, PY + 0.5, ICS)
    caption(sh, fcx, PY + 0.5 + ICS + 0.04, ['Output', 'File'], color=EV, w=1.0)
    # sequence arrows
    for k in range(3):
        x0 = PX[k] + PW + 0.2; x1 = PX[k + 1] - 0.06
        col = HUE['gh'][0] if k == 2 else 'A49A86'
        arrow(sh, x0, PY + PH / 2, x1, PY + PH / 2, color=col, lw=2.6)
    return g


# ---- lower evidence zones ------------------------------------------------------------------------------------
ZY, ZH = 3.95, 3.22
ZX = [0.2, 4.62, 9.04]
ZW = 4.09


def record(slide):
    g = group(slide); sh = g.shapes
    x0 = ZX[0]
    px, py, pw = x0 + 0.28, ZY + 0.52, ZW - 0.6
    paper(sh, px, py, pw, 1.22, EVM, n=2)
    rows = [('Call', 'tool(input)'), ('Status', 'Result or Error'), ('Artifact', 'Output Reference')]
    for k, (a, b) in enumerate(rows):
        y = py + 0.05 + k * 0.38
        tx(sh, px + 0.16, y, 1.0, 0.36, a, size=14, bold=True, color=EV, align='l')
        tx(sh, px + 1.12, y, pw - 1.2, 0.36, b, size=13.5, color=INK, align='l')
        if k < 2:
            arrow(sh, px + 0.14, y + 0.375, px + pw - 0.14, y + 0.375, color='D5D7E8', lw=1.0, head=None)
    # resource use
    tx(sh, x0 + 0.2, ZY + 1.86, ZW - 0.4, 0.28, 'Resource Use', size=14, bold=True, color=EV)
    for k, (nm, cap) in enumerate([('stopwatch', 'Latency'), ('utility', 'Cost'), ('tools', 'Tool Use')]):
        cx = x0 + ZW * (k + 0.5) / 3
        ic(sh, nm, cx - 0.26, ZY + 2.16, 0.52)
        caption(sh, cx, ZY + 2.7, cap, color=MUTE, w=1.2)
    return g


def validity(slide):
    g = group(slide); sh = g.shapes
    x0 = ZX[1]
    cw, gap = 1.2, 0.12
    cx0 = x0 + (ZW - 3 * cw - 2 * gap) / 2
    items = [('document', 'File', ['Complete,', 'Readable']), ('schema', 'Schema', ['Required', 'Structure']),
             ('runtime', 'Execution', ['Runs, Loads', 'or Parses'])]
    for k, (nm, title, sub) in enumerate(items):
        x = cx0 + k * (cw + gap)
        card(sh, x, ZY + 0.5, cw, 2.5, key='ev')
        ic(sh, nm, x + cw / 2 - 0.33, ZY + 0.66, 0.66)
        tx(sh, x, ZY + 1.42, cw, 0.32, title, size=15, bold=True, color=EV)
        tx(sh, x, ZY + 1.78, cw, 0.5, sub, size=12.5, color=INK, anchor='t')
        # check mark badge
        b = box(sh, x + cw / 2 - 0.17, ZY + 2.52, 0.34, 0.34, fill=EV, shape=MSO_SHAPE.OVAL)
        poly(sh, [(x + cw / 2 - 0.09, ZY + 2.69), (x + cw / 2 - 0.02, ZY + 2.76), (x + cw / 2 + 0.1, ZY + 2.61)], 'FFFFFF', lw=2.0)
    return g


def _ref(t):
    return 0.55 * math.sin(2 * math.pi * (t * 1.25 + 0.05)) + 0.9 * t


def _pred(t):
    return _ref(t) + 0.22 * math.sin(2 * math.pi * t * 2.3 + 0.8) - 0.1


def performance(slide):
    """Task performance is scored by the output mode of the task grid (Section 6): one row per mode with a reference.
    Decision making is scored by decision utility, a separate criterion."""
    g = group(slide); sh = g.shapes
    x0 = ZX[2]
    card(sh, x0 + 0.22, ZY + 0.5, ZW - 0.44, 2.5, key='ev')
    gx, gw, gh = x0 + 0.42, 1.15, 0.52
    rows = [('Regression', 'Error · CRPS'), ('Classification', 'Accuracy · F1 · Brier'),
            ('Generation', 'Rubric · Fidelity · Claims')]
    for k, (mode, metric) in enumerate(rows):
        y = ZY + 0.66 + k * 0.78
        if k == 0:      # prediction against the held-out reference
            n = 40
            pts = lambda f: [(gx + gw * j / n, y + gh * 0.92 - gh * 0.5 * f(j / n)) for j in range(n + 1)]
            poly(sh, pts(_ref), EV, lw=1.8, dash=MSO_LINE.DASH)
            poly(sh, pts(_pred), INK, lw=1.8)
        elif k == 1:    # predicted labels against true labels
            for j, (lab, ok) in enumerate((('A', True), ('B', False))):
                bx = gx + 0.05 + j * 0.58
                b = box(sh, bx, y + 0.1, 0.3, 0.3, fill=EV if ok else EVM, radius=0.5); label_in(b, lab, size=12)
                cx, cy = bx + 0.42, y + 0.25
                if ok: poly(sh, [(cx - 0.07, cy), (cx - 0.01, cy + 0.07), (cx + 0.09, cy - 0.07)], EV, lw=2.2)
                else:
                    poly(sh, [(cx - 0.06, cy - 0.06), (cx + 0.06, cy + 0.06)], HUE['alert'][0], lw=2.2)
                    poly(sh, [(cx - 0.06, cy + 0.06), (cx + 0.06, cy - 0.06)], HUE['alert'][0], lw=2.2)
        else:           # generated text or series judged without a single reference
            paper(sh, gx + 0.1, y + 0.06, gw - 0.3, gh - 0.06, line=PAPER_LINE, n=2)
            for j in range(3):
                arrow(sh, gx + 0.2, y + 0.16 + 0.11 * j, gx + gw - 0.32 - 0.2 * (j == 2), y + 0.16 + 0.11 * j,
                      color=EVM, lw=2.0, head=None)
        tx(sh, gx + gw + 0.18, y - 0.02, 2.3, 0.3, mode, size=14, bold=True, color=EV, align='l')
        tx(sh, gx + gw + 0.18, y + 0.26, 2.3, 0.28, metric, size=12.5, bold=False, color=INK, align='l')
    return g


def links(slide):
    """Evidence links: each assessment points back to the object it examines."""
    g = group(slide); sh = g.shapes
    ybot = PY + PH + 0.02
    # Execution -> Execution Record (long sweep to the left)
    ex = PX[2] + 0.5
    dot = lambda x, y: box(sh, x - 0.08, y - 0.08, 0.16, 0.16, fill=EV, line='FFFFFF', lw=1.2, shape=MSO_SHAPE.OVAL)
    curve(sh, [(ex, ybot + 0.06), (ex - 1.6, ZY - 0.45), (ZX[0] + ZW / 2 + 1.25, ZY - 0.27)], EV, lw=2.8)
    dot(ex, ybot + 0.04)
    # Artifact -> Artifact Validity and Task Performance
    axx = PX[3] + 0.52
    curve(sh, [(axx, ybot + 0.06), (axx - 0.9, ZY - 0.45), (ZX[1] + ZW / 2 + 1.25, ZY - 0.27)], EV, lw=2.8)
    ax2 = PX[3] + 1.73
    curve(sh, [(ax2, ybot + 0.06), (ax2 - 0.05, ZY - 0.6), (ZX[2] + ZW / 2 + 0.1, ZY - 0.27)], EV, lw=2.8)
    dot(axx, ybot + 0.04); dot(ax2, ybot + 0.04)
    lab = tx(sh, 5.35 - 0.95, 3.25 - 0.15, 1.9, 0.3, 'Evidence Links', size=14, bold=True, italic=True, color=EV)
    lab.rotation = -7
    return g


def build(out=OUT):
    p, slide = new_slide(H)
    zone(slide, 0.2, 0.42, W - 0.4, 2.62, 'Evaluation Episode', key='ink', bw=3.4)
    for x, t in zip(ZX, ['Execution Record', 'Artifact Validity', 'Task Performance']):
        zone(slide, x, ZY, ZW, ZH, t, key='ev', bw=3.1, size=18)
    episode(slide)
    record(slide)
    validity(slide)
    performance(slide)
    links(slide)
    save(p, out)
    return out


if __name__ == '__main__':
    print(build(sys.argv[1] if len(sys.argv) > 1 else OUT))
