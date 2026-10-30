"""Build Figure 1 (survey organization) as an editable one-slide PPTX.

The survey reads as the construction of a Time Series Agent: define, build,
evaluate, advance. The build stage shows the LLM side beside the three
Harness layers, ordered from general to specific. Styling follows the
editorial figures (warm grey fill, navy lines, dashed section boxes, Comic
Sans headings); layer tints match the colours in Figure 3.
"""
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).with_name("Figure01_Organization.pptx")
HEAD_FONT, LABEL_FONT = "Comic Sans MS", "Arial"
NAVY, INK, GREY, FILL = (RGBColor.from_string(h) for h in ("304B63", "1F1F1F", "767670", "F1F1EE"))
LAYERS = {  # border, tint
    "llm": (RGBColor.from_string("E8A033"), RGBColor.from_string("FBF0DA")),
    "gh": (RGBColor.from_string("3A5398"), RGBColor.from_string("E5EAF4")),
    "gts": (RGBColor.from_string("00A087"), RGBColor.from_string("DDF2EC")),
    "tsk": (RGBColor.from_string("E64B35"), RGBColor.from_string("FBE5E0")),
}

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(14.25), Inches(4.75)
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def write(shape, lines, size=17, font=HEAD_FONT, color=INK, align=PP_ALIGN.CENTER):
    frame = shape.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    frame.margin_left = frame.margin_right = Inches(0.1)
    for i, parts in enumerate(lines):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        para.alignment = align
        for content, part_color in parts:
            run = para.add_run()
            run.text = content
            run.font.name, run.font.size, run.font.bold = font, Pt(size), True
            run.font.color.rgb = part_color or color


def box(x, y, w, h, number, title, border=NAVY, tint=FILL, dashed=True):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.adjustments[0] = 0.12
    shape.fill.solid()
    shape.fill.fore_color.rgb = tint
    shape.line.color.rgb, shape.line.width = border, Pt(2)
    if dashed:
        shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    shape.shadow.inherit = False
    write(shape, [[(f"§ {number}", border if not dashed else NAVY)], [(title, None)]])
    return shape


def connector(x1, y1, x2, y2, color=NAVY, width=2.25, dashed=False, head=True):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    line.line.color.rgb, line.line.width = color, Pt(width)
    if dashed:
        line.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    if head:
        ln = line.line._get_or_add_ln()
        etree.SubElement(ln, A_NS + "tailEnd", type="triangle", w="med", len="med")


def label(x, y, w, h, content, size=20, font=HEAD_FONT, color=NAVY, rotation=0):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    write(shape, [[(content, color)]], size=size, font=font)
    shape.rotation = rotation


TOP, BOTTOM = 0.95, 3.85
MID = (TOP + BOTTOM) / 2

# Define
label(0.35, 0.25, 2.5, 0.5, "Define")
box(0.35, TOP, 2.5, 1.25, 1, "Introduction")
box(0.35, BOTTOM - 1.4, 2.5, 1.4, 2, "What Is a Time Series Agent?")

# Build: LLM side beside the Harness layers, general to specific
label(3.35, 0.25, 5.65, 0.5, "Build")
border, tint = LAYERS["llm"]
box(3.35, TOP, 1.45, BOTTOM - TOP, 3, "LLM side", border, tint, dashed=False)
stack_x, stack_w, layer_h, layer_gap = 4.95, 3.55, 0.82, 0.22
for k, (key, number, title) in enumerate([("gh", 4, "General Harness"),
                                           ("gts", 5, "General Time Series Harness"),
                                           ("tsk", 6, "Task-Specific Harness")]):
    border, tint = LAYERS[key]
    shape = box(stack_x, TOP + k * (layer_h + layer_gap), stack_w, layer_h, number, title, border, tint, dashed=False)
    shape.text_frame.paragraphs[0].runs[0].text = f"§ {number}  "
    first, second = shape.text_frame.paragraphs
    first.runs[0].font.size = Pt(17)
    run = first.add_run()
    run.text = second.runs[0].text
    run.font.name, run.font.size, run.font.bold, run.font.color.rgb = HEAD_FONT, Pt(17), True, INK
    second._p.getparent().remove(second._p)
connector(8.72, TOP + 0.1, 8.72, BOTTOM - 0.1, color=GREY, width=1.5)
label(7.95, MID - 0.17, 1.95, 0.34, "general to specific", size=12.5, font=LABEL_FONT, color=GREY, rotation=90)

# Evaluate
label(9.65, 0.25, 2.1, 0.5, "Evaluate")
box(9.65, MID - 0.9, 2.1, 1.8, 7, "Infrastructure and Benchmarks")

# Advance
label(12.3, 0.25, 1.6, 0.5, "Advance")
box(12.3, TOP, 1.6, 1.25, 8, "Open Problems")
box(12.3, BOTTOM - 1.25, 1.6, 1.25, 9, "Conclusion")

# Stage flow and evaluation feedback
for x1, x2 in ((2.88, 3.3), (9.15, 9.6), (11.8, 12.25)):
    connector(x1, MID, x2, MID)
connector(10.7, MID + 0.92, 10.7, 4.32, color=GREY, width=1.5, dashed=True, head=False)
connector(10.7, 4.32, 6.72, 4.32, color=GREY, width=1.5, dashed=True, head=False)
connector(6.72, 4.32, 6.72, BOTTOM + 0.04, color=GREY, width=1.5, dashed=True)
label(7.55, 4.3, 2.3, 0.36, "feedback", size=12.5, font=LABEL_FONT, color=GREY)

prs.save(OUT)
print(OUT)
