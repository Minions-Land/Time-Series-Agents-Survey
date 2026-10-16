# From General to Specific: A Survey of Time-Series Agent Systems

**Build a time-series agent for your scenario: identify the capabilities you need, compare reusable modules, and find the original methods, repositories, and evaluation resources.**

<p align="center">
  <a href="main.tex">Manuscript</a> ·
  <a href="paper_classification_ledger.json">Paper Cards</a> ·
  <a href="TS_AGENT_HARNESS_SURVEY.bib">Bibliography</a> ·
  <a href="references/CLASSIFICATION_LEDGER.md">Curation Guide</a> ·
  <a href="figures/editable/README.md">Editable Figures</a>
</p>

## Start with your question

| Your question | Start here |
|---|---|
| How do I develop an agent for my time-series scenario? | [Survey manuscript](main.tex): system definition, LLM capabilities, and three Harness scopes |
| Which mechanisms could address my temporal data or workflow problem? | [Module records](paper_classification_ledger.json): function, scope, task, and source evidence |
| What exactly does a paper contribute? | [Paper Card structure](references/reports/paper-card-schema.md) and [maintained records](paper_classification_ledger.csv) |
| Where can I develop or evaluate the system? | Infrastructure and Benchmarks in the [manuscript](main.tex), with original resource links |
| Where are the references and figure sources? | [BibTeX](TS_AGENT_HARNESS_SURVEY.bib) and [PowerPoint collection](figures/editable/README.md) |

## From general to specific

**Time-Series Agent ≈ LLM + General Harness + Time-Series Harness Module**

The survey connects four kinds of contribution:

| Contribution | Design question |
|---|---|
| **LLM side** | How does the model interpret observations, select tools, and respond to feedback? Which learned temporal capabilities help the workflow? |
| **General Harness** | How are interaction, memory, tools, execution, planning, feedback, and coordination organized? |
| **General Time-Series Harness** | How are temporal data, operations, context, memory, and validation handled across tasks? |
| **Task-Specific Harness** | How are those capabilities specialized for the required output and objective? |

Task-specific methods cover **forecasting and prediction**, **augmentation and synthesis**, **anomaly detection and diagnosis**, and **decision support**. The temporal-function view connects a reader's problem to the module records. The [classification guide](references/CLASSIFICATION_LEDGER.md) explains the shared mechanism vocabulary and reuse criteria.

The comparison unit is a concrete module. A paper can contribute several modules; each module is counted at its most specific applicable scope. LLM-side contributions are recorded independently.

## Evidence-linked Paper Cards

Cards connect a paper's identity and claims to concrete modules, task assumptions, evaluation evidence, and source passages. Follow the original paper and repository links to explore the authors' implementations.

The ledger snapshot contains **138 examined records**, **136 retained works and resources**, and **292 module entries**. These are curation counts, not a count of independently reproduced systems. Field definitions and review states are documented in the [card schema](references/reports/paper-card-schema.md).

| Resource | Role |
|---|---|
| [CSV ledger](paper_classification_ledger.csv) | Maintained source for paper and module annotations |
| [JSON ledger](paper_classification_ledger.json) | Generated structured view for search, analysis, and downstream interfaces |
| [BibTeX](TS_AGENT_HARNESS_SURVEY.bib) | Manuscript citation records |
| [Taxonomy schema](references/taxonomy_schema.json) | Classification vocabulary |
| [Curation guide](references/CLASSIFICATION_LEDGER.md) | Evidence requirements, aggregation rules, and maintenance commands |

## Comparative perspective

The survey asks what differs across methods, which assumptions shape their use, and what evidence supports each choice. Section-level synthesis connects those comparisons to system design and evaluation. Open problems bring together questions that recur across tasks, including temporal validity, reusable procedures, evolving context, and decision utility.

Our resource direction is a **searchable, conversational guide to papers and modules**, with source-grounded explanations and links to official repositories, documentation, datasets, and benchmarks. See the [revision and resource-hub proposal](docs/editorial-and-resource-hub-proposal.md) for the planned interface and editorial changes. The linked ledger and manuscript are available now; the conversational interface is planned.

## Contribute a paper or correction

[Open an issue](https://github.com/Minions-Land/Time-Series-Agents-Survey/issues) with the paper title and official URL, the proposed module or correction, a page/section locator, and the relevant official repository or benchmark link. For implementation details, identify the relevant documentation page or code location. Curation follows the documented evidence and scope criteria.

<details>
<summary><strong>For maintainers: update and validate the ledger</strong></summary>

Edit the CSV source, then regenerate and validate its structured view:

```bash
uv run scripts/classification_manager.py sync
uv run scripts/classification_manager.py validate
```

See the [maintenance documentation](references/CLASSIFICATION_LEDGER.md) for the source files and generated reports. Manuscript compilation uses the existing LaTeX project; editable PowerPoint figures are maintained separately from their manuscript exports.

</details>
