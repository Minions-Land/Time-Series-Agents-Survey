# Visual system for the survey figures

## Purpose

This file defines the shared visual language for the figures in *From General to Specific: A Survey of Time-Series Agent Systems*. It is the design source for native PowerPoint assets and the PNGs consumed by `main.tex`.

## Production workflow

1. Fix the information architecture and the text labels before drawing.
2. Build the figure as native PowerPoint objects in a section-specific `.pptx` source.
3. Export a PNG from the same source and inspect the rendered result at paper size.
4. Check component editability in PowerPoint: text, fills, lines, arrows, and tables must remain independent objects; the full composition must be groupable and ungroupable.
5. Replace the LaTeX PNG only after the PPT and PNG pass visual checks.

Legacy PNGs remain in place until an active PPT source passes this workflow.

## Typography

- Primary typeface: Times New Roman.
- Figure title: 28–32 pt equivalent on a 1600×900 canvas.
- Section labels: 18–22 pt, bold.
- Topic labels: 16–18 pt, regular or semibold.
- Supporting text: 13–15 pt.
- Use sentence case and short noun phrases. Avoid code-like labels, unexplained abbreviations, and decorative slogans.

## Palette

| Semantic role | Hex | Use |
|---|---|---|
| Ink | `#1E2F47` | Titles, section labels, structure lines |
| Muted ink | `#6B7280` | Supporting text |
| LLM | `#EEEAF7` / `#7058A6` | LLM-side contributions |
| General Harness | `#E4EFF4` / `#2D6E8F` | General runtime mechanisms |
| General Time-Series Harness | `#E8F2EA` / `#3E8167` | Cross-task temporal mechanisms |
| Task-Specific Harness | `#F8F1DF` / `#B78324` | Task-bound mechanisms |
| Evidence / infrastructure | `#E9F0F4` / `#467A92` | Benchmarks, traces, and paper-card evidence |
| Paper card | `#FBFBF8` / `#1E2F47` | Ledger and evidence layer |

Use low-saturation fills, dark outlines, and one semantic accent per row. Do not use gradients or image slices in the final assets.

## Geometry

- Canvas: 1600×900 (16:9) for editable PPT sources.
- Outer margin: 56–72 px.
- Main content aligns to a 12-column grid.
- Dashed rounded rectangles indicate section or taxonomy boundaries.
- Solid connectors indicate the reading path; they sit behind content boxes.
- Small circles on a vertical rail mark section order.
- Bottom paper-card strip is reserved for fields that make the evidence layer explicit.

## Figure roles

- Introduction: module-level contribution timeline.
- What Is a Time-Series Agent: nested construction and paper-card unit.
- LLM-Side: temporal representation, alignment, and language reasoning.
- General Harness: seven reusable runtime dimensions.
- General Time-Series Harness: temporal objects, operations, evidence, and contracts.
- Task-Specific Harness: four task families with the same seven-module lens.
- Infrastructure and Benchmarks: traces, tools, evaluators, and benchmark coverage.
- Open Problems and Case Studies: evidence-backed gaps and representative systems.

