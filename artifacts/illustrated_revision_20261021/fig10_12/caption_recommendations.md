# Figure–manuscript alignment

## Figure 10
AnomaMind’s evidence acquisition, construction, interval detection, and refinement procedure \citep{anomamind2026}. Read the upper sequence from retrieved knowledge and diagnostics to an updated interval decision. The highlighted candidate regions show what detection and refinement operate on; the return path updates the accumulated evidence state. The lower left identifies the supporting toolkit, and the lower right separates the detector-training signals from inference-time refinement. The illustrations depict these operations schematically.

The existing main-text paragraph correctly explains the four stages and the distinction between the learned detector and its surrounding Harness. Retain it. No new quantitative or method claims were introduced.

## Figure 11
An evaluation episode and its complementary records, synthesized from AION \citep{aion2026} and TimeSeriesGym \citep{timeseriesgym2025}. The upper sequence connects the task contract, accessible resources, execution, and submitted artifact. The illustrations show examples of resources and outputs. The lower panels separate task performance, artifact validity, and execution history, supporting analysis of prediction quality, implementation errors, and operational failures.

Existing text says “through the challenge and grader”; this figure explicitly shows execution rather than a standalone grader. Recommended text: “Figure~\ref{fig:evaluation-stack} follows an episode from its task contract and accessible resources through execution to the submitted artifact, and separates the three records needed to interpret its outcome.” Continue with existing weak predictor/failed tool/misaligned input examples.

## Figure 12
Executable evaluation in TimeSeriesGym \citep{timeseriesgym2025}. Challenge resources and instructions enter an execution environment in which an Agent produces code, models, or other outputs. A challenge-specific grader checks the submitted artifact and its task metrics. The shared challenge contract enables comparison across Agents; the illustrated workspace shows example resource and artifact types.

Existing benchmark paragraph fits this illustration. No benchmark counts or claims changed.

# Component editability

Each figure contains native Times New Roman labels and connectors, with independently replaceable original-image crops. All content is grouped semantically and enclosed in one top-level figure group. Raster illustrations preserve generated RGB details; inner pixels are not native drawing paths. Group/ungroup separates image objects, labels, connectors, and containers. Structural checks passed; interactive PowerPoint UI ungroup tests have not been performed by this worker.

# Verification

Three editppt single-page runs were claimed, built, validated, recorded, and finalized. Subsequent grouping and native shadows were verified with Artifact Tool finalization (package pass, geometry finding count 0, import pass). Final PDFs were rendered and inspected individually. PDF font inspection confirmed TimesNewRomanPSMT and TimesNewRomanPS-BoldMT. Scientific content checked against main.tex AnomaMind method/equations and evaluation/TimeSeriesGym paragraphs. Charts inside illustrations are schematic and contain no measured numerical results.
