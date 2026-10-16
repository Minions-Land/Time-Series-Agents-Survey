# Introduction comparison and a conversational module library

Date: 2026-10-16. This is a discussion report, not a manuscript revision or a deployed service.

## Reading coverage

The duplicated Preprints link denotes one source. Read Introduction in six reference surveys and three direct competitors. For From Prompts to Agents, SSRN PDF retrieval returned HTTP 403; only the official repository's motivation and taxonomy were verified. Do not present its paragraph sequence as full-text verified.

| Source | Verified location/version | Introduction argument | Useful writing principle |
|---|---|---|---|
| Recursive Self-Improvement in AI: A Survey | Preprints 202609.2680 v1, HTML Section 1 | Model solving and researcher-led improvement converge; infrastructure design and repair have different objectives; ask what improves, what evidence supports it, and what sustains the loop; contributions follow these questions. | Derive the organizing questions from the practical objective. |
| Co-Evolution in Agentic Systems: Toward Self-Directed Evolution Beyond Human Design | arXiv:2608.10299 v1, Introduction, pp. 1–2 | Post-deployment improvement leads from one evolving entity to adaptive counterparts; expanding evolutionary freedom motivates agent–agent, agent–environment and meta co-evolution. | A classification axis should explain a consequential change in system assumptions. |
| Graph Engineering in the Era of LLM Agents: From Individual Intelligence to System Intelligence | arXiv:2608.21156 v2, Section 1, pp. 4–6 | Model capabilities lead to an agent runtime; interdependent tasks motivate system organization; task organization, coordination and runtime state become the engineering objects. | Explain the concrete bottleneck before naming an engineering framework. |
| Graphs Meet AI Agents: Taxonomy, Progress, and Future Opportunities | arXiv:2506.18019 v3, Section I, pp. 1–3 | Planning, tool execution, memory and collaboration create information-organization problems; graphs offer a common structural mechanism; review graphs for agents and agents for graphs. | Derive module categories from the problems they solve. |
| Self-Improvements in Modern Agentic Systems: A Survey | arXiv:2607.13104, Section 1 (printed pp. 5–7 in inspected PDF) | Historical self-improvement connects to language-native modification; foundation-model and scaffold updates are distinguished by modification target and learning signals. | Explain why model-side and runtime-side contributions require separate treatment. |
| Self-Improving Agents in the Era of Experience: A Survey of Self- to Meta-Evolution | Author-repository PDF, Section 1, pp. 4–5; official README identifies OpenReview IUltZSgLMm | Deployment experience must persist and affect later behavior; the harness provides experience infrastructure; runtime adaptation, parameter consolidation and meta-evolution follow. | Define the system object and trace how useful information flows through it. |
| LLM Agents for Time-Series: A Survey | Local primary-source PDF, Section 1, pp. 1–2; arXiv:2608.26226 | Expert-heavy pipelines motivate adaptive tool-augmented systems; task-specific architecture, tools and memory motivate a problem-driven taxonomy. | Task-oriented construction guidance is already present in a close competitor. |
| A Survey of Reasoning and Agentic Systems in Time Series with Large Language Models | Local TMLR PDF, Section 1, pp. 5–7; arXiv:2509.11575 | Prediction expands to explanation, counterfactual reasoning and action; reasoning topology changes evidence access and verification; topology × objective plus attribute tags organize the literature. | A concrete example can explain why a taxonomy changes system behavior. |
| LLM-Based Agents for Forecasting and Prediction: Methods, Training, Evaluation, and Applications | Local primary-source PDF, Section 1, pp. 2–3; arXiv:2608.23058 | Forecasts inform decisions; language supplies semantic evidence and control; architecture choices are judged through scored outcomes, information availability, cost and deployment constraints. | Tie the organizing question to evaluation and resource choices. |
| From Prompts to Agents: A Comprehensive Survey of LLM-Driven Time Series Analysis | Official CoderPowerBeyond/Agent-Prompt-TS-Survey README only | Verified motivation: connect representation, model adaptation, workflow autonomy and analytical task; distinguish frozen prompting from backbone updates; evaluate workflow capabilities. | This competitor also uses a unified design space and a maintained resource repository. Full Introduction remains unverified. |

Sources: https://www.preprints.org/manuscript/202609.2680 ; https://arxiv.org/abs/2608.10299 ; https://arxiv.org/abs/2608.21156 ; https://arxiv.org/abs/2506.18019 ; https://arxiv.org/abs/2607.13104 ; https://github.com/FrontisAI/Awesome-Self-Improving-Agents/blob/main/Self_Improving_Agents.pdf ; https://arxiv.org/abs/2608.26226 ; https://arxiv.org/abs/2509.11575 ; https://arxiv.org/abs/2608.23058 ; https://github.com/CoderPowerBeyond/Agent-Prompt-TS-Survey .

## Implication for our Introduction

The distinctive question is which concrete modules a developer can reuse, what temporal/task assumptions constrain that reuse, and how to implement and evaluate their composition. Task orientation, a taxonomy, a JSON catalog, or a GitHub list alone do not establish that distinction.

Suggested paragraph progression:
1. Temporal analysis informs actions; intermediate findings also determine the next analytical operation.
2. Adaptive workflows require choosing evidence, tools, revisions and stopping decisions under temporal constraints.
3. General runtime capabilities must be combined with reusable temporal functions and task-bound procedures.
4. Useful mechanisms are distributed across agent systems, reasoning models, adaptive pipelines and evaluation resources; paper names alone cannot recover these mechanisms.
5. Explain module-level analysis and reuse scope with one concrete example, then connect construction to repositories and benchmarks.
6. Position against the verified competitor emphases; state contributions in framework, comparative synthesis, evaluation guidance and evidence-linked module curation.

Candidate contribution wording, grounded in existing module records:

> We curate an evidence-linked module library that connects agent systems with time-series reasoning methods and adaptive workflows. For each module, we record its function, scope of reuse, task assumptions, and supporting passages, enabling readers to compare concrete mechanisms across differently framed research contributions. The accompanying Paper Cards connect this synthesis to bibliographic records and evaluation evidence.

An interactive service or tested method execution should be claimed after it is implemented and evaluated.

## Non-agent framing: evidence and a discovered label problem

ARTIST (Adaptive Time Series Reasoning via Segment Selection, arXiv:2602.18645v3) is a concrete example. Its abstract and Introduction frame it as a time-series reasoning approach. Section 3 (PDF p. 4) describes a controller selecting temporal segments and termination, with a reasoner operating on accumulated segments. The ledger already separates `artist2026:joint-policy` (LLM training) from `artist2026:segment-selection` (task-specific QA procedure). This supports method-level inclusion beyond papers branded as agent systems. It does not establish that the procedure transfers across tasks without adaptation.

The reviewed ledger has 12 records with `claimed_as_agent=false`, but that count is not a validated population of non-agent Harness methods:
- TimeXL's Section 3.3 (PDF p. 5) explicitly introduces three interacting LLM agents. Its false flag conflicts with the primary text.
- CALM refers to LLM reasoning agents in its Introduction; its title being a framework does not justify a blanket absence claim. Its documented event-time buffering (p. 6), artifact reload (p. 8), and anomaly curation (p. 8) remain concrete modules worth comparing.
- Several false records are LLM training works; FutureSim is an agent evaluation resource. These are different roles.

Recommended replacement audit fields: system-level self-description, component-level agent terminology, method/resource role, evidence locator and quotation, and reviewer classification. Record unfamiliar or ambiguous cases explicitly. Maintain the CSV as canonical and regenerate JSON; do not hand-edit only the JSON.

Separate author-claimed novelty, implemented components, adopted dependencies, and reviewer-proposed reuse. This prevents counting an inherited tool as a new contribution or presenting a proposed adapter as an existing implementation.

## Paper2Agent: verified method and transfer to this project

Read arXiv:2509.06917v1 and the published article, Reimagining research papers as interactive and reliable AI agents (Nature, 16 September 2026), especially Main and Overview of Paper2Agent. Also fetched the current official repository root and routing skill as reference material; no installation or code execution was performed.

Sources: https://arxiv.org/html/2509.06917v1 ; https://www.nature.com/articles/s41586-026-11044-y ; https://github.com/jmiao24/Paper2Agent .

The article packages papers and associated research outputs as MCP resources, executable tools and workflow prompts. Environment setup, method wrapping and iterative tests produce tools linked to original code. Reference examples validate results before delivery. Multiple paper MCPs can be connected to one conversational agent. The current repository also distinguishes paper-to-skill and code-to-MCP paths.

For our survey, retain the paper as a provenance unit, the module as a comparison/composition unit, and a tested workflow as an execution unit. A single conversational entry point can retrieve several cards and dispatch selected tools without maintaining one permanently running model instance for every paper.

### Proposed Paper Card additions

| Record | Fields | Purpose |
|---|---|---|
| Identity | paper/version, BibTeX, official code URL, code revision | Stable provenance |
| Evidence | section/page/equation, short source excerpt, review decision | Grounded answers |
| Module | function, reuse scope, task, inputs, outputs, state, constraints, assumptions, contribution role | Comparison and composition |
| Implementation | entry point, dependencies, license, model/data requirements, adapter status | Determine practical availability |
| Workflow | ordered steps, module dependencies, intermediate artifacts, feedback and stop rules | Reusable execution recipe |
| Evaluation | datasets/splits, as-of cutoff, metrics, baselines, costs, reference outputs and tolerances | Reproducible comparisons |
| Validation | source reviewed / adapter implemented / smoke tested / reproduction checked, run evidence | Distinguish evidence from executable readiness |

### Repository organization proposal

Preserve the existing CSV/JSON source and existing schema. Generate human-readable paper pages, module indexes and search records from that source. Add a shared retrieval/API layer, workflow recipes and optional paper adapters; maintain query evaluations separately from adapter execution tests. Do not introduce a second independently edited card taxonomy.

Suggested views: by task, by needed temporal function, by reuse scope, by benchmark, and by runnable status. Each recommendation should return the paper, module, evidence location, interface requirements and applicable evaluation resource.

### Implementation sequence and acceptance evidence

1. Correct self-description labels and enrich a small set of representative module cards with interfaces and evidence.
2. Build citation-grounded cross-paper questions and module search over existing records; test source support, retrieval accuracy and constraint matching against manually checked answers.
3. Add a few runnable adapters where official code and small examples are available; pin revisions and compare outputs with reference runs.
4. Demonstrate a scenario-to-modules-to-benchmark workflow, recording setup effort, successful execution, output correctness and cost.

This makes the interactive library a concrete extension of the survey's construction objective. The current deliverable is this analysis; no conversational system or executable paper agent has been deployed.
