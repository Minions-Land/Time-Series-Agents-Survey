# Table audit for the survey manuscript

The manuscript was reviewed table by table after the restructuring around agent capabilities, task instantiation, evaluation, and resources. The rule was to keep a table only when it defines the framework, records a non-redundant comparison, or gives a compact evaluation contract. Work-level detail belongs in the appendix ledger.

## Tables retained in the main text

| Current table | Purpose | Decision | Visual treatment |
|---|---|---|---|
| `tab:harness-hierarchy` | Shows the hierarchy from General Harness to the temporal module and its two specializations. | Keep. It is the one compact definition of the paper's structure. | Short two-column table immediately after the construction figure. |
| `tab:direct-prior-comparison` | Compares related surveys and runtime frameworks. | Keep. It establishes the paper's position relative to competing surveys. | Long table with concise cells; no work-level rows beyond representative frameworks. |
| `tab:mechanism-decision` | Gives the GH/GTS/TSK judgment rule and reuse test. | Keep. It is necessary for reproducibility of the classification. | Small four-column table. |
| `tab:component-vocab` | Defines the 14 general agent capabilities used throughout the paper. | Keep. It is the vocabulary table for the framework. | Long table grouped into three readable blocks. |
| `tab:gts-invariants` | Defines six temporal design obligations and their task-facing forms. | Keep. It is the central time-series capability table. | Long table; retain the four-column layout because the task column explains instantiation. |
| `tab:invariant-component-matrix` | Crosswalk between general agent capabilities and temporal obligations. | Keep in the main text. It is compact, explanatory, and visualizes the bridge between Sections 2 and 3. | Matrix with bullets/circles; avoid adding more prose rows. |
| `tab:locus-rubric` | States the primary-locus decision rule for systems and benchmarks. | Keep. It is needed to interpret the corpus counts. | Small rubric table. |
| `tab:task-summary` | Summarizes how shared capabilities appear in task families. | Keep as the only task table. It replaces five repetitive task-specific tables. | Compact three-column table with representative examples only. |
| `tab:gts-measurement-status` | Separates established, adjacent, proposed, and open evaluation instruments. | Keep. It makes evidence maturity explicit. | Long table with abbreviated status labels explained in the caption. |
| `tab:gts-obligation-protocol` | Gives the proposed tests and violation predicates for temporal obligations. | Keep. It is the operational evaluation protocol, not a literature inventory. | Long table; retain as a technical reference. |
| `tab:evaluation-locus` | Maps evaluation routes to GH, GTS, and TSK. | Keep. It connects the taxonomy to evaluation. | Long table; place after the protocol table. |
| `tab:benchmark-families` | Explains what benchmark families evaluate and what they cannot establish alone. | Keep. It is the only benchmark comparison table. | Compact three-column table. |

## Appendix table retained

| Current table | Purpose | Decision | Visual treatment |
|---|---|---|---|
| `tab:agent-ledger` | Complete profiles of all 139 reviewed works. | Keep only in the appendix. It is essential for auditability but too dense for the conceptual narrative. | Portrait longtable, reduced to `\scriptsize`, with two columns; no landscape rotation. |

## Tables removed from the main text

| Removed table | Reason |
|---|---|
| General Harness contributions | Repeated the 14-component vocabulary and the appendix ledger. The information is now summarized in prose under “General agent mechanisms.” |
| General Time-Series Harness contributions | Repeated the six-obligation table and the appendix evidence. The information is now summarized in prose under “Shared time-series mechanisms.” |
| Forecasting task-specific table | Repeated representative rows already available in the ledger; its concepts are represented by the forecasting row in `tab:task-summary`. |
| QA and temporal reasoning task-specific table | Repeated the same pattern for another task family; summarized in `tab:task-summary`. |
| Classification task-specific table | Repeated the same pattern for another task family; summarized in `tab:task-summary`. |
| Anomaly and diagnosis task-specific table | Repeated the same pattern for another task family; summarized in `tab:task-summary`. |
| Benchmark, streaming, and deployment task-specific table | Overlapped with the benchmark and evaluation sections; summarized in `tab:task-summary` and `tab:benchmark-families`. |
| Repository stack table | Listed requirements rather than compared alternatives. Converted to a short paragraph in the infrastructure section. |

The result is 12 main-text tables plus one appendix ledger table, down from 19 main-text tables plus the ledger. The current PDF is 47 pages, and the main narrative no longer interrupts the classification argument with repeated paper inventories.
