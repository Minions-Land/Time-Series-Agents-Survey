"""Figure 15 (fig:open-problems-cases): controlled comparisons for reusable Time Series Agents, V7 house style.

Three zones read left to right per row: Open Question -> Controlled Comparison (paired objects showing the
intervention) -> Evidence to Record. Footer: what to match across the paired conditions.
Row wording follows the old figure and the Open problems subsection.
"""
import os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *

H = 7.18
DD, DM, DL = HUE['data']
ED, EM, EL = HUE['ev']
TD = HUE['tsk'][0]
ZY, ZH = 0.42, 5.62
QZ, CZ, EZ = (0.2, 3.25), (3.65, 5.85), (9.7, 3.43)   # (x, w) of the three zones
R0, PITCH, RH = 0.83, 1.03, 0.88                      # first row top, row pitch, row height
AX, BX = 5.02, 8.13                                   # centres of the paired objects
MID = (AX + BX) / 2
ROWS = [
    # (question lines, icon), comparison kind, (A caption, B caption), evidence lines
    ((['Perception or', 'Execution'], 'reason'), 'vs', ('Model Judgment', 'Numerical Tool'),
     ['Numerical Error', 'Execution Cost']),
    ((['Memory Under', 'Change'], 'memory'), 'to', ('Prior Evidence', 'Revised Values'),
     ['Revalidation', 'Updated Conclusions']),
    ((['Procedure', 'Transfer'], 'trajectory_path'), 'vs', ('Seen Setting', 'Held-Out Setting'),
     ['Held-Out Performance', 'Reuse Success']),
    ((['Evidence', 'Sensitivity'], 'reference_lookup'), 'vs', ('Evidence Present', 'Evidence Removed'),
     ['Response to Removal', 'Grounded Claims']),
    ((['Prediction to', 'Decision'], 'decision'), 'to', ('Forecast', 'Inventory Action'),
     ['Forecast Error', 'Action Utility']),
]


def ico(name, fallback):
    return name if os.path.exists(os.path.join(ICON_DIR, name + '.png')) else fallback


def frame(sh, cx, y, w, h, col, phase, amp=0.9, smooth=False):
    """A tiny plot: axes plus one series."""
    x = cx - w / 2
    poly(sh, [(x, y), (x, y + h), (x + w, y + h)], '9AA0AC', lw=1.2)
    series(sh, x + 0.08, y + 0.02, w - 0.14, h - 0.1, color=col, phase=phase, amp=amp * (1.3 if smooth else 1), lw=1.6,
           smooth=smooth)


def release(sh, cx, y, k, col):
    """A small release sheet: 'Release v_k' with its series."""
    w, h = 1.9, 0.5
    s = box(sh, cx - w / 2, y, w, h, fill='FFFFFF', line=DM, lw=1.3, shape=MSO_SHAPE.RECTANGLE); shadow(s)
    textbox_runs(sh, cx - w / 2 + 0.1, y + 0.04, 1.0, h - 0.08,
                 [('Release v', INK, True, False), (str(k), INK, True, True)], 13.5)
    # the same series in both releases; v2 revises its latest values (red tail)
    import v7kit
    x0, w0, yc, a = cx + 0.22, 0.6, y + h / 2, (h - 0.16) / 2.2
    pts = [(x0 + w0 * j / 30, yc - a * v7kit._y(0.1 + 0.3 * j / 30)) for j in range(31)]
    poly(sh, pts[:21] if k == 2 else pts, INK, lw=1.6)
    if k == 2:
        poly(sh, [(px, py - 0.03 - 0.06 * (j / 10)) for j, (px, py) in enumerate(pts[20:])], col, lw=1.9)


def row(sh, r, spec):
    (qlines, qicon), kind, (ca, cb), ev = spec
    y = R0 + r * PITCH
    gy = y + 0.03                       # glyph band top (0.56 tall), caption below
    cy = gy + 0.28
    # open question
    card(sh, QZ[0] + 0.15, y, QZ[1] - 0.3, RH, 'ink')
    ic(sh, ico(qicon, 'reason'), QZ[0] + 0.24, y + 0.12, 0.64)
    tx(sh, QZ[0] + 0.95, y + 0.06, QZ[1] - 1.15, RH - 0.12, qlines, size=15.5, bold=True, align='l')
    # paired objects
    for cx, cap in ((AX - (0.5 if r == 4 else 0), ca), (BX, cb)):   # row 5: caption steps left of the τ pill
        tx(sh, cx - 1.1, gy + 0.58, 2.2, 0.27, cap, size=13.5, bold=True, color=DD)
    if r == 0:
        ic(sh, 'llm', AX - 0.3, gy - 0.02, 0.6); ic(sh, 'tools', BX - 0.3, gy - 0.02, 0.6)
    elif r == 1:
        release(sh, AX, gy + 0.04, 1, INK); release(sh, BX, gy + 0.04, 2, TD)
    elif r == 2:
        frame(sh, AX, gy + 0.02, 1.35, 0.52, INK, 0.0); frame(sh, BX, gy + 0.02, 1.35, 0.52, HUE['gh'][0], 0.31, smooth=True)
    elif r == 3:
        ic(sh, ico('evidence_check', 'data'), AX - 0.29, gy, 0.58)
        box(sh, BX - 0.26, gy + 0.03, 0.52, 0.52, fill='FFFFFF', line='9AA0AC', lw=1.4, radius=0.15, dash=MSO_LINE.DASH)
        arrow(sh, BX - 0.14, gy + 0.15, BX + 0.14, gy + 0.43, color=TD, lw=2.6, head=None)
        arrow(sh, BX + 0.14, gy + 0.15, BX - 0.14, gy + 0.43, color=TD, lw=2.6, head=None)
    elif r == 4:
        mini_forecast(sh, AX - 0.72, gy + 0.03, 1.44, 0.4)
        ic(sh, ico('inventory_boxes', 'decision'), BX - 0.29, gy, 0.58)
    if kind == 'vs':
        v = box(sh, MID - 0.25, cy - 0.2, 0.5, 0.4, fill=DL, line=DM, lw=1.0, radius=0.5)
        label_in(v, 'vs.', size=13, color=DD)
    else:
        arrow(sh, MID - 0.42, cy, MID + 0.42, cy, color=DD, lw=2.6)
    # evidence to record
    paper(sh, EZ[0] + 0.2, y + 0.12, EZ[1] - 0.55, RH - 0.14, line=EM)
    tx(sh, EZ[0] + 0.2, y + 0.12, EZ[1] - 0.55, RH - 0.14, ev, size=14, bold=True, color=ED)
    # read each row left to right
    arrow(sh, QZ[0] + QZ[1] - 0.12, cy, AX - 0.95, cy, color='A49A86', lw=2.2)
    arrow(sh, BX + 0.95, cy, EZ[0] + 0.14, cy, color='A49A86', lw=2.2)


def footer(slide):
    g = group(slide); sh = g.shapes
    y, h = 6.28, 0.7
    items = [('llm', 'Backbone'), ('cutoff', 'Information Boundary'), ('utility', 'Resource Budget')]
    widths = [1.75, 2.95, 2.45]
    total = 1.3 + 0.35 + sum(widths) + 0.3 * 2
    x0 = (W - total) / 2
    card(sh, x0 - 0.2, y, total + 0.4, h, 'ink')
    pl = box(sh, x0, y + 0.13, 1.3, h - 0.26, fill=INK, radius=0.5); shadow(pl)
    label_in(pl, 'Match', size=16)
    x = x0 + 1.3 + 0.35
    for (nm, lab), w in zip(items, widths):
        ic(sh, nm, x, y + 0.08, 0.54)
        tx(sh, x + 0.62, y, w - 0.62, h, lab, size=14.5, bold=True, align='l')
        x += w + 0.3
    return g


def build(out):
    p, slide = new_slide(H)
    zone(slide, QZ[0], ZY, QZ[1], ZH, 'Open Question', 'ink')
    zone(slide, CZ[0], ZY, CZ[1], ZH, 'Controlled Comparison', 'data')
    zone(slide, EZ[0], ZY, EZ[1], ZH, 'Evidence to Record', 'ev')
    for r, spec in enumerate(ROWS):
        g = group(slide)
        row(g.shapes, r, spec)
    footer(slide)
    save(p, out)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'Figure15_V7.pptx'))
