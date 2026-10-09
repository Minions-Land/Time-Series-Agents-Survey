# Figure integration audit (2026-10-09)

Scope: read-only audit of `main.tex` and the active figure assets. The question is whether Figures 1--8 (plus the LLM-side and supporting figures) are actually wired into the LaTeX source, whether their files exist, and whether the source/caption choices are consistent with the native editable PPT workflow.

## Result at a glance

- **No broken `includegraphics` path was found.** Every one of the 37 `\includegraphics` targets in `main.tex` resolves to an existing file (with the extension written in the source).
- The eight main synthesis figures and the LLM-side figure are wired to active native PDF exports. Their matching PPTX, PNG, and grouped PPTX files exist under `artifacts/active/`.
- The main source still mixes the new active figures with older `artifacts/rsi_figures/*.png` assets and the supporting workflow exports. This is a consistency issue for the visual refresh, even though it is not a missing-file error.
- The grouped PDF exports are not consistently the files used by LaTeX. In particular, `Figure7_infrastructure_native.pdf` is included, while a distinct `grouped_pdf/Figure7_infrastructure_native_grouped.pdf` exists. The grouped and ungrouped Figure 7 PDFs have different sizes and checksums, so this choice should be made deliberately.
- The current figure captions are clear enough to compile, but most author-synthesized Figures 1--8 have no bibliographic citation in the caption. Source-derived support figures do cite the originating work. If the paper requires every figure to carry a source citation, the synthesis captions need explicit ledger/review citations (or an explicit “author synthesis from …” statement).
- The existing visual-QA note is stale: `artifacts/VISUAL_QA_20261002.md` reports a 49-page PDF, whereas the current root `main.pdf` is 65 pages (created 2026-10-07). The source-to-PNG audit JSON also predates the current main PDF and should not be treated as a current rendered-PDF audit.

## Primary figure wiring

| Paper figure | LaTeX location | Included asset | File status | Editable source(s) | Audit note |
|---|---:|---|---|---|---|
| Figure 1, contribution timeline | `main.tex:193--198` | `artifacts/active/Figure1_module_timeline_native.pdf` | present | `Figure1_module_timeline_native.pptx`, `_grouped.pptx` | Active native export; caption explains module-level counting and log axis. |
| Figure 2, organization map | `main.tex:262--267` | `artifacts/active/Figure2_organization_native_v2.pdf` | present | `Figure2_organization_native_v2.pptx`, `_grouped.pptx` | The grouped PDF counterpart exists under `artifacts/active/grouped_pdf/`; LaTeX currently uses the active root PDF. |
| Figure 3, construction hierarchy | `main.tex:271--276` | `artifacts/active/Figure3_construction_native.pdf` | present | `Figure3_construction_native.pptx`, `_grouped.pptx` | Also reused for the Paper Card schema at `main.tex:1160--1165`. |
| Figure 4, General Harness | `main.tex:432--434` | `artifacts/active/Figure4_general_harness_native_v2.pdf` | present | `Figure4_general_harness_native_v2.pptx`, `_grouped.pptx` | Active native export; no external source citation in caption. |
| Figure 5, General Time-Series Harness | `main.tex:644--646` | `artifacts/active/Figure5_general_ts_harness_native.pdf` | present | `Figure5_general_ts_harness_native.pptx`, `_grouped.pptx` | Active native export; no external source citation in caption. |
| Figure 6, Task-Specific Harness | `main.tex:814--816` | `artifacts/active/Figure6_task_specific_native_v2.pdf` | present | `Figure6_task_specific_native_v2.pptx`, `_grouped.pptx` | Active native export; no external source citation in caption. |
| Figure 7, infrastructure/evaluation | `main.tex:955--960` | `artifacts/active/Figure7_infrastructure_native.pdf` | present | `Figure7_infrastructure_native.pptx`, `_grouped.pptx`, `Figure7_infrastructure_rsi_style_grouped.pptx` | A distinct grouped PDF exists and differs from the included PDF; choose one canonical visual. |
| Figure 8, open problems/cases | `main.tex:1129--1134` | `artifacts/active/Figure8_open_problems_native.pdf` | present | `Figure8_open_problems_native.pptx`, `_grouped.pptx` | Active native export; no external source citation in caption. |
| LLM-side figure | `main.tex:378--380` | `artifacts/active/Figure_LLM_side_native_v3.pdf` | present | `Figure_LLM_side_native_v3.pptx`, `_grouped.pptx` | Caption cites ChatTS and identifies the adaptation. |

The active figures have one page each and a common 1200x675 pt slide geometry. The native object audit recorded editable shape objects for Figures 1--8 and the LLM-side figure; the supporting workflow deck is a seven-slide editable deck.

## Other figure assets still used by the manuscript

These paths all resolve, but they are not the primary active native PDF set:

- `artifacts/rsi_figures/survey_organization.png` (`main.tex:202--207`, Figure 2 in the compiled paper).
- `artifacts/rsi_figures/gts_landscape.png` (`main.tex:653--655` and `690--692`).
- `artifacts/rsi_figures/research_routes.png` (`main.tex:772--774`, `892--894`, and `1067--1071`).
- `artifacts/Overview.png` (`main.tex:823--825`).
- Reused support exports: `support_pdf/tsagent_trace_native.pdf`, `timeclaw_runtime_native.pdf`, `anomamind_workflow_native.pdf`, `aion_principles_native.pdf`, and `timeseriesgym_benchmark_native.pdf`, plus the PNG support figures for TS-Agent, AION, MERIT, and AnomaMind.

The old RSI PNGs are especially visible in the compiled PDF because they coexist with the new native figures. If the visual system is meant to be uniform, replace these four RSI PNG usages with native PPT-derived exports or explicitly retain them as source-derived examples and label them consistently.

## Caption and in-text citation audit

Source-derived support figures generally include an explicit source, for example `\citep{chatts2025}`, `\citet{tsagent2025}`, `\citet{aion2026}`, `\citet{merit2025}`, `\citet{anomamind2026}`, `\citep{timeclaw2026explore}`, and `\citep{timeseriesgym2025}`.

The following synthesis captions currently do not carry a citation or source note:

- Figure 1 (`fig:contribution-trend`): counts come from the ledger and the caption explains the unit, but there is no ledger citation or appendix cross-reference in the caption itself.
- Figure 2 organization (`fig:survey-organization`): describes the paper's own structure; the caption names the visual grammar but has no citation to the comparison surveys.
- Figure 3 construction (`fig:overview`): author synthesis with no citation in the caption.
- Figure 4 General Harness (`fig:general-harness-seven-dimensions`): author synthesis; the surrounding paragraph cites the survey literature, but the caption does not.
- Figure 5 General Time-Series Harness (`fig:gts-landscape`): author synthesis; the surrounding text cites temporal-agent surveys, but the caption does not.
- Figure 6 Task-Specific Harness (`fig:task-specific-harness`): author synthesis; no caption citation.
- Figure 7 evaluation stack (`fig:evaluation-stack`): author synthesis; the benchmark chapter cites individual resources later, but the caption has no source note.
- Figure 8 open-problem map (`fig:open-problems-cases`): author synthesis from the ledger; no caption citation or appendix cross-reference.

This is not a BibTeX resolution problem: the manuscript compiles without undefined citation/reference warnings, and all cited keys used in the visible figure captions resolve. It is a provenance/presentation choice. A consistent solution is to add a short “author synthesis from the Paper Card ledger and [survey keys]” clause to each synthesis caption, while keeping the detailed purpose/interpretation paragraph in the body.

The figure labels are unique. Only eight explicit `\ref` calls appear in the source, so most figures are introduced by a nearby prose paragraph but are never cross-referenced as `Fig.~\ref{...}`. For reviewer readability, add a first in-text reference when each figure is discussed, especially for Figures 1--8 and the evaluation figures.

## Build and bookkeeping observations

- `main.log` contains no missing-file or undefined-reference warning for the current build. It does contain underfull-box messages in the notation/benchmark/appendix areas; these are layout issues rather than figure integration failures.
- `artifacts/FIGURE_SOURCES.md` and `artifacts/figure_visual_audit_20261002.json` document the native source-to-PNG checks and report `latex_reference: true` for Figures 1--8 and the LLM-side map. Those checks validate asset wiring and native-object conversion, but not the current 65-page rendered PDF.
- `artifacts/VISUAL_QA_20261002.md` says “Page count: 49” and lists old page ranges, while the current root PDF has 65 pages. Regenerate this QA record after the next final LaTeX build.
- The repository contains many intermediate/working PPTs in `artifacts/active/` (including the RSI working-copy deck). They do not break LaTeX, but a canonical-source manifest would prevent accidental edits to a non-active copy.

## Recommended next actions

1. Pick one canonical PDF for each main figure. If the grouped PDF is the final export, change `main.tex` to the grouped path (or overwrite the active root PDF from that source) and record the choice in `FIGURE_SOURCES.md`.
2. Decide whether old RSI PNGs are intentional source-derived examples. If not, replace `survey_organization.png`, `gts_landscape.png`, `research_routes.png`, and `Overview.png` with active native exports.
3. Add provenance clauses/citations to the eight synthesis captions and add nearby `Fig.~\ref{...}` references in the prose.
4. Rebuild and regenerate the visual-QA record so its page count and inspected page ranges match the current `main.pdf`; then verify the remote heads after the final synchronization.

