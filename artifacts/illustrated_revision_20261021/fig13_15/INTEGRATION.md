# Figures 13–15: illustrated revision

The editable PPTs each contain one slide. Each scientific vignette is an independent original-pixel crop of a generated asset sheet. Labels, connectors and panel outlines are native PowerPoint objects. Semantic modules and the whole figure are grouped. Ungrouping exposes these components; internal pixels of an illustration are not native vector shapes. All final PDFs embed Times New Roman. The generated mini-plots are explanatory schematics, not experimental measurements.

The editppt workflow was completed separately for all three source PDFs: prepare, local claim, generated-sheet import, exact cropping, manifest build, validation, record and finalize. Final PPTs then receive semantic groups and native subtle shadows, followed by Artifact Tool validation. All three passed package integrity, geometry and import checks. Final PDF exports were individually visually inspected. No interactive PowerPoint UI ungroup test was performed by this worker.

## Figure 13

Files: `pptx/Figure13_TSAgent_illustrated.pptx`, `pdf/Figure13_TSAgent_illustrated.pdf`.

Suggested caption:

> An evidence-conditioned analytical workflow in TS-Agent \citep{tsagent2025}. Read from the question and observed series to numerical tools, evidence review, and the grounded response. The return path requests another operation or revises the analysis. The lower record links tool inputs and outputs to source provenance and the final response. The illustrated plots and source documents depict the information handled by each module. Adapted from the method's analytical workflow.

The existing main-text introduction of the figure remains consistent. The imagery of documents should be understood as illustrative evidence objects, not a claim that this method requires ocean data or satellite imagery. If preferred, keep the caption's phrase "illustrated plots and source documents" to make the role clear.

## Figure 14

Files: `pptx/Figure14_TIMECLAW_illustrated.pptx`, `pdf/Figure14_TIMECLAW_illustrated.pdf`.

Suggested caption:

> TIMECLAW's numerical workspace, temporal tools, multimodal memory, and capability evolution \citep{timeclaw2026harness}. The upper path keeps series, windows, and metadata addressable while tools operate on them and retrieve analytical context. The lower path extracts reusable procedures from execution traces, tests candidates on held-out similar tasks, and registers accepted tools with invocation descriptions. This path returns new capabilities to the runtime. Adapted from the system's runtime and tool-promotion mechanisms.

This is TIMECLAW (`timeclaw2026harness`), not the distinct TimeClaw exploratory-learning paper. The lower path is supported by the General Harness subsection "Optimization and Evolution" in current main.tex. In the immediate figure-introduction paragraph, add a sentence such as: "The lower path shows how recurrent executed procedures become candidate tools, which are evaluated before registration."

## Figure 15

Files: `pptx/Figure15_Open_Problems_illustrated.pptx`, `pdf/Figure15_Open_Problems_illustrated.pdf`.

Replace "Read each row" in main text with "Read the five panels". The previous five-row table is now a five-panel experimental atlas.

Suggested caption:

> Controlled comparisons for reusable Time-Series Agents. The five panels pair an open problem with a testable contrast: model judgment and tool use, old and revised evidence, seen and held-out settings, supporting evidence and its removal, and forecast quality and downstream action utility. The illustrations show the objects and interventions involved; the labels identify the outcomes to examine. Matched backbone and resource budgets isolate the factor under study. This agenda synthesizes temporal interfaces \citep{chatts2025}, evolving execution \citep{timeclaw2026harness,timesageev2026}, controlled evidence \citep{drcik2026}, and decision workflows \citep{fincon2024}.
