# Figure and table review (read-only audit)

Scope: `main.tex` and the currently referenced assets under `artifacts/active/`, `artifacts/rsi_figures/`, and `artifacts/active/support_pdf/`. This note does not modify manuscript or figure files. Captions belong in LaTeX; embedded visual text should carry only labels needed to read the diagram (no figure number, caption prose, “Source:”, or explanatory paragraph inside the PPT/PDF).

## Overall findings

- The manuscript has 38 figure environments but only a smaller set of distinct visual roles. Several sections repeat a nearly identical “one figure per subsection” pattern. The paper will read more cleanly if each major section keeps one overview figure and uses method-specific redraws only where the figure carries evidence or explains an executable mechanism.
- Figures 1–3 currently overlap in purpose: Figure 1 is the module timeline, Figure 2 is a survey-position map, and Figure 3 is the construction hierarchy. Figure 2 and Figure 3 should remain distinct only if the former answers “where this survey sits” and the latter answers “how to build an agent”; their captions and surrounding prose must make that difference explicit.
- The paper’s visual unit should be the module-level contribution, while paper-level tables remain supporting evidence. Figure 1’s caption already states this correctly; the same module-level language should be used consistently in the other aggregate figures.
- Current native exports pass pixel equality and contain native PowerPoint objects according to `artifacts/figure_visual_audit_20261002.json`. This verifies export consistency, not whether each figure is visually necessary or semantically non-redundant.

## Main-text figures

### Figure 1 — `fig:contribution-trend`

**Purpose:** Establish the temporal growth of LLM-side, General Harness, General Time-Series Harness, and Task-Specific Harness module contributions. This is the only figure that quantifies corpus evolution and should stay early in the paper.

**Keep:** Yes. It supports the paper’s module-level unit of analysis and explains why a paper can contribute to several curves.

**Required checks:** Keep the y-axis logarithmic only if the caption and prose explain that it is for visibility of early modules. Make the legend and line styles distinguish GH from GTS even when their counts overlap. Avoid implying that curves are mutually exclusive papers. The title/caption text should stay in LaTeX; the graphic itself should contain axis labels, tick labels, and a compact legend only.

### Figure 2 — `fig:position-map`

**Purpose:** Position this survey against the cited time-series-agent surveys.

**Keep:** Conditional. Retain only if it genuinely shows scope relations that Table `tab:direct-prior-comparison` does not already show. If the map simply repeats survey names and checkmarks, remove it and let the table carry the comparison. If retained, make the visual answer one question: how prior survey scopes become inputs to the construction recipe.

**Required checks:** The caption currently cites three surveys but the comparison table includes four. Align the cited set. Do not put “Source:” or caption-like explanatory sentences in the artwork. Use the canonical full survey names in LaTeX or a readable abbreviation plus a key; avoid tiny labels.

### Figure 3 — `fig:survey-organization`

**Purpose:** Give the reader a roadmap from LLM-side contribution and reusable runtime to temporal contracts, task modules, evaluation, and open problems.

**Keep:** Yes, but only as the paper roadmap. It should not also be used as the construction hierarchy or Paper Card schema figure.

**Required checks:** The figure must show section flow, not generic nested boxes. Keep labels short; move explanation to the paragraph immediately before/after it. Caption should state what to follow and what conclusion the map supports. Do not duplicate the Paper Card construction diagram in the appendix.

### Figure 4 — `fig:overview`

**Purpose:** State the conceptual hierarchy: independent LLM side and nested Harness stack, with GH → GTS → TSK specificity.

**Keep:** Yes. This is the central concept figure and should appear in Section 2. It must be visually distinct from Figure 3’s roadmap.

**Required checks:** Show the hierarchy as nested/contained modules, with LLM as the independent branch. Use “Time-Series Harness Module” as the parent label. Do not include “Supporting Components” in the formula or diagram. The formula appears in prose/LaTeX, while the figure should explain the nesting and the deepest-applicable-module rule.

### LLM-side figures — `fig:llm-alignment` and `fig:llm-chatts`

**Purpose:** Explain how numerical temporal data and temporal attributes become language-facing supervision, then connect this to representative LLM-side works such as ChatTS.

**Keep:** At most one overview figure plus one method-specific figure. The current pair risks repeating the same ChatTS pipeline. Keep the overview if it summarizes the LLM-side interface; keep the ChatTS redraw only if the paragraph discusses a specific training/data contribution and the figure is directly cited there.

**Required checks:** Remove any figure-internal title, caption prose, or source line. LaTeX captions carry attribution and interpretation. Formulae for alignment/training belong in the surrounding method paragraph, not as dense text inside the graphic.

### General Harness figures (Section 4)

The current series includes interface (`fig:gh-interface`), memory, tools, control/verification, planning, optimization/evolution, coordination, plus a TS-Agent trace. These are conceptually useful, but one figure per short subsection creates visual repetition.

**Recommended set:** retain one seven-dimension overview (Figure 4/general-harness overview), one representative executable trace, and at most one figure for a mechanism that is otherwise hard to understand (e.g., memory/evolution). Remove or move repeated single-work redraws to the appendix/supplement unless the text extracts a specific design lesson from each.

**Caption rule:** every retained figure should identify the mechanism and its reading direction; attribution goes in LaTeX (`Source:` or `adapted from`) with the cited method immediately after the claim in the paragraph. No method name, source statement, or explanatory caption paragraph should be baked into the artwork.

### General Time-Series Harness figures (Section 5)

The current series mirrors the seven General Harness dimensions: temporal interface, memory, operations, validation, planning, evolution, and coordination.

**Keep:** Keep the section overview plus two or three figures that demonstrate genuinely temporal obligations: point-in-time/as-of semantics and temporal validation are strongest candidates. The rest should be consolidated into a multi-panel figure or represented in text. The figures must visibly differ from their GH counterparts through temporal arguments (as-of time, horizon, frequency, window, provenance, revision, chronological admissibility), rather than merely changing color or title.

**Important semantic check:** A GTS figure should not repeat a generic GH workflow. If it does not show a temporal state/operation/validator that survives a change of downstream task, classify it as GH or remove it from Section 5.

### Task-Specific Harness figures (Section 6)

The section overview plus forecasting, augmentation, anomaly diagnosis, and decision-support examples are justified because each task family has a different output contract.

**Keep:** Retain the four task-family overview and one representative mechanism figure per task family. Ensure each panel shows the task contract: forecast horizon and backtest for forecasting; fidelity/utility for augmentation; detection→diagnosis and evidence for anomaly work; action, risk, cost, and review for decision support.

**Caption rule:** captions should state what task contract is instantiated and what the reader should inspect. Put citations after the named method/work in the body paragraph; use caption citations only for adapted/redrawn source figures.

### Infrastructure and benchmark figures (Section 7)

Current figures cover a benchmark overview, QA trace, infrastructure/runtime, benchmark-selection view, workspace, and (in some versions) ModernTSF. This section needs figures because the paper argues that task scores alone do not evaluate an Agent process.

**Keep:** one infrastructure overview and one benchmark/evaluation matrix or trace. A separate QA trace is useful if QA is explicitly treated as language-facing evidence, but do not repeat the same trace in workspace/infrastructure figures. The figure must make evaluation layers visible: process validity, temporal contract, task outcome, resource behavior, reproducibility, and decision utility.

**ModernTSF:** retain a dedicated visual only if it adds a concrete executable artifact or evaluation record beyond the generic infrastructure figure; otherwise mention it in the benchmark table and prose.

### Open-problem/case-study figures (Section 8)

**Keep:** one open-problem map and, optionally, one compact case-study panel. The map should derive nodes from missing/weak Paper Card fields and connect each gap to a Harness layer. The current caption is appropriate but the body text must explain how to read left-to-right. Avoid turning every case study into a separate decorative diagram.

## Tables

### `tab:direct-prior-comparison` (main text)

**Purpose:** Compare only time-series-agent surveys by organizing object and questions answered. Keep it in the main text. The columns should remain discriminative rather than list every shared survey feature. Use a single noun per column title (e.g., Model, Tasks, Reasoning, Lifecycle, Coverage, Evaluation, Deployment). “Ours” is the only self-name. Verify every checkmark against the cited survey’s actual scope; blank means not explicitly developed, not “the survey never mentions it.”

The introductory paragraph is essential: it explains why these dimensions were selected and how the table supports the contribution-locus view. Keep the paragraph; shorten repeated prose after the table.

### `tab:unified-notation` (main text)

**Purpose:** Fix symbols used in method equations. Keep it, but place it near the first equation block and avoid repeating the same definitions in every subsection. It is not a taxonomy table.

**Formatting:** use one noun for column titles (`Symbol`, `Meaning`, `Layer`, `Use`). Caption in LaTeX only. The lead-in should explain that it is a lookup table for equations.

### `tab:benchmark-families` (main text)

**Purpose:** Map benchmark/infrastructure resources to the part of the Agent contract they can establish. Keep it; this is central to the evaluation chapter. The body text must interpret the table and explain what is missing when a resource covers only task score. Cite resources after their names in prose, with repository links as footnotes.

### `tab:app-harness-hierarchy` (appendix)

**Purpose:** Decode the Paper Card hierarchy and deepest-applicable-layer rule. Keep in the appendix. It is compact and useful for reproducibility; do not repeat a near-identical hierarchy table in the main text.

### `tab:ledger-sample` (appendix)

**Purpose:** Show how a human-readable Paper Card record looks. Keep a short sample in the appendix, ideally 5–8 representative rows. Avoid duplicating the complete 138-work table in the main narrative. The caption should state that source locators and quotations remain in JSON.

### `tab:fine-component-vocab` (appendix)

**Purpose:** Expose the 14 fine-grained coding labels behind the seven-dimension comparison layer. Keep in the appendix because it is needed for auditability but too detailed for the main text. The caption currently repeats “vocabulary used for ledger-level coding”; shorten it and define the relationship to the seven dimensions once in the surrounding prose.

### `tab:agent-ledger` (appendix)

**Purpose:** Exhaustive work-level classification ledger. Keep in the appendix or supplementary material, not the main text. It is a database view, not a central argument. Ensure the prose explicitly says that rows are works while module fields are multi-label; the exclusive plot count uses the deepest applicable module. Check the count (currently 138) against the JSON/CSV before release.

## Caption and embedded-text audit checklist

1. Every retained figure has a LaTeX caption with purpose, reading instruction, and attribution when adapted/redrawn.
2. Artwork contains no `Figure N`, `Caption:`, `Source:`, citation key, or long explanatory paragraph; these belong in LaTeX.
3. A source figure adapted/redrawn is cited in the caption and discussed in the surrounding paragraph.
4. Figure numbering and labels match the final ordering after deletions or consolidation.
5. Tables use one noun per column heading where possible, and the paragraph before/after each table explains the question it answers.
6. Figure files, editable PPTs, and exported PDF/SVG remain linked to the same semantic asset; do not change the LaTeX asset alone.

