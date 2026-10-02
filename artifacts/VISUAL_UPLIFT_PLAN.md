# Visual uplift plan

## Target

The survey will use one visual system across the main text and appendix. Each large section receives a figure whose visual grammar is stable, while the figure's content answers the section's specific question.

## Section-to-figure map

| Section | Figure purpose | Current source | Next action |
|---|---|---|---|
| Introduction | Module-level publication and contribution timeline | `artifacts/contribution_timeline.png` | Rebuild as a native editable chart/diagram with the module-level counting rule |
| What Is a Time-Series Agent | Construction hierarchy and Paper Card unit | `artifacts/Overview.png` plus the Paper Card text box | Consolidate into one native composition |
| LLM-Side Contributions | Temporal representation, alignment, instruction, and reasoning | `artifacts/paper_figures/redrawn/chatts_overview.png` | Replace the screenshot-style asset with a clean editable mechanism map |
| General Harness | Seven reusable runtime dimensions | Text and Table 3 | Build a seven-dimension radial or linear map with the same palette |
| General Time-Series Harness | Temporal objects, operations, evidence, and contracts | `artifacts/rsi_figures/gts_landscape.png` | Build a temporal-contract landscape with explicit reusable mechanisms |
| Task-Specific Harness | Four task families under the same seven-module lens | `artifacts/rsi_figures/research_routes.png` | Build a four-branch task map and retain task-specific labels |
| Infrastructure and Benchmarks | Traces, tools, evaluators, and benchmark coverage | `artifacts/paper_figures/redrawn/timeseriesgym_benchmark.png`, `timeclaw_runtime.png` | Build one evaluation-contract figure and one benchmark coverage table |
| Open Problems and Case Studies | Evidence-backed gaps and representative systems | Existing open-problem material | Build a six-panel route map only after claims and citations are checked |

## Acceptance criteria for every figure

- The source is a native `.pptx` with independent text, fills, lines, arrows, and table/chart objects.
- The composition remains groupable and ungroupable in PowerPoint without flattening.
- Times New Roman is used consistently unless a cited source requires another font.
- Colors encode the four contribution layers consistently: LLM, General Harness, General Time-Series Harness, and Task-Specific Harness.
- The PNG used by LaTeX is exported from the same PPT source.
- The figure has a short caption that states what the figure establishes and cites the source when the visual grammar or an adapted mechanism comes from prior work.
- The figure is checked at paper size for text fit, line crossings, and caption placement.

## Current checkpoint

Figure 2 is the first active source. Its native PowerPoint source is `artifacts/active/Figure2_organization_native_v2.pptx`; the LaTeX PNG is `artifacts/active/Figure2_organization_native_v2.png`. The figure uses the RSI organization-map structure while replacing its content with the current nine-section survey plan and Paper Card evidence layer.

The old PNGs remain available as legacy references. They are not overwritten until their replacements pass the same workflow.

## Order of work

1. Figure 2 organization map (completed checkpoint).
2. Overview / construction hierarchy and Paper Card.
3. Module-level contribution timeline.
4. General Harness seven-dimension map.
5. General Time-Series Harness temporal-contract map.
6. Task-Specific Harness four-family map.
7. Evaluation and benchmark map.
8. Open-problem and case-study map.
9. Full-paper visual audit, compile, render, and synchronized push.

