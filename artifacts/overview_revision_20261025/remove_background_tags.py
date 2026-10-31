"""Remove background-reference tags from the overview PDF and close the gap they leave."""
import sys
import pymupdf as fitz

SRC, OUT = sys.argv[1], sys.argv[2]
BOLD = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
doc = fitz.open(SRC)
page = doc[0]
spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]
images = page.get_image_info(xrefs=True)


def tag(name, y_hint=None):
    cands = [s for s in spans if s["text"].strip() == name]
    if y_hint is not None:
        cands.sort(key=lambda s: abs(s["bbox"][1] - y_hint))
    s = cands[0]
    cy = (s["bbox"][1] + s["bbox"][3]) / 2
    year = min((y for y in spans if y["text"].strip().isdigit() and abs((y["bbox"][1] + y["bbox"][3]) / 2 - cy) < 8
                and 0 <= y["bbox"][0] - s["bbox"][2] < 20), key=lambda y: y["bbox"][0] - s["bbox"][2])
    logo = min((i for i in images if abs((i["bbox"][1] + i["bbox"][3]) / 2 - cy) < 10 and 0 < s["bbox"][0] - i["bbox"][2] < 12),
               key=lambda i: s["bbox"][0] - i["bbox"][2])
    return {"name": s, "year": year, "logo": logo}


def rect(*boxes, pad=0.6):
    r = fitz.Rect(boxes[0])
    for b in boxes[1:]:
        r |= fitz.Rect(b)
    return r + (-pad, -pad, pad, pad)


def color(span):
    c = span["color"]
    return ((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)


font = fitz.Font(fontfile=BOLD)
removed = {n: tag(n) for n in ("GridMind", "Grid-Agent", "Tree-of-Evidence")}
zara = tag("ZARA")
zara_logo = doc.extract_image(zara["logo"]["xref"])["image"]

targets = [*removed.values(), zara]
# Pass 1: text only, images untouched.
for t in targets:
    for key in ("name", "year"):
        page.add_redact_annot(rect(t[key]["bbox"], pad=0.3), fill=False)
page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                      text=fitz.PDF_REDACT_TEXT_REMOVE)
# Pass 2: only the target logos, with boxes that touch no other image.
keep = [fitz.Rect(i["bbox"]) for i in images if i["xref"] not in {t["logo"]["xref"] for t in targets}]
for t in targets:
    box = fitz.Rect(t["logo"]["bbox"])
    for other in keep:
        if box.intersects(other):
            box = fitz.Rect(box.x0, box.y0, box.x1, min(box.y1, other.y0 - 0.5)) if other.y0 > box.y0 else fitz.Rect(box.x0, max(box.y0, other.y1 + 0.5), box.x1, box.y1)
    assert not any(box.intersects(o) for o in keep), t["name"]["text"]
    page.add_redact_annot(box, fill=False)
page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                      text=fitz.PDF_REDACT_TEXT_NONE)

# Move ZARA into the slot GridMind occupied, keeping row alignment.
slot = removed["GridMind"]
lw, lh = (fitz.Rect(zara["logo"]["bbox"]).width, fitz.Rect(zara["logo"]["bbox"]).height)
x0, y0 = slot["logo"]["bbox"][:2]
page.insert_image(fitz.Rect(x0, y0, x0 + lw, y0 + lh), stream=zara_logo)
name, year = zara["name"], zara["year"]
page.insert_text(slot["name"]["origin"], name["text"].strip(), fontname="tnrb", fontfile=BOLD,
                 fontsize=name["size"], color=color(name))
x = slot["name"]["origin"][0] + font.text_length(name["text"].strip(), fontsize=name["size"]) + (year["bbox"][0] - name["bbox"][2])
page.insert_text((x, slot["year"]["origin"][1]), year["text"].strip(), fontname="tnrb", fontfile=BOLD,
                 fontsize=year["size"], color=color(year))

doc.save(OUT, garbage=3, deflate=True)
print("removed:", list(removed), "| moved: ZARA")
