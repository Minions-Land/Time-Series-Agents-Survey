# Figure source status

The main-text section figures use active native sources. Figure 2 uses `artifacts/active/Figure2_organization_native_v2.pptx`; the LLM-side figure uses `artifacts/active/Figure_LLM_side_native_v3.pptx`; Figures 1, 3, 4, 5, 6, 7, and 8 use their corresponding active PPT sources under `artifacts/active/`; and the supporting AION, MERIT, AnomaMind, and TS-Agent figures use slides in `artifacts/active/Figure_supporting_workflows_native.pptx`. Each active source has a PNG exported from the same presentation.

The previous PPT decks are archived in `artifacts/archive/previous_attempts/` and are not active sources. They were useful for testing layouts, but they do not satisfy the final component-level conversion requirement.

The replacement workflow is:

1. Freeze the target visual composition from the approved reference image.
2. Convert that composition into native PowerPoint text, shapes, tables, connectors, and icons with fixed coordinates.
3. Export the PPT slide to PNG for LaTeX.
4. Compare the PNG and the rendered PDF page against the target image before committing.

Figures 1–8 and the LLM-side map have passed package integrity, layout, font, Artifact Tool re-import, and source-to-PNG export checks. PowerPoint component-level editing still needs a final desktop check before the whole figure family is treated as complete.

Every additional active figure source will be recorded here only after it passes the component-level and overlay checks.
