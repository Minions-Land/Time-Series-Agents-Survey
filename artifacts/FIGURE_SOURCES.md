# Figure source status

Most PNGs in `main.tex` are legacy exports. Figure 2 now uses the active native source `artifacts/active/Figure2_organization_native_v2.pptx` and its exported PNG `artifacts/active/Figure2_organization_native_v2.png`.

The previous PPT decks are archived in `artifacts/archive/previous_attempts/` and are not active sources. They were useful for testing layouts, but they do not satisfy the final component-level conversion requirement.

The replacement workflow is:

1. Freeze the target visual composition from the approved reference image.
2. Convert that composition into native PowerPoint text, shapes, tables, connectors, and icons with fixed coordinates.
3. Export the PPT slide to PNG for LaTeX.
4. Compare the PNG and the rendered PDF page against the target image before committing.

Figure 2 has passed package integrity, layout, font, and Artifact Tool re-import checks. PowerPoint component-level editing still needs a final desktop check before the whole figure family is treated as complete.

Every additional active figure source will be recorded here only after it passes the component-level and overlay checks.
