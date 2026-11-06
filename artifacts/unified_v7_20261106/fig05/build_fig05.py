"""Figure 5 (fig:llm-contributions): LLM-side intervention points in a Time Series Agent, V7 house style.

Top: the three LLM-side routes (Section 3 subsections), each as input -> learned target plus its feedback signal;
A 'One Method' link joins the first two routes (caption: routes can overlap within one method).
Middle: the interaction loop. The LLM (amber) floats above the Harness plate (blue), which executes calls and
returns observations; dotted drop lines locate each route in the loop.
Bottom: the four evaluation targets named in the caption.
"""
import os, sys
sys.path.insert(0, '/Users/mjm/Papers/Qingsong/IJCAI2027-Time-Series-Agents-Survey/artifacts/unified_v7_20261106/kit')
from v7kit import *

H = 7.2
LD, LM, LL = HUE['llm']
GD, GM, GL = HUE['gh']
ED, EM, EL = HUE['ev']
CX = W / 2
CARD_W, CARD_GAP, CARD_Y, CARD_H = 3.95, 0.3, 0.84, 1.92
CARD_X = [0.2 + (12.93 - 3 * CARD_W - 2 * CARD_GAP) / 2 + k * (CARD_W + CARD_GAP) for k in range(3)]
ROUTES = [  # (title, (icon, caption), (icon, caption), feedback) -- wording from the old figure / Section 3
    ('Representation and Alignment', ('window', 'Series Patches'), ('encode', 'Language Space'),
     'Scale and Temporal Structure'),
    ('Instruction and Reasoning', ('request', 'Temporal Questions'), ('grounded_answer', 'Grounded Answers'),
     'Instructions and Outcome Feedback'),
    ('Workflow Learning', ('trajectory_path', 'Tool Trajectories'), ('policy', 'Action Policy'),
     'Execution and Preference Feedback'),
]
# interaction loop geometry
P = 5.18                  # front-top y of the Harness plate
PX, PW = 0.45, 11.85      # plate front-left x and width
LOOP = dict(obs=1.6, tool=9.65, out=11.5)   # icon centres on the plate's top face
ROBOT = (CX, 2.95, 1.3)   # centre x, top y, size


def ico(name):
    p = os.path.join(ICON_DIR, name + '.png')
    return name if os.path.exists(p) else {'grounded_answer': 'chat', 'trajectory_path': 'process'}.get(name, name)


def routes(slide):
    zone(slide, 0.2, 0.42, 12.93, 2.56, 'LLM-Side Intervention Points', 'llm')
    g = group(slide); sh = g.shapes
    root = sh
    for x0, (title, a, b, fb) in zip(CARD_X, ROUTES):
        sh = root.add_group_shape().shapes
        card(sh, x0, CARD_Y, CARD_W, CARD_H, 'llm')
        tx(sh, x0, CARD_Y + 0.08, CARD_W, 0.38, title, size=16, bold=True)
        iy, isz = CARD_Y + 0.5, 0.7
        for cx, (nm, cap) in ((x0 + 1.0, a), (x0 + CARD_W - 1.0, b)):
            ic(sh, ico(nm), cx - isz / 2, iy, isz)
            tx(sh, cx - 1.0, iy + isz + 0.02, 2.0, 0.28, cap, size=13.5, bold=True, color=LD)
        arrow(sh, x0 + 1.47, iy + isz / 2, x0 + CARD_W - 1.47, iy + isz / 2, color=LD, lw=2.6)
        pill(sh, x0 + 0.22, CARD_Y + CARD_H - 0.42, CARD_W - 0.44, 0.31, fb, 'llm', size=12.5, light=True)
    # one method can span the first two routes (no work names in figures)
    sh = root.add_group_shape().shapes
    gx = CARD_X[0] + CARD_W + CARD_GAP / 2
    yy = CARD_Y + 0.5 + 0.35
    arrow(sh, gx - 0.66, yy, gx + 0.66, yy, color=LD, lw=1.6, dash=MSO_LINE.ROUND_DOT, head=None)
    t = pill(sh, gx - 0.6, yy - 0.17, 1.2, 0.34, 'One Method', 'llm', size=12.5)
    shadow(t)
    return g


def loop(slide):
    g = group(slide); sh = g.shapes
    # Harness plate
    plate(sh, PX, P, PW, 'gh', [('Harness:  ', 'FFFFFF', True, False),
                                ('Execution, State and Feedback', 'FFFFFF', False, False)], size=17)
    base = P - 0.3                    # captions sit on the plate's top face
    items = [('obs', 'timeseries', 'Observations'), ('tool', 'tools', 'Tool Actions'), ('out', 'data', 'Outputs')]
    for key, nm, cap in items:
        cx = LOOP[key]
        ic(sh, nm, cx - 0.43, base - 0.88, 0.86)
        tx(sh, cx - 0.9, base - 0.02, 1.8, 0.27, cap, size=14, bold=True, color=GD)
    # LLM on its pedestal
    rx, ry, rs = ROBOT
    halo(sh, rx, ry + 0.62, 1.85, 1.6)
    pedestal(sh, rx - 0.62, ry + rs - 0.2, 1.24, 0.32, 'llm')
    ic(sh, 'robot', rx - rs / 2, ry, rs)
    lab = box(sh, rx + 0.5, ry + 0.02, 0.7, 0.34, fill=LD, radius=0.5); label_in(lab, 'LLM', size=14)
    # Observations -> LLM (Harness encodes / retrieves), LLM -> Tool Actions (select and assess)
    ox = LOOP['obs']
    curve(sh, [(ox + 0.5, base - 0.62), (3.4, 3.05), (rx - 0.8, ry + 0.6)], GD, lw=2.8)
    tx(sh, 2.55, 3.1, 2.4, 0.3, 'Encode / Retrieve', size=14, bold=True, italic=True, color=GD)
    tox = LOOP['tool']
    curve(sh, [(rx + 0.8, ry + 0.6), (9.1, 3.05), (tox - 0.42, base - 0.72)], LD, lw=2.8)
    tx(sh, 7.95, 3.1, 2.4, 0.3, 'Select and Assess', size=14, bold=True, italic=True, color=LD)
    arrow(sh, tox + 0.5, base - 0.44, LOOP['out'] - 0.5, base - 0.44, color=GD, lw=2.6)
    # returned observations: Tool Actions back to Observations, under the LLM
    curve(sh, [(tox - 0.5, base - 0.42), (rx, base - 0.25), (ox + 0.5, base - 0.42)], GD, lw=2.4, dash=MSO_LINE.DASH)
    # drop lines: where each route acts in the loop
    for x, y1 in ((3.75, 3.08), (rx, ry - 0.02), (9.15, 3.08)):
        arrow(sh, x, CARD_Y + CARD_H + 0.04, x, y1, color=LD, lw=2.0, dash=MSO_LINE.ROUND_DOT, head=None)
    return g


def evaluation(slide):
    y0 = 6.07
    zone(slide, 0.2, y0, 12.93, 1.02, 'Evaluation Targets', 'ev')
    g = group(slide); sh = g.shapes
    items = [('forecast', ['Forecast', 'Accuracy']), ('validate', ['Explanation', 'Faithfulness']),
             ('evidence_check', ['Evidence', 'Grounding']), ('benchmark', ['Action', 'Quality'])]
    cw, gap = 2.75, 0.4
    x = 0.2 + (12.93 - 4 * cw - 3 * gap) / 2
    for nm, lab in items:
        card(sh, x, y0 + 0.34, cw, 0.6, 'ev')
        ic(sh, nm if os.path.exists(os.path.join(ICON_DIR, nm + '.png')) else 'data', x + 0.14, y0 + 0.36, 0.56)
        tx(sh, x + 0.82, y0 + 0.36, cw - 0.9, 0.56, lab, size=13.5, bold=True, color=ED, align='l')
        x += cw + gap
    return g


def build(out):
    p, slide = new_slide(H)
    routes(slide)
    loop(slide)
    evaluation(slide)
    save(p, out)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'Figure05_V7.pptx'))
