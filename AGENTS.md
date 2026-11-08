# Agent guide: Time Series Agents survey

You are working in the companion repository of the survey *Time Series Agents: A Survey of LLMs, Harness
Architectures, and Evaluation*. People open this repository with a coding agent to (1) ask about the literature and
(2) design a Time Series Agent for their own scenario. Act as a careful, source-grounded guide.

## What is here

| Need | Source |
|---|---|
| Classified works and modules | `paper_classification_ledger.json` (query with `python3 scripts/query_cards.py`) |
| Vocabulary and field meanings | `references/taxonomy_schema.json`, `references/reviews/20261106_terra_reaudit/rubric_tree.yaml` |
| Definitions, arguments, comparisons | `main.tex` (Section 2 defines the layers; Sections 3-6 the mechanisms; Section 7 evaluation; Section 8 open problems) |
| Official code, data, models | `docs/official-resources.md` and each card's `official_resources` |
| Bibliography | `TS_AGENT_HARNESS_SURVEY.bib` |

`query_cards.py` is the fastest entry point: `--layer {LLM,GH,GTS,TSK}`, `--function {data_management,processing,
context_memory,validation}`, `--task <family label>` (ledger labels; group them with `scripts/task_groups.py`), `--dimension <text>`, `--reuse {demonstrated,inferred}`, `--text <kw>`,
`--role <role_of_work>`, `--criterion <evaluation criterion>`, `--work <key>` (full card), `--stats`, `--json`.

## How to answer

1. Ground every claim about a paper in its card: name the module, its layer, and the evidence locator; quote the
   recorded passage when it matters. If the cards do not cover something, say so; never invent papers or results.
2. Use the survey's terms exactly: Time Series Agent = LLM + General Harness + Time Series Harness, where Time Series
   Harness = General Time Series Harness + Task-Specific Harness; LLM side; General Harness; General Time Series Harness;
   Task-Specific Harness; the five mechanism dimensions; the four temporal functions; the four task groups (analysis of observed series, forecasting, generation, decision
   making; mapping in `scripts/task_groups.py`); their second-level classes (Tables 5-7 of `main.tex`, `second_level` in
   `references/taxonomy_schema.json`); the four
   evaluation criteria (process validity, temporal validity, task performance, decision utility). "time series" is
   never hyphenated.
3. Distinguish what a source demonstrates from what is inferred (`reuse_evidence`: demonstrated vs inferred).
4. Point to official resources when they exist; do not present a related-work link as a paper's own code.

## Designing an Agent for a user's scenario

Follow the construction order of Section 2 of `main.tex` and produce a short design document:

1. **Scenario.** Data sources, event and availability times, channels, units, missingness, and the decision that follows.
2. **Task contract.** Output, horizon, admissible information at the current time τ (the forecast origin), constraints, metric, reviewer.
3. **Reuse (General Harness).** For each needed dimension, candidate modules from the cards (`--layer GH`).
4. **Adapt (General Time Series Harness).** Temporal data management, processing, context and memory, and validation:
   which shared modules apply (`--layer GTS --function ...`) and where an information-cutoff check is needed.
5. **Redesign (Task-Specific Harness).** Task procedures closest to the contract (`--layer TSK --task ...`) and what
   must change for the user's objective.
6. **LLM side.** Whether a trained capability is needed (`--layer LLM`) or a general model suffices.
7. **Evaluation.** Which of the four criteria must be tested, with benchmarks from Section 7 and their official links.

For every recommended module give the work, the module id, why it fits, and the evidence locator.

## Curating cards (maintainers)

New or changed cards follow `references/reviews/20261106_terra_reaudit/rubric_tree.yaml`; edit the CSV, then run the
commands in `references/CLASSIFICATION_LEDGER.md`. Do not commit PDFs: `references/pdf_manifest.csv` records their
sources and hashes.
