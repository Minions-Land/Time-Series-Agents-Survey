# RSI editable PPT versus the figures used by the paper

## Scope

I checked the editable RSI-derived deck
`artifacts/active/TimeSeriesAgent_Figures_RSI_template_working_copy_grouped.pptx`, its five-page export
`..._grouped.pdf`, the current figure references in `main.tex`, and the eight one-page native PDFs currently included by `main.tex`.
No manuscript or figure file was modified in this check.

## Evidence

| Item | Verified result |
|---|---|
| RSI-derived editable source | 5 slides; exported page size 1312.5 x 1006.5 pt (aspect ratio about 1.305). Each slide contains one top-level `p:grpSp`, so the source is natively groupable/ungroupable. The slide XML contains 46/69/28/140/58 shapes on slides 1--5; slides 1 and 5 also contain 6 and 8 native picture objects. |
| RSI deck slide subjects | (1) Time-Series Agent construction; (2) Survey organization; (3) Contribution layers; (4) Research routes; (5) four task contracts. |
| Current `main.tex` sources | `main.tex` includes exactly these eight figure PDFs: `Figure2_organization_native_v2.pdf`, `Figure3_construction_native.pdf`, `Figure4_general_harness_native_v2.pdf`, `Figure5_general_ts_harness_native.pdf`, `Figure6_task_specific_native_v2.pdf`, `Figure7_infrastructure_native.pdf`, `Figure8_open_problems_native.pdf`, and `Figure_LLM_side_native_v3.pdf`. It does not reference the grouped RSI deck, its PDF export, or the v6 PPTX. |
| Current native figure format | Each of the eight files is a one-page 1199.99 x 675.014 pt PDF (aspect ratio about 1.778, 16:9), which differs from the five-slide RSI deck export. |
| Current compiled PDF | `main.pdf` contains the native-figure titles such as “Organization of the survey”, “How a Time-Series Agent is constructed”, “Seven dimensions of a General Harness”, and “Infrastructure and benchmark coverage”. It does not contain the unique grouped-deck titles “Modules compose across tasks”, “Contribution layers in Time-Series Agents”, or “Research routes in Time-Series Agent systems”. |

## Slide-to-figure correspondence

The grouped deck and the native PDFs share concepts and some labels, but they are not the same exported pages:

- Deck slide 2 is conceptually closest to `Figure2_organization_native_v2.pdf`, but the section descriptions, title, paper-card footer, and layout differ.
- Deck slides 1 and 3 are conceptually closest to `Figure3_construction_native.pdf`, but the deck uses a workflow/contribution-layer composition while the PDF uses the nested runtime plus paper-card composition.
- Deck slide 5 is conceptually closest to `Figure6_task_specific_native_v2.pdf`; both expose the four task contracts, but the deck uses four illustrated panels and the PDF uses a seven-module lens with task-contract columns.
- Deck slide 4 is a research-route/timeline figure. No current `Figure2`--`Figure8` or LLM-side PDF has that title or layout; the current paper instead uses the separate module-level timeline as `Figure1_module_timeline_native.pdf`.

The visual renders confirm this distinction: the five deck pages are 4:3-like, with the original RSI-style composition and native grouped objects; the eight included PDFs are 16:9 native figures with different text blocks and geometry. Therefore the current PDF figures are RSI-inspired/adapted native redraws, not direct exports of the five-page grouped deck.

## Conclusion

The answer to “were the previously extracted RSI PPT figures modified and placed into the paper?” is **not yet, in the strict source-traceability sense**. The editable RSI-derived deck exists and is groupable, but it is currently an unreferenced artifact. The paper uses a separate set of eight native PDF figures that follow the same visual language and reuse related concepts. To make the grouped RSI deck the canonical source, the next step is to choose which of its five slides should replace or supply the corresponding manuscript figures, export those selected slides to PDF/SVG, and update `main.tex` and the figure inventory together.
