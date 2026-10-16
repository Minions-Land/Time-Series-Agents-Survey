# Complete module-boundary and resource audit

Final integration: 17 October 2026. Source inspection and resource checks began 16 October.

## Coverage and workflow

Three disjoint assignments covered all 138 examined records and all 292 pre-audit module IDs (104 / 88 / 100). Each module has a mechanism-specific decision, original and proposed scope, a rationale, pages inspected, a quotation and a source path. Reviewers read the cited method passages and adjacent task definitions; disputed decisions were checked in additional method/appendix passages. This is a classification and attribution audit, not a replication of reported experiments.

`assignment_*.json` preserve the input snapshot. `shard_*.json` contain the primary reviews and attributed links. `cross_review_2.json`, `cross_review_3.json` and `shard_3_second_review.json` record independent review of changes. `adjudications.json` contains the integrated decisions, including a rejected layer change. No module IDs were invented to preserve counts.

## Final decisions

The first pass proposed 276 keeps, 14 modifications and 2 exclusions. Final adjudication applied:

- **9 scope changes:** Agentic RAG differentiable prompt pool GTS→LLM; TimeSeriesExamAgent exam generation GTS→TSK; TimeOmni TSR-SUITE GTS→LLM; ChatAD instruction construction TSK→LLM; ClimateAgent workflow benchmark GTS→TSK; TS-Agent intent gate GTS→TSK; FinCon analyst aggregation GH→TSK; SIREN case retrieval and skill rehearsal TSK→GH.
- **4 task-label corrections:** TimeSeriesGym includes anomaly detection; the three TSQ modules explicitly carry data-quality assessment.
- **1 retained scope with stronger evidence:** Hierarchical AI-Meteorologist numerical aggregation stays GTS. Independent review separated the actual mean/extrema/sum/circular-mean operation on p.2 from the adjacent forecast-report context policy on p.3.
- **2 excluded modules:** Grid-Agent is retained as a background reference because its evaluated problem is static power-flow violation remediation. Both original module reviews remain archived.

The resulting corpus has **138 examined records, 135 retained records and 290 modules: 47 LLM / 56 GH / 40 GTS / 147 TSK**. The timeline includes 134 dated records and 289 modules, excluding the previously undated MoiraiAgent module. No unresolved scope decisions remain in this audit; the evidence and differing reviewer judgments remain inspectable.

## Official resources

The review found **100 author-attributed resource links across 76 works**. Every link has a source location and availability record. Availability results: 92 reachable, 4 HTTP errors, 3 anonymous-site application shells, 1 failed fetch. The other 62 records explicitly state `not_found_in_source` after checking paper text and PDF hyperlinks. This status describes the inspected sources, not universal nonexistence. The index does not claim that code has been installed or executed. External code was not downloaded.

See [the human-readable index](../../../docs/official-resources.md) and [CSV index](../../official_resources.csv). Schema 2.5 standardizes repository/project/data/model/evaluation resource types, preserves original task labels and makes review status explicit. The maintained CSV generates the public JSON.

## Verification

- Full 292-ID assignment/review coverage and review quotations checked: no missing IDs, duplicates or quotation/page mismatches.
- All 299 active PDF evidence quotations matched their declared pages after correcting a SIREN Appendix K.2 locator to p.17.
- Canonical CSV/JSON, task memberships, schema versions, module/function applicability, appendix markers, source links and plot counts passed read-only checks.
- Reapplying the audit in memory is idempotent and reproduces the maintained rows.
- 11 unit/regression tests passed, including original-alias preservation and rejection of unattributed resource links.
- LaTeX compiled; no undefined citations/references or overfull boxes. Updated trend and appendix pages inspected visually.

Historical audit files are preserved. Use the current schema and maintained CSV for further work; the current temporal-function mapping is `module_function_mapping.json` in this directory.
