# Unified survey figures, 22 October 2026

Approved style from Figure 4/7/9 v2, applied to all 14 conceptual figures. Figure 2 remains the existing statistical plot with its distinct curves and line styles. Manuscript paths now use the PDFs in this directory.

- Selected headings use Comic Sans MS; explanatory text uses Arial.
- Native time-series signals remain black. Navy supports runtime relationships; terracotta highlights rejection, actions or updates.
- Gradients and soft shadows are limited to selected windows, functional objects and execution regions.
- Figure 3 replaces the obsolete seven-function image with the existing native nested-layer layout, matching the caption and current taxonomy. Its General Harness functions match the five-function section. Small native icons are reused from Figure 6.
- Figure 5/6 layouts are preserved. Figure 8 retains task panels. Figure 14 retains its existing dimensional icon assets.
- Figure 1/11/12 typography received local fit corrections after rendering.

Each PPTX has one slide and preserves nested editable groups, native text, signals, arrows and tables. Isolated raster icons retain their pixel interiors. The files passed structural checks, geometry checks and Artifact Tool import; this is not an interactive PowerPoint ungroup test.

`All_Figures_Editorial.pdf` contains Figures 1–15 for inspection. `placement.json` records the compiled manuscript pages. Captions and scientific descriptions are unchanged, and all figures retain top-float placement.

Reproduction: run `unify.py`, then `finish_layout.py`, validate the drafts with the presentation finalizer, export through LibreOffice with the existing project font configuration, and run `integrate.py` before `latexmk -pdf main.tex`. Drafts and intermediate renders live in `.build/` and are excluded from Git. Original files and approved trials are preserved in prior Git history.
