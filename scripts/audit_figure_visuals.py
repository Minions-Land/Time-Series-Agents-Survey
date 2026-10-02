#!/usr/bin/env python3
"""Audit native figure sources against the PNGs consumed by main.tex.

The comparison intentionally ignores PNG metadata and compares decoded pixels.
This verifies that the active PNG is the export used to approve the composition,
while the PPTX package counts provide a lightweight native-object check.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[1]


PAIRS = [
    ("Figure 1", ".ppt-build/figure1-active/figure1-timeline.png", "artifacts/active/Figure1_module_timeline_native.png", "artifacts/active/Figure1_module_timeline_native.pptx"),
    ("Figure 2", ".ppt-build/figure2-active/figure2-organization.png", "artifacts/active/Figure2_organization_native_v2.png", "artifacts/active/Figure2_organization_native_v2.pptx"),
    ("Figure 3", ".ppt-build/figure3-active/figure3-construction.png", "artifacts/active/Figure3_construction_native.png", "artifacts/active/Figure3_construction_native.pptx"),
    ("Figure 4", ".ppt-build/figure4-active/figure4-general-harness.png", "artifacts/active/Figure4_general_harness_native_v2.png", "artifacts/active/Figure4_general_harness_native_v2.pptx"),
    ("Figure 5", ".ppt-build/figure5-active/figure5-general-ts-harness.png", "artifacts/active/Figure5_general_ts_harness_native.png", "artifacts/active/Figure5_general_ts_harness_native.pptx"),
    ("Figure 6", ".ppt-build/figure6-active/figure6-task-specific.png", "artifacts/active/Figure6_task_specific_native_v2.png", "artifacts/active/Figure6_task_specific_native_v2.pptx"),
    ("Figure 7", ".ppt-build/figure7-active/figure7-infrastructure.png", "artifacts/active/Figure7_infrastructure_native.png", "artifacts/active/Figure7_infrastructure_native.pptx"),
    ("Figure 8", ".ppt-build/figure8-active/figure8-open-problems.png", "artifacts/active/Figure8_open_problems_native.png", "artifacts/active/Figure8_open_problems_native.pptx"),
    ("LLM-side", ".ppt-build/figure-llm-active/figure-llm-side.png", "artifacts/active/Figure_LLM_side_native_v3.png", "artifacts/active/Figure_LLM_side_native_v3.pptx"),
    ("Supporting: AION", ".ppt-build/redrawn-2.png", "artifacts/active/Figure_support_aion.png", "artifacts/active/Figure_supporting_workflows_native.pptx"),
    ("Supporting: MERIT", ".ppt-build/redrawn-3.png", "artifacts/active/Figure_support_merit.png", "artifacts/active/Figure_supporting_workflows_native.pptx"),
    ("Supporting: AnomaMind", ".ppt-build/redrawn-4.png", "artifacts/active/Figure_support_anomamind.png", "artifacts/active/Figure_supporting_workflows_native.pptx"),
    ("Supporting: TS-Agent", ".ppt-build/redrawn-7.png", "artifacts/active/Figure_support_tsagent.png", "artifacts/active/Figure_supporting_workflows_native.pptx"),
]


PPT_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
TAG_NAMES = {
    "sp": f"{{{PPT_NS}}}sp",
    "cxnSp": f"{{{PPT_NS}}}cxnSp",
    "pic": f"{{{PPT_NS}}}pic",
    "graphicFrame": f"{{{PPT_NS}}}graphicFrame",
}


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def pixel_report(export_path: Path, active_path: Path) -> dict:
    exported = Image.open(export_path).convert("RGBA")
    active = Image.open(active_path).convert("RGBA")
    if exported.size != active.size:
        return {
            "status": "size-mismatch",
            "export_size": list(exported.size),
            "active_size": list(active.size),
        }
    diff = ImageChops.difference(exported, active)
    stats = ImageStat.Stat(diff)
    changed = sum(1 for pixel in diff.getdata() if pixel != (0, 0, 0, 0))
    total = exported.width * exported.height
    return {
        "status": "exact" if changed == 0 else "pixel-difference",
        "size": list(exported.size),
        "mean_absolute_difference": round(sum(stats.mean) / len(stats.mean), 6),
        "changed_pixel_fraction": round(changed / total, 8),
    }


def native_object_report(pptx_path: Path) -> dict:
    counts = {key: 0 for key in TAG_NAMES}
    slide_count = 0
    with zipfile.ZipFile(pptx_path) as package:
        slide_names = sorted(
            name for name in package.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        )
        slide_count = len(slide_names)
        for name in slide_names:
            root = ET.fromstring(package.read(name))
            for key, tag in TAG_NAMES.items():
                counts[key] += len(root.findall(f".//{tag}"))
    counts["total_native_objects"] = sum(counts.values())
    counts["slide_count"] = slide_count
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="artifacts/figure_visual_audit_20261002.json")
    parser.add_argument("--markdown", default="artifacts/FIGURE_OVERLAY_QA_20261002.md")
    args = parser.parse_args()

    tex = (ROOT / "main.tex").read_text(encoding="utf-8")
    rows = []
    for label, export_rel, active_rel, pptx_rel in PAIRS:
        export_path = ROOT / export_rel
        active_path = ROOT / active_rel
        pptx_path = ROOT / pptx_rel
        pixels = pixel_report(export_path, active_path) if export_path.exists() and active_path.exists() else {"status": "missing"}
        native = native_object_report(pptx_path) if pptx_path.exists() else {"status": "missing"}
        rows.append({
            "label": label,
            "export_preview": export_rel,
            "active_png": active_rel,
            "pptx": pptx_rel,
            "latex_reference": active_rel in tex,
            "pixels": pixels,
            "native_objects": native,
        })

    overall = "pass" if all(
        row["latex_reference"] and row["pixels"].get("status") == "exact" and row["native_objects"].get("total_native_objects", 0) > 0
        for row in rows
    ) else "review"
    report = {
        "date": dt.date.today().isoformat(),
        "status": overall,
        "comparison": "Decoded PNG pixels; metadata ignored",
        "rows": rows,
    }
    json_path = ROOT / args.json
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Figure overlay and native-source audit",
        "",
        f"Date: {report['date']}",
        "",
        "The audit compares each active PNG with the decoded pixel output produced by its native PowerPoint source. PNG metadata is ignored. It also checks that the active PNG is referenced by `main.tex` and counts native PowerPoint shape, connector, picture, and graphic-frame objects in the source package.",
        "",
        "| Figure | Export preview | Active PNG | Pixel result | Size | Native objects | LaTeX reference |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        px = row["pixels"]
        native = row["native_objects"]
        lines.append(
            f"| {row['label']} | `{row['export_preview']}` | `{row['active_png']}` | {px.get('status', 'missing')} | {tuple(px.get('size', [])) or 'missing'} | {native.get('total_native_objects', 0)} | {'yes' if row['latex_reference'] else 'no'} |"
        )
    lines.extend([
        "",
        f"Overall status: **{overall}**.",
        "",
        "All current pairs are expected to report `exact`; this is the source-to-PNG gate before a figure is used in LaTeX. The PowerPoint Group -> Ungroup -> single-component edit test is recorded separately in `artifacts/VISUAL_QA_20261002.md`.",
        "",
    ])
    md_path = ROOT / args.markdown
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": overall, "json": relative(json_path), "markdown": relative(md_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
