# 2026 Agent-survey expansion audit

**Purpose.** This note records additional 2026 surveys checked against the
Harness-oriented taxonomy. It separates (i) surveys that define a system or
Harness ontology, (ii) surveys that organize multi-agent mechanisms, and (iii)
task-specific time-series surveys. A record is not promoted to the production
BibTeX until its paper and Google Scholar BibTeX receipt have been checked.

## Sources checked

| Survey | Year / source identity | What the source actually organizes | Evidence status | Use in our taxonomy |
|---|---|---|---|---|
| Meng et al., *Agent Harness for Large Language Model Agents: A Survey* | 2026, Preprints v3/v4; DOI [10.20944/preprints202604.0428.v3](https://doi.org/10.20944/preprints202604.0428.v3); companion repository [Gloriaameng/Awesome-Agent-Harness](https://github.com/Gloriaameng/Awesome-Agent-Harness) | A six-component Harness tuple (H=(E,T,C,S,L,V)): **Execution Loop**, **Tool Registry**, **Context Manager**, **State Store**, **Lifecycle Hooks**, **Evaluation Interface**. It also uses a six-component completeness matrix and discusses cross-cutting challenges such as sandboxing, evaluation, protocol standardization, memory, planning, and multi-agent coordination. | Full paper PDF and repository README obtained; exact terminology checked in abstract, figure, and README. | **Primary external support for a Harness ontology.** It directly supports Interface/Execution, Tools, Memory/Context, Control/Feedback, and Evaluation. Planning and multi-agent coordination are treated as mechanisms/challenges rather than additional tuple members. |
| Lumer et al., *Tool and Agent Selection for Large Language Model Agents in Production: A Survey* | 2026, Preprints v2; DOI [10.20944/preprints202512.1050.v2](https://doi.org/10.20944/preprints202512.1050.v2) | Separates a **frontend layer** from a **backend layer**. The backend explicitly covers retrieval, execution, orchestration, context engineering, memory, tool execution, human-in-the-loop, authentication/authorization, multi-turn tool calling, and evaluation. Its taxonomy spans manual, UI-driven, retrieval-based, and autonomous selection. | Crossref record and full abstract checked; full PDF not yet acquired. | Supports **Tools and Execution**, **Memory and Context**, **Coordination/Orchestration**, and **Control/Verification/Evaluation**. It is a production tool-selection survey, not a complete Harness ontology. |
| Zhang et al., *Generalizability of Large Language Model-Based Agents: A Comprehensive Survey* | 2026, ACM; DOI [10.1145/3794858](https://doi.org/10.1145/3794858) | Categorizes generalization strategies by whether they target the **backbone LLM**, **agent components**, or **interactions**; distinguishes **generalizable frameworks** from **generalizable agents** and reviews benchmarks. | Crossref and OpenAlex records plus abstract checked; full PDF not yet acquired. | Supports the distinction between reusable GH/GTS mechanisms and task-bound mechanisms, and supports evaluation/generalization as a separate axis. It is not a component taxonomy. |
| Zhu et al., *A Survey on Large Language Model-based Multi-Agent Systems: Paradigms, Applications, and Challenges* | 2026, TechRxiv v1; DOI [10.36227/techrxiv.177160638.89229642/v1](https://doi.org/10.36227/techrxiv.177160638.89229642/v1) | Uses a three-dimensional framework: **Structure**, **Interaction**, and **Evolution**. It discusses organizational architectures, communication and collective decision-making, prompt restructuring, memory consolidation, and parameter updates. | Crossref abstract checked; full PDF not yet acquired. | Supports **Coordination and Scaling**, **Interface/Interaction**, and **Optimization/Evolution**. It is a multi-agent survey, not a time-series survey. |
| Gong, *A Survey of Large Language Models in Multi-Agent Systems: Advancing Coordination and Intelligence* | 2026, Applied and Computational Engineering; DOI [10.54254/2755-2721/2026.ch34641](https://doi.org/10.54254/2755-2721/2026.ch34641) | Organizes the field around **communication and interaction**, **system architecture and coordination**, **evaluation and benchmarking**, and **learning and evolution**. | Crossref abstract checked; full PDF not yet acquired. | Independent support for **Coordination**, **Evaluation**, and **Evolution**. It does not define a Harness tuple. |
| Liu et al., *Large language model-based multi-agent systems for financial markets simulation: a survey* | 2026, *Science China Information Sciences*; DOI [10.1007/s11432-026-4986-x](https://doi.org/10.1007/s11432-026-4986-x) | The available registry abstract describes a survey of LLM multi-agent systems for financial-market simulation; OpenAlex records a 2026 publication and an earlier arXiv version (2408.06361). | Bibliographic identity checked through Crossref/OpenAlex; publisher PDF link identified but not retrieved in this pass. | A domain-specific multi-agent survey useful for the decision-support/trading branch, but not evidence for the general Harness component ontology. |
| Yu et al., *Large Language Models for Time Series Analysis: Methodologies, Applications, and Emerging Challenges* | 2026, TechRxiv v2; DOI [10.36227/techrxiv.176703979.99494698/v2](https://doi.org/10.36227/techrxiv.176703979.99494698/v2) | Classifies LLM roles in time-series analysis as **fine-tune-based inference engines**, **TSA-methods-based enhancers**, and **hybrid collaborators**; reviews forecasting, classification, anomaly detection, and imputation. | Crossref abstract checked; TechRxiv page was Cloudflare-blocked, so no claim-level PDF coding is made. | Useful as a **time-series role/task survey** and for the LLM contribution branch (including hybrid/multi-agent systems), but not a Harness taxonomy. |
| Li et al., *A Survey of Large Language Models for Time Series Anomaly Detection: Methods, Challenges, and Future Directions* | 2026, SSRN; DOI [10.2139/ssrn.6033215](https://doi.org/10.2139/ssrn.6033215) | Task-specific survey focused on LLMs for time-series anomaly detection. | Identity and year checked through Crossref/OpenAlex; no abstract or PDF was available from the queried registries in this pass. | Candidate source for the anomaly-detection task branch only; **not used for component definitions** until full text is obtained. |

## What this changes in the notable comparison table

The new evidence does **not** justify expanding the table with many more
fine-grained components. It strengthens a compact seven-row comparison:

1. **Interface and Interaction** — execution loop, context interface,
   communication, and interaction with the environment.
2. **Memory and Context** — context management, state stores, short/long-term
   memory, and memory consolidation.
3. **Tools and Execution** — tool registries, retrieval, tool execution, and
   external APIs.
4. **Control, Verification, and Feedback** — lifecycle hooks, error recovery,
   human-in-the-loop control, observability, and evaluation interfaces.
5. **Planning and Workflow** — planning, orchestration, decomposition, and
   multi-step execution. This is a mechanism-level row, not a universal tuple
   component in every survey.
6. **Optimization and Evolution** — Harness optimization, prompt or memory
   evolution, and adaptation.
7. **Coordination and Scaling** — multi-agent structure, communication,
   delegation, and collective decision-making.

The table should retain each survey's **original term** in the cell and mark
the row as unsupported when that survey does not define an equivalent
component. In particular, Meng et al.'s six tuple should not be silently
expanded with planning or multi-agent coordination; those appear in that work
as mechanisms or cross-cutting challenges. Likewise, Yu, Chen, and Chang
remain task/reasoning-oriented sources rather than Harness ontologies.

## Screening decisions

- **Eligible for the core Harness reference queue:** Meng et al. (2026). A
  Google Scholar result, Cite page, and raw BibTeX receipt were obtained; the
  paper PDF is also stored in the local candidate snapshot. The receipt is at
  `references/reports/scholar_receipts/meng2026agentharness.bib`. It is still
  kept out of the production bibliography until the manuscript actually cites
  it.
- **Not admitted yet:** Lumer et al. (2026), Zhu et al. (2026), Gong (2026),
  and Zhang et al. (2026). Lumer, Zhang, and Zhu produced exact Scholar search
  results, but the Cite endpoint returned a block before a BibTeX receipt could
  be saved. Gong produced no exact Scholar result in the same pass. Their PDFs
  were not all available from an unblocked official source. They therefore
  remain screening evidence only.
- **Use for the time-series task/LLM-role branch, not Harness definitions:** Yu
  et al. (2026), Li et al. (2026), and the already reviewed Chen et al. and
  Chang et al. surveys.
- **Do not add a production citation solely from Crossref/OpenAlex metadata.**
  These records are a search and scope audit until the paper PDF and the
  Google Scholar Cite→BibTeX receipt are available.

**Audit date:** 2026-09-13 (Asia/Shanghai).
