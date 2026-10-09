# Figure source status

The main-text section figures use active native sources. Figures 2, 3, and 6 now use direct single-page PDF exports from the grouped RSI-derived deck `artifacts/active/TimeSeriesAgent_Figures_RSI_template_working_copy_grouped.pptx`; the page mapping is recorded in `artifacts/active/RSI_PPT_PAPER_MAPPING.md`. The LLM-side figure uses `artifacts/active/Figure_LLM_side_native_v3.pptx`; Figures 1, 4, 5, 7, and 8 use their corresponding active grouped PPT sources under `artifacts/active/`; and the supporting AION, MERIT, AnomaMind, and TS-Agent figures use slides in `artifacts/active/Figure_supporting_workflows_native.pptx`. Each active source has a PDF export used by LaTeX and an editable PowerPoint source.

The previous 16:9 native redraws for Figures 2, 3, and 6 remain in `artifacts/active/` as historical alternatives; they are no longer the active LaTeX sources. The RSI-derived deck is retained as the canonical editable source for the three mapped figures and preserves native groups for later group/ungroup editing.

The replacement workflow is:

1. Freeze the target visual composition from the approved reference image.
2. Convert that composition into native PowerPoint text, shapes, tables, connectors, and icons with fixed coordinates.
3. Export the PPT slide to PNG for LaTeX.
4. Compare the PNG and the rendered PDF page against the target image before committing.

Figures 1–8 and the LLM-side map have passed package integrity, layout, font, Artifact Tool re-import, and source-to-PNG export checks. The supporting AION, MERIT, AnomaMind, and TS-Agent figures pass the same decoded-pixel comparison against their slides in the seven-slide native deck. The complete 13-pair result is recorded in [`FIGURE_OVERLAY_QA_20261002.md`](FIGURE_OVERLAY_QA_20261002.md) and [`figure_visual_audit_20261002.json`](figure_visual_audit_20261002.json). A PowerPoint desktop inspection of the Figure 8 source confirmed independent selection of the native text, fills, lines, and connectors. The active directory is restricted to the final source pair for each figure; earlier revisions are retained under `artifacts/archive/previous_attempts/active_revisions_20261002/`.

Every additional active figure source will be recorded here only after it passes the component-level and overlay checks.
