# Figure source status

The current PNGs in `main.tex` are legacy exports. They remain in place until their replacements pass the visual audit.

The previous PPT decks are archived in `artifacts/archive/previous_attempts/` and are not active sources. They were useful for testing layouts, but they do not satisfy the final component-level conversion requirement.

The replacement workflow is:

1. Freeze the target visual composition from the approved reference image.
2. Convert that composition into native PowerPoint text, shapes, tables, connectors, and icons with fixed coordinates.
3. Export the PPT slide to PNG for LaTeX.
4. Compare the PNG and the rendered PDF page against the target image before committing.

Every active figure source will be recorded here only after it passes the component-level and overlay checks.
