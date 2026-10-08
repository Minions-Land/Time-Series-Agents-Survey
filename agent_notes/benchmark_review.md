# Benchmark and infrastructure review (read-only)

Scope: Section 7 (`Infrastructure and Benchmarks for Time-Series Agents`) and the immediately related ModernTSF/TimeClaw/AION claims. This review does not modify `main.tex`.

## Evidence checked

Local source PDFs were available for `timeseriesgym2025`, `temporalbench2026`, `tfrbench2026`, `tracebench2026`, `tsqbench2026`, `timeclaw2026harness`, `aion2026`, and `tsagent2025` under `references/pdfs/`. Bibliographic identities are present in `TS_AGENT_HARNESS_SURVEY.bib`. ModernTSF has no local paper PDF or BibTeX record; its only local evidence is `references/repository-resources.csv` and the repository footnote in the manuscript.

## Claim-level checks

| Manuscript item | Result | Evidence / correction needed |
|---|---|---|
| AION represents a task as task file, workspace, validation interface | Supported | AION PDF, abstract and Sec. 1 explicitly define the three-component tuple and describe task files, workspaces, and validation interfaces. The equation in Sec. 7 is consistent with that description. |
| AION has temporal grounding, knowledge-grounded reasoning, and reliability mechanisms | Supported | AION abstract explicitly lists these three design principles and gives layered review/post-experiment analysis as reliability mechanisms. |
| Evaluation should include process, temporal contract, task outcome, resource behavior | Survey synthesis | This is the survey's proposed evaluation decomposition, not a result claimed by one benchmark. Keep it as the organizing proposal and cite the benchmark papers where each layer is instantiated. |
| TemporalBench has four information/task settings and four domains | Supported | Local PDF abstract, p. 1: historical structure interpretation, context-free forecasting, contextual temporal reasoning, event-conditioned prediction; retail, healthcare, energy, physical systems. The table's wording is accurate. |
| TFRBench has ten datasets across five domains and reasoning traces with iterative verification | Supported | Local PDF abstract, p. 1 explicitly states ten datasets/five domains and the multi-agent iterative verification protocol. |
| TraceBench controls root-cause attribution with simulated dynamical systems | Supported | Local PDF abstract, p. 1: three interpretable mechanical systems, controlled interventions, four agents, trajectories and leaderboard. The table's “controlled diagnostic environments” description is accurate. |
| TSAQA / MMTS-Bench cover temporal QA and multimodal grounding | Partly supported / verify exact scope | `tsaqa2026` and `mmtsbench2026` PDFs are not both in `references/pdfs/` under the expected keys in the current checkout. The broad role is plausible from the cited identities, but the exact “large ... collections” and task list should be checked against the PDFs before making a strong quantitative claim. |
| TimeSeriesGym covers diverse ML-engineering challenges and evaluates files, code, and models with numeric and LLM-based grading | Supported | Local PDF abstract, p. 1 states diverse domains/tasks, isolated and combined skills, submission files/code/models, and precise numeric plus LLM-based evaluation. The manuscript's row is well aligned. |
| TSQBench evaluates time-series data quality dimensions and grounded quantitative comparison | Supported | Local `tsqbench2026.pdf`, abstract, p. 1 describes dimension identification, dimension-wise comparison, eleven real-world datasets, analytical tools, and TSQAGENT. The table should call the resource `TSQBench` while distinguishing the associated system `TSQAGENT`; current wording is acceptable. |
| FutureSim provides replayable world-event evaluation under changing information | Bibliographically supported; benchmark-role wording needs source check | Bib entry is present and the cited title supports replaying world events, but no local PDF was found in `references/pdfs/` during this pass. Keep the claim at title/metadata strength until the paper is locally checked. |
| WorldReasoner evaluates prospective-event forecasting with valid reasoning and temporal availability | Bibliographically supported; claim should be source-checked | Bib entry is present; no local PDF was found in this pass. The wording is plausible from the title, but “makes temporal leakage and trace quality explicit targets” needs the paper's methods/abstract as evidence. |
| TimeClaw supplies executable temporal tools, experience-driven capability evolution, and episodic multimodal memory | Supported | Local `timeclaw2026harness.pdf`, abstract, p. 1 explicitly lists these three components and contextualized temporal reasoning. `timeclaw2026explore` is a separate Bib entry for the exploratory execution learning work; do not merge their claims without checking which version is intended. |
| ModernTSF supplies callable model/dataset interfaces, evidence, budgets, artifacts, and recoverable execution | Repository evidence only | `references/repository-resources.csv` records README-level evidence: 178 model/method entries, 80 dataset presets, reproducible/auditable execution. There is no BibTeX key or local paper PDF. Keep the repository footnote and label this as infrastructure/repository evidence, rather than a paper result. |

## Logic findings

1. The opening claim says evaluation has “three levels” and then defines a four-coordinate vector `(GH, GTS, TSK, resource)`. This is a terminology inconsistency. Either call the vector four dimensions, or group resource behavior under the process/evaluation record and keep three levels. The current prose should be reconciled before publication.
2. The benchmark gap statement (“absence of a widely adopted cross-task suite”) is a synthesis claim. It is reasonable given the table, but should be framed as the survey's coverage finding and supported by the complementary coverage discussion, rather than implying a formal exhaustive census.
3. The existing benchmark table is strongest when it states what each resource can establish. It should avoid implying that a benchmark covers an entire Harness layer merely because it reports a task score. The current prose mostly follows this rule.
4. `timeseriesgym_benchmark_native.pdf` is included twice in Section 7 (benchmark landscape and benchmark selection). This may be intentional as a visual anchor, but the second use repeats the same asset and source. Consider using a distinct selection schematic or retain only one occurrence to avoid visual redundancy.
5. `ModernTSF` is used in Section 7, Section 8, and the ledger despite having no production BibTeX entry. The repository footnote is appropriate for a code/infrastructure resource; do not cite it as if it were a peer-reviewed paper. The ledger row should keep its source type as repository/footnote.
6. Figure captions cite their source, but the explanatory text immediately before/after each figure should state what conclusion the figure supports. The benchmark-landscape figure currently has a short caption and one sentence; the table's “What the benchmark table answers” paragraph is clearer and can serve as the model for the other figures.
7. The section's construction logic is coherent: task contract → episode record → coverage matrix → resource landscape → infrastructure gap → benchmark selection. This directly supports the survey's practical goal of choosing an evaluation stack for a new Time-Series Agent.

## Suggested validation queue (no edits made)

- Acquire or inspect local PDFs for `tsaqa2026`, `mmtsbench2026`, `futuresim2026`, and `worldreasoner2026`; confirm every quantitative/table-level phrase against the abstract or methods section.
- Decide whether the evaluation hierarchy is three levels plus resource metadata, or four evaluation coordinates, then use one terminology consistently in the paragraph, figure caption, and equation.
- Preserve the ModernTSF repository footnote and explicitly mark repository-derived fields in the Paper Card/ledger.
- Recheck the duplicate TimeSeriesGym figure usage during the next visual pass.
