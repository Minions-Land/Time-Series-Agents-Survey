# Visual uplift plan

## Target

The survey will use one visual system across the main text and appendix. Each large section receives a figure whose visual grammar is stable, while the figure's content answers the section's specific question.

## Section-to-figure map

| Section | Figure purpose | Current source | Next action |
|---|---|---|---|
| Introduction | Module-level publication and contribution timeline | `artifacts/active/Figure1_module_timeline_native.pptx` | Active native source; replace legacy `contribution_timeline.png` |
| What Is a Time-Series Agent | Construction hierarchy and Paper Card unit | `artifacts/active/Figure3_construction_native.pptx` | Active native source; replace legacy `Overview.png` |
| LLM-Side Contributions | Temporal representation, alignment, instruction, and reasoning | `artifacts/active/Figure_LLM_side_native_v3.pptx` | Active native source and PNG; replaces the screenshot-style asset |
| General Harness | Seven reusable runtime dimensions | `artifacts/active/Figure4_general_harness_native_v2.pptx` | Active native source; seven dimensions surround the reusable runtime |
| General Time-Series Harness | Temporal objects, operations, evidence, and contracts | `artifacts/active/Figure5_general_ts_harness_native.pptx` | Active native source; separate reusable temporal semantics from task contracts |
| Task-Specific Harness | Four task families under the same seven-module lens | `artifacts/active/Figure6_task_specific_native_v2.pptx` | Active native source and PNG; shared seven-module lens with four task contracts |
| Infrastructure and Benchmarks | Traces, tools, evaluators, and benchmark coverage | `artifacts/active/Figure7_infrastructure_native.pptx` | Active native source and PNG; evaluation layers, episode record, and resources |
| Open Problems and Case Studies | Evidence-backed gaps and representative systems | `artifacts/active/Figure8_open_problems_native.pptx` | Active native source and PNG; ledger gaps, system cases, and Paper Card fields |
| Supporting mechanism examples | AION, MERIT, AnomaMind, and TS-Agent schematics | `artifacts/active/Figure_supporting_workflows_native.pptx` | Seven-slide native source; the main text uses the corresponding exported PNGs |

## Acceptance criteria for every figure

- The source is a native `.pptx` with independent text, fills, lines, arrows, and table/chart objects.
- The composition remains independently editable in PowerPoint without flattening; group/ungroup is verified as a separate desktop interaction.
- Times New Roman is used consistently unless a cited source requires another font.
- Colors encode the four contribution layers consistently: LLM, General Harness, General Time-Series Harness, and Task-Specific Harness.
- The PNG used by LaTeX is exported from the same PPT source.
- The figure has a short caption that states what the figure establishes and cites the source when the visual grammar or an adapted mechanism comes from prior work.
- The figure is checked at paper size for text fit, line crossings, and caption placement.

## Current checkpoint

The active directory now contains one source pair per figure used by `main.tex`. Figure 2 uses `artifacts/active/Figure2_organization_native_v2.pptx`; the LLM-side map uses `artifacts/active/Figure_LLM_side_native_v3.pptx`; Figures 1 and 3--8 use the corresponding final native sources. Superseded revisions remain in `artifacts/archive/previous_attempts/active_revisions_20261002/` so that a later comparison does not accidentally replace an active source.

The visual language has been checked in the 46-page PDF: Times New Roman is consistent, the four semantic layers retain stable colors, the figures remain legible at paper size, and the references begin on a clear page after the conclusion. A PowerPoint desktop check of Figure 8 confirmed that the composition consists of individually selectable native objects; the generated PNG and the LaTeX figure use the same source composition. The direct Group command was not confirmed in the current desktop test copy and remains a separate follow-up check.

The old PNGs remain available as legacy references. They are not overwritten until their replacements pass the same workflow.

## Order of work

1. Figure 2 organization map (completed checkpoint).
2. Overview / construction hierarchy and Paper Card (completed checkpoint).
3. Module-level contribution timeline (completed checkpoint).
4. General Harness seven-dimension map (completed checkpoint).
5. General Time-Series Harness temporal-contract map (completed checkpoint).
6. Task-Specific Harness four-family map (completed).
7. Evaluation and benchmark map (completed).
8. Open-problem and case-study map (completed).
9. LLM-side editable mechanism map (completed).
10. Full-paper visual audit, compile, render, and synchronized push.
