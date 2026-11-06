"""Shared style kit for the survey's figures, taken from the approved overview figure (V7 Atelier).

Reference figure: artifacts/overview_flow_20261106/V7_Atelier_Build.pdf (source: ../../overview_flow_20261106/build/v7_atelier.py).

STYLE RULES (every figure must follow them so the paper reads as one set)
- Canvas: 13.333 in wide (new_slide), height chosen for the content (typically 5.0-7.5 in). All figures are placed
  at \\linewidth, so equal canvas width keeps type sizes equal across the paper.
- Font: Comic Sans MS everywhere (F). Sizes: zone banners 18-19 pt bold white; card / panel titles 15-17 pt bold;
  labels and icon captions 12.5-14 pt; nothing below 11.5 pt. Short labels use Title Case ("Observed Series").
  Uppercase only for verb stamps (REUSE / ADAPT / REDESIGN).
- Wording: take labels from the manuscript (headings, captions, body text). Do not invent claims, verbs or names.
- Palette (HUE): muted, blue-violet as the main colour; one semantic hue per survey component (dark, mid, light):
  llm ochre, gh steel blue, gts sea teal, tsk soft terracotta, ev blue-violet; 'data' warm grey for inputs;
  'ink' blue-violet for frames and banners; 'alert' muted brick only for small error / failure marks.
  No large red areas. Zones are tinted without frames; cards have shadows without outlines.
  Dark = text, outlines, arrows, banner fills; mid = side faces / secondary fills; light = surfaces.
- Layout grammar:
  * zone(): pale tinted rounded panel with a dashed outline and a dark pill banner centred on its top edge.
  * paper(): a stack of white sheets with a drop shadow for documents, inputs, records, outputs.
  * card(): a single white rounded card with shadow for a self-contained item.
  * plate(): an oblique 3D slab (front face carries the label) for layers / platforms; pedestal() for an object
    that stands on something (agents, models).
  * Clay icons (ic) carry meaning; captions under icons are 1-2 Title Case words.
  * Arrows: curved (curve) or straight (arrow), 2.2-3.2 pt, in the hue of the component that emits them;
    dashed for returned observations / feedback; no shadows on arrows.
  * Time series: series() for observed data, mini_forecast() for history -> t0 -> forecast band.
- Depth: shadow() on cards, plates, banners and funnel layers only. Light alpha fills allowed; no gradients.
- Native PowerPoint only: every element is an editable shape, text box or picture; group each logical block with
  group(slide) so the figure can be ungrouped and edited.
"""
import math, os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.abspath(os.path.join(HERE, '..', '..', 'overview_flow_20261106', 'icons', 'clay'))
F = 'Comic Sans MS'
W = 13.333
INK, MUTE = '262A4D', '666A84'
# Muted palette, blue-violet as the main colour (2026-11-06). Red is not a component colour any more:
# it is reserved for small error / warning marks (key 'alert').
HUE = dict(  # (dark, mid, light)
    llm=('B0852F', 'E5CD9B', 'FBF6EA'),    # LLM side: ochre
    gh=('44689F', 'AFC1DE', 'EEF2F9'),     # General Harness: steel blue
    gts=('37807A', 'A3CCC8', 'ECF5F4'),    # General Time Series Harness: sea teal
    tsk=('BC6E52', 'E8B8A5', 'FBF0EB'),    # Task-Specific Harness: soft terracotta (chosen 2026-11-06)
    ev=('4B4F96', 'B5B8DA', 'F0F1F8'),     # Evaluation: the main blue-violet
    data=('857A68', 'D9D2C4', 'FAF8F3'),   # scenario / inputs: warm grey
    ink=('4B4F96', 'B5B8DA', 'F0F1F8'),    # frames and banners: the main blue-violet
    alert=('B5574B', 'E6B1AA', 'FAEDEB'))  # errors, failures, late data only
ZONE_FILL = dict(llm='FDFAF3', gh='F5F8FC', gts='F4F9F8', tsk='FDF7F4', ev='F6F7FB', data='FBFAF6', ink='F6F7FB',
                 alert='FDF6F5')
PAPER_LINE = 'CDD0E0'


def rgb(h):
    return RGBColor.from_string(h)


def new_slide(h, w=W):
    p = Presentation()
    p.slide_width, p.slide_height = Inches(w), Inches(h)
    s = p.slides.add_slide(p.slide_layouts[6])
    box(s.shapes, 0, 0, w, h, fill='FFFFFF', shape=MSO_SHAPE.RECTANGLE)
    return p, s


def group(slide_or_group):
    return slide_or_group.shapes.add_group_shape()


def box(sh, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=None, dash=None):
    s = sh.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None: s.fill.background()
    else: s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    if line is None: s.line.fill.background()
    else:
        s.line.color.rgb = rgb(line); s.line.width = Pt(lw)
        if dash: s.line.dash_style = dash
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE: s.adjustments[0] = radius
    etree.SubElement(s._element.spPr, qn('a:effectLst'))   # no theme shadow
    return s


def text(sh, x, y, w, h, t, size=13, bold=False, color=INK, align='c', anchor='m', italic=False, wrap=False):
    """Text box; t is a string or a list of lines."""
    tb = sh.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = Inches(0.02); tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    for i, ln in enumerate(t if isinstance(t, list) else [t]):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        r = para.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = F; f.color.rgb = rgb(color)
    return tb


tx = text


def label_in(shape, t, size=13, bold=True, color='FFFFFF', align='c', italic=False):
    tf = shape.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04); tf.margin_top = tf.margin_bottom = Inches(0.01)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, ln in enumerate(t if isinstance(t, list) else [t]):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        r = para.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = F; f.color.rgb = rgb(color)
    return shape


def runs(shape, parts, size, align='c'):
    """Styled runs in one line: parts = [(text, colour, bold, subscript)]. Works on shapes and text boxes."""
    tf = shape.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
    for t, col, b, sub in parts:
        r = p.add_run(); r.text = t; f = r.font; f.size = Pt(size); f.bold = b; f.name = F; f.color.rgb = rgb(col)
        if sub: r.font._rPr.set('baseline', '-25000')
    return shape


def textbox_runs(sh, x, y, w, h, parts, size, align='c'):
    return runs(sh.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)), parts, size, align)


def ic(sh, name, x, y, s):
    """Clay icon from the shared library (ICON_DIR/<name>.png). Missing icons show as a grey disc."""
    path = os.path.join(ICON_DIR + '_print', name + '.png')   # print-size copy (shrink_icons.py)
    if not os.path.exists(path): path = os.path.join(ICON_DIR, name + '.png')
    if not os.path.exists(path):
        return box(sh, x, y, s, s, fill='DDDDDD', shape=MSO_SHAPE.OVAL)
    return sh.add_picture(path, Inches(x), Inches(y), width=Inches(s), height=Inches(s))


SHADOW = ('<a:outerShdw xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" blurRad="76200" dist="50800" '
          'dir="3600000" algn="tl" rotWithShape="0"><a:srgbClr val="3A3020"><a:alpha val="32000"/></a:srgbClr></a:outerShdw>')
SKETCH = ('<a:extLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:ext uri="{C807C97D-BFC1-408E-A445-0C87EB9F89A2}">'
          '<ask:lineSketchStyleProps xmlns:ask="http://schemas.microsoft.com/office/drawing/2018/sketchyshapes" sd="1219033472">'
          '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><ask:type><ask:lineSketchFreehand/></ask:type>'
          '</ask:lineSketchStyleProps></a:ext></a:extLst>')


def shadow(shape):
    sp = shape._element.spPr
    ef = sp.find(qn('a:effectLst'))
    if ef is None: ef = etree.SubElement(sp, qn('a:effectLst'))
    ef.append(etree.fromstring(SHADOW))
    return shape


def sketchy(shape):
    """Hand-drawn outline (PowerPoint 365 renders it; Keynote shows a plain line)."""
    ln = shape._element.spPr.find(qn('a:ln'))
    if ln is not None: ln.append(etree.fromstring(SKETCH))
    return shape


def alpha_fill(shape, val):
    clr = shape.fill._xPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
    etree.SubElement(clr, qn('a:alpha')).set('val', str(int(val * 1000)))


def poly(sh, pts, color, lw=1.6, dash=None, fill=None, alpha=None, closed=False):
    ff = sh.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    ff.add_line_segments([(Inches(x), Inches(y)) for x, y in pts[1:]], close=closed)
    s = ff.convert_to_shape()
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
        if alpha is not None: alpha_fill(s, alpha)
    else: s.fill.background()
    if color:
        s.line.color.rgb = rgb(color); s.line.width = Pt(lw)
        if dash: s.line.dash_style = dash
    else: s.line.fill.background()
    return s


def arrow(sh, x1, y1, x2, y2, color=INK, lw=2.2, dash=None, head='triangle', tail=None):
    c = sh.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
    if dash: c.line.dash_style = dash
    ln = c.line._get_or_add_ln()
    if tail:
        e = etree.SubElement(ln, qn('a:headEnd')); e.set('type', tail); e.set('w', 'med'); e.set('len', 'med')
    if head:
        e = etree.SubElement(ln, qn('a:tailEnd')); e.set('type', head); e.set('w', 'med'); e.set('len', 'med')
    return c


def bezier(pts, n=40):
    (x0, y0), (cx, cy), (x1, y1) = pts
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1)
            for t in [k / n for k in range(n + 1)]]


def curve(sh, pts, color, lw=2.6, dash=None, head=True):
    """Quadratic Bezier [(start), (control), (end)] with an arrowhead at the end."""
    s = poly(sh, bezier(pts), color, lw=lw, dash=dash)
    if head:
        e = etree.SubElement(s.line._get_or_add_ln(), qn('a:tailEnd')); e.set('type', 'triangle'); e.set('w', 'med'); e.set('len', 'med')
    return s


def banner(sh, cx, y, w, title, fill, size=19, h=0.5):
    b = box(sh, cx - w / 2, y, w, h, fill=fill, radius=0.5); shadow(b)
    label_in(b, title, size=size)
    return b


def zone(slide, x, y, w, h, title, key='ink', bw=None, size=19):
    """Tinted dashed panel with a dark pill banner on its top edge. bw: banner width (default from title length)."""
    g = group(slide); sh = g.shapes
    dk, md, lt = HUE[key]
    box(sh, x, y, w, h, fill=ZONE_FILL[key], radius=min(0.035, 0.25 / max(h, 1)))   # tint only, no frame
    if title:
        bw = bw or min(w - 0.3, 0.155 * len(title) * size / 19 + 0.6)
        banner(sh, x + w / 2, y - 0.25, bw, title, dk, size=size)   # banner in the zone's (muted) component colour
    return g


def pill(sh, x, y, w, h, t, key='ink', size=14, light=False):
    """Rounded tag. light=True gives a pale tag with dark text; otherwise a dark tag with white text."""
    dk, md, lt = HUE[key]
    b = box(sh, x, y, w, h, fill=lt if light else dk, radius=0.5)
    return label_in(b, t, size=size, color=dk if light else 'FFFFFF')


def paper(sh, x, y, w, h, line='B9A98A', n=3):
    """A stack of n sheets, offset up-right, with a drop shadow. Returns the front sheet."""
    for k in range(n - 1, -1, -1):
        s = box(sh, x + 0.07 * k, y - 0.07 * k, w, h, fill='FFFFFF', line=PAPER_LINE, lw=1.0 if k == 0 else 0.75,
                shape=MSO_SHAPE.RECTANGLE)
        sketchy(s)
        if k == n - 1: shadow(s)
    return s


def card(sh, x, y, w, h, key='ink', fill='FFFFFF', lw=1.3, radius=0.08):
    s = box(sh, x, y, w, h, fill=fill, radius=radius)   # no outline: the shadow separates the card
    shadow(s)
    return s


def plate(sh, x, y, w, key, label_parts=None, depth=(0.6, -0.5), t=0.4, size=17):
    """Oblique slab: (x, y) is the front-left top corner, w the front width. label_parts as in runs()."""
    dk, md, lt = HUE[key]
    dx, dy = depth
    front = [(x, y), (x + w, y), (x + w, y + t), (x, y + t)]
    side = [(x + w, y), (x + w + dx, y + dy), (x + w + dx, y + dy + t), (x + w, y + t)]
    top = [(x, y), (x + w, y), (x + w + dx, y + dy), (x + dx, y + dy)]
    shadow(poly(sh, front, dk, lw=1.0, fill=dk, closed=True))
    poly(sh, side, dk, lw=1.0, fill=md, closed=True)
    poly(sh, top, dk, lw=1.3, fill=lt, closed=True)
    i = 0.07
    poly(sh, [(x + i * 2.2, y - i), (x + w - i * 0.6, y - i), (x + w + dx - i * 2.2, y + dy + i), (x + dx + i * 0.6, y + dy + i)],
         'FFFFFF', lw=1.2, closed=True)
    if label_parts:
        textbox_runs(sh, x, y + 0.02, w, t - 0.06, label_parts, size)


def pedestal(sh, x, y, w, h, key='llm'):
    dk, md, lt = HUE[key]
    e = box(sh, x, y, w, h, fill=lt, line=md, lw=1.4, shape=MSO_SHAPE.OVAL); shadow(e)
    box(sh, x + 0.08 * w, y + 0.12 * h, 0.84 * w, 0.62 * h, line='FFFFFF', lw=1.0, shape=MSO_SHAPE.OVAL)
    return e


def halo(sh, cx, cy, w, h, color='FFF1CC', alpha=55):
    e = box(sh, cx - w / 2, cy - h / 2, w, h, fill=color, shape=MSO_SHAPE.OVAL); alpha_fill(e, alpha)
    return e


def trapezoid(sh, cx, ya, yb, wa, wb, key='ev', fill=None):
    """Funnel / ladder layer: top width wa at ya, bottom width wb at yb."""
    s = poly(sh, [(cx - wa / 2, ya), (cx + wa / 2, ya), (cx + wb / 2, yb), (cx - wb / 2, yb)], HUE[key][0], lw=1.3,
             fill=fill or HUE[key][2], closed=True)
    return shadow(s)


def cylinder(sh, x, y, w, h, key='gh'):
    """Database / pool drum."""
    dk, md, lt = HUE[key]
    c = box(sh, x, y, w, h, fill=lt, line=dk, lw=1.3, shape=MSO_SHAPE.CAN)
    shadow(c)
    return c


# ---- time series glyphs -------------------------------------------------------------------------------------
def _y(t):
    noise = 0.16 * math.sin(97.1 * t + 0.3) + 0.11 * math.sin(211.7 * t + 2.0) + 0.07 * math.sin(353.9 * t)
    return 0.5 * math.sin(2 * math.pi * t * 5.2) + 0.2 * math.sin(2 * math.pi * t * 17.3 + 1.1) + 0.4 * t + noise


def _calm(t):
    return 0.5 * math.sin(2 * math.pi * t * 5.2) + 0.4 * t


def series(sh, x, y, w, h, color=INK, phase=0.0, amp=1.0, lw=1.6, smooth=False, n=90):
    """A deterministic seasonal series in the box (x, y, w, h). Returns the point list as well."""
    f = _calm if smooth else _y
    pts = [(x + w * k / n, y + h / 2 - h / 2.6 * amp * f((k / n + phase) % 1.0)) for k in range(n + 1)]
    poly(sh, pts, color, lw=lw)
    return pts


def mini_forecast(sh, x, y, w, h, cut=0.62, t0_label=True):   # the pill shows the decision time τ
    """Observed history up to t0, then a dashed forecast inside a widening band."""
    n = 110; kc = int(n * cut); amp = h / 2.6
    xs = [x + w * k / n for k in range(n + 1)]
    ys = [y + h / 2 - amp * _y(k / n) for k in range(n + 1)]
    off = ys[kc] - (y + h / 2 - amp * _calm(kc / n))
    for k in range(kc + 1, n + 1):
        ys[k] = y + h / 2 - amp * _calm(k / n) + off
    m = n - kc
    up = [(xs[k], ys[k] - 0.02 - 0.17 * (k - kc) / m) for k in range(kc, n + 1)]
    lo = [(xs[k], ys[k] + 0.02 + 0.17 * (k - kc) / m) for k in range(kc, n + 1)]
    poly(sh, up + lo[::-1], None, fill=HUE['tsk'][0], alpha=22, closed=True)
    poly(sh, list(zip(xs[:kc + 1], ys[:kc + 1])), INK, lw=1.5)
    poly(sh, list(zip(xs[kc:], ys[kc:])), HUE['tsk'][0], lw=1.8, dash=MSO_LINE.DASH)
    t0 = xs[kc]
    arrow(sh, t0, y - 0.06, t0, y + h + 0.02, color=HUE['gts'][0], lw=1.4, dash=MSO_LINE.DASH, head=None)
    if t0_label:
        p = box(sh, t0 - 0.22, y + h + 0.02, 0.44, 0.24, fill=HUE['gts'][0], radius=0.5)
        runs(p, [('τ', 'FFFFFF', True, False)], 15)
        r = p.text_frame.paragraphs[0].runs[0]; r.font.name = 'Times New Roman'; r.font.italic = True   # matches $\tau$ in the text
    return t0


def save(p, path):
    p.save(path)
    return path
