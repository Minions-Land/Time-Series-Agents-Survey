"""Shared content and native-shape helpers for the overview-flow figure variants."""
import copy, os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(ROOT, 'logos')          # institution logos taken from the Figure 2 PPTX
ICONS = {'pixel': os.path.join(ROOT, 'icons', 'pixel'), 'clay': os.path.join(ROOT, 'icons', 'clay')}

# Palette follows Figure 1 of the manuscript.
C = dict(llm='F0A030', gh='3B5BA5', gts='2A9D8F', tsk='E05A47', ev='5B5F97',
         ink='1F2A44', mute='6B7280', cream='FBF3E4', white='FFFFFF', navy='16213E')

# Content states the survey's construction claims; no paper names, institutions or section numbers.
STAGES = [
    dict(key='llm', name='LLM', short='LLM', verb='ALIGN', icon='llm',
         role='interprets temporal evidence and selects actions',
         claim='Not enough alone: it acts through the harness',
         items=['Represent numbers for the language model', 'Reason over temporal evidence', 'Learn which workflow action to take']),
    dict(key='gh', name='General Harness', short='GH', verb='REUSE', icon='runtime',
         role='domain-independent runtime',
         claim='Carry it over from general Agents',
         items=['Interaction & memory', 'Tools & execution', 'Planning & coordination', 'Feedback & self-improvement']),
    dict(key='gts', name='General Time Series Harness', short='GTS', verb='ADAPT', icon='timeline',
         role='temporal semantics shared across tasks',
         claim='Add time where a generic runtime is ambiguous',
         items=['Timestamps, units, missingness', 'Windows, resampling, decomposition', 'Only information available at t₀', 'Chronology guards & validators']),
    dict(key='tsk', name='Task-Specific Harness', short='TSK', verb='REBUILD', icon='forecast',
         role='procedures bound to one task contract',
         claim='Rebuild around output, objective and actions',
         items=['Forecasting', 'Synthesis & augmentation', 'Anomaly diagnosis', 'Decision support']),
    dict(key='ev', name='Evaluation', short='EVAL', verb='VERIFY', icon='validate',
         role='tests the complete workflow',
         claim='Valid run ≠ accurate result ≠ useful decision',
         items=['Process validity', 'Temporal validity', 'Task performance', 'Decision utility']),
]
S = {s['key']: s for s in STAGES}
INPUT = dict(name='Scenario & data', sub='series · context · task request', icon='timeseries')
OUTPUT = dict(name='Accepted output', sub='forecast · diagnosis · decision', icon='decision')
FLOW = dict(act='action', obs='observation', ops='temporal operations', cap='shared temporal capabilities',
            cand='candidate output', fb='feedback: revise', stop='accept / terminate', axis='scope of reuse: general → specific')
TITLE = 'How to Build a Time Series Agent'
MOTTO = 'Reuse what is general  ·  adapt what is temporal  ·  rebuild what is task-bound'
KEY = 'Align model capability, harness responsibility and evaluation'


def rgb(h):
    return RGBColor.from_string(h)


def new_pres(w=13.333, h=6.4):
    p = Presentation()
    p.slide_width, p.slide_height = Inches(w), Inches(h)
    return p, p.slides.add_slide(p.slide_layouts[6])


def box(shapes, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=None, dash=None, shadow=False):
    s = shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = rgb(line); s.line.width = Pt(lw)
        if dash: s.line.dash_style = dash
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if not shadow:
        sp = s._element.spPr
        ef = etree.SubElement(sp, qn('a:effectLst'))
    s.text_frame.text = ''
    return s


def text(shapes, x, y, w, h, t, size=10, bold=False, color='1F2A44', font='Avenir Next', align='c', anchor='m', italic=False, wrap=True):
    tb = shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = Inches(0.02); tf.margin_top = tf.margin_bottom = Inches(0.0)
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        r = para.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = font; f.color.rgb = rgb(color)
    return tb


def label_in(shape, t, size=10, bold=True, color='FFFFFF', font='Avenir Next', align='c'):
    tf = shape.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04); tf.margin_top = tf.margin_bottom = Inches(0.01)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER}[align]
        r = para.add_run(); r.text = ln
        f = r.font; f.size = Pt(size); f.bold = bold; f.name = font; f.color.rgb = rgb(color)
    return shape


def pic(shapes, path, x, y, w=None, h=None):
    kw = {}
    if w: kw['width'] = Inches(w)
    if h: kw['height'] = Inches(h)
    return shapes.add_picture(path, Inches(x), Inches(y), **kw)


def icon(shapes, style, name, x, y, size):
    path = os.path.join(ICONS[style], name + '.png')
    if not os.path.exists(path):
        return box(shapes, x, y, size, size, fill='DDDDDD', shape=MSO_SHAPE.OVAL)
    return pic(shapes, path, x, y, w=size, h=size)


def logo(shapes, fname, x, y, size):
    if not fname:
        return None
    stem = os.path.splitext(fname)[0]
    path = next(os.path.join(MEDIA, f) for f in os.listdir(MEDIA) if os.path.splitext(f)[0] == stem)
    return pic(shapes, path, x, y, w=size, h=size)


def arrow(shapes, x1, y1, x2, y2, color='1F2A44', lw=1.75, dash=None, head='triangle', tail=None, curve=False):
    kind = MSO_CONNECTOR.CURVE if curve else MSO_CONNECTOR.STRAIGHT
    c = shapes.add_connector(kind, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
    if dash: c.line.dash_style = dash
    ln = c.line._get_or_add_ln()
    if tail:
        e = etree.SubElement(ln, qn('a:headEnd')); e.set('type', tail); e.set('w', 'med'); e.set('len', 'med')
    if head:
        e = etree.SubElement(ln, qn('a:tailEnd')); e.set('type', head); e.set('w', 'med'); e.set('len', 'med')
    return c


SKETCH = ('<a:extLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:ext uri="{C807C97D-BFC1-408E-A445-0C87EB9F89A2}">'
          '<ask:lineSketchStyleProps xmlns:ask="http://schemas.microsoft.com/office/drawing/2018/sketchyshapes" sd="1219033472">'
          '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><ask:type><ask:lineSketchFreehand/></ask:type>'
          '</ask:lineSketchStyleProps></a:ext></a:extLst>')


def sketchy(shape):
    """Office 365 hand-drawn outline; renders natively in PowerPoint."""
    ln = shape._element.spPr.find(qn('a:ln'))
    if ln is None:
        return shape
    ln.append(etree.fromstring(SKETCH))
    return shape


def group(slide):
    return slide.shapes.add_group_shape()
