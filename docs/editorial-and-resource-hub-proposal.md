# Editorial revision and resource-hub proposal

Status: proposal, 2026-10-16. This incorporates the authors' discussion and supersedes the executable-adapter roadmap in the earlier Introduction/Paper2Agent review. The manuscript narrative was revised on 2026-10-16: LLM interaction now introduces the construction framework; method-level comparison and resource navigation guide the synthesis. Card-field enrichment and conversational navigation remain planned.

## Shared objective

Help readers develop a specialized time-series agent by selecting appropriate model capabilities, runtime mechanisms, temporal functions, task procedures, and evaluation resources. Paper Cards provide a source-grounded route from each design choice to its literature and official resources.

The companion repository is a curated intermediary: it explains, compares, and links. Official repositories, documentation, checkpoints, datasets, and benchmark pages remain the destinations for implementations. An optional conversational layer retrieves the cards, explains choices with citations, and directs readers to those resources.

## Introduction: proposed paragraph logic

1. **Application objective.** Temporal analysis supplies evidence for actions. Use a demand-planning example to connect observations, forecasts, and operational decisions.
2. **Adaptive workflow.** Intermediate evidence changes what should be inspected, computed, revised, or accepted next. This motivates the model-and-harness system, with temporal information boundaries and task constraints.
3. **Specialization problem.** A generic coding agent supplies reusable execution; temporal semantics and output objectives determine the additional modules. Introduce the three reuse scopes and the independent LLM side through this concrete need.
4. **Literature-discovery problem.** Useful mechanisms are distributed across explicitly agentic systems, reasoning methods, adaptive pipelines, and evaluation resources. Identify modules from method evidence as well as paper-level self-description. ARTIST's temporal-segment selection is a checked example; TimeXL's existing self-description flag requires correction before use in corpus claims.
5. **Our analytical position.** Compare concrete modules through function, reuse assumptions, required evidence, and evaluation. Explain which choices fit which settings, and connect the conclusions to official implementation and benchmark resources.
6. **Position and contributions.** Contrast verified organizing questions in existing surveys, then state the construction framework, comparative synthesis/design guidance, evaluation-resource mapping, and evidence-linked module library.

Keep the seven-dimension enumeration and detailed coding rules in the conceptual/method sections and appendix. The Introduction should establish why the distinctions matter before presenting their vocabulary.

### Suggested position statement

> We take a construction-oriented view of time-series agents: specialization depends on how model capabilities, reusable runtime mechanisms, temporal operations, and task procedures are composed under a scenario's information and output requirements. We compare methods through these design choices and connect them to the evidence and resources needed for implementation and evaluation.

### Suggested resource contribution

> We provide an evidence-linked module library that connects agent systems, time-series reasoning methods, and adaptive workflows. Paper Cards record module functions, reuse assumptions, source evidence, and links to original papers and implementation resources, supporting comparison and resource discovery for new temporal scenarios.

Resource links and reuse assumptions must be checked before the manuscript claims completed coverage. Conversational access becomes a delivered contribution after the interface and answer-quality evaluation exist.

## Opinion throughout the survey

The editorial voice should arise from comparative evidence. Integrate interpretation alongside method descriptions and finish each substantive subsection with a short synthesis. A section-level ending draws out broader relationships and leads into the next design question.

A synthesis can answer:
- What is the important difference among the reviewed mechanisms?
- Under what inputs, feedback, supervision, or operating constraints is each useful?
- What trade-off or requirement follows for the developer?
- Which unresolved question follows from this comparison?

These questions guide writing; they are not four mandatory sentences or a repeated heading. Use a natural closing paragraph, with work names and citations attached to the comparisons. Avoid generic endings about promise, limitations, or the need for further research.

### Section-specific emphasis

| Section | Comparative judgment |
|---|---|
| LLM side | Which capability is learned, what supervision it requires, and which operations the runtime must supply |
| General Harness | Which execution/state/control mechanism fits the interaction pattern and failure conditions |
| General Time-Series Harness | Which temporal assumptions a module enforces and what survives a change of task |
| Task-Specific Harness | Which output, objective, and feedback make a procedure appropriate, and what changes when the task changes |
| Infrastructure and Benchmarks | Which system behavior a resource makes observable and what additional measurements the scenario needs |
| Discussion/Open Problems | Cross-section research questions, their motivating evidence, and concrete ways to evaluate progress |

### Example of a method-grounded closing paragraph

For augmentation and synthesis, compare MERIT's reviewed positive views for contrastive learning with MetaCaster's generator updates driven by downstream forecast error. The conclusion is to select the generation feedback according to the intended learner and use of the generated data. This is a practical judgment derived from their mechanisms; numerical superiority would require matched experimental evidence.

## Repository and Paper Card organization

Keep the CSV as the maintained source and JSON as its generated view. Add fields through the existing generator and validator, then derive reader-facing pages and indexes. Preserve one module taxonomy.

### Link-oriented fields

- Official paper URL and version, bibliographic identity.
- Module function, scope, task, inputs/outputs and reuse assumptions when documented.
- Source passages and review decisions supporting the annotation.
- Official repository URL, documentation/demo/model/data links, and link-check date.
- Relevant evaluation resource, metric, temporal protocol, and primary-source locator.
- Comparative notes with supporting works; distinguish author statements, our synthesis, and suggested reuse.

A repository commit or release can anchor a code-specific assertion when needed. Collecting environments, wrapping every method, or reproducing every repository is outside this resource-hub design.

### Reader-facing navigation

1. Start with a scenario or task.
2. Select a required temporal function.
3. Compare module cards and their assumptions.
4. Read the original evidence.
5. Follow official implementation and evaluation links.

The README is the front door, using GitHub-compatible link bars, compact tables, and optional maintenance details from the requested Awesome README skill. Dedicated task/module indexes can be generated later from reviewed fields. Manuscript/PDF links should point to an actually published artifact; the local compiled PDF is currently Git-ignored.

### Conversational scope

Example request: "I have irregular sensor streams and need anomaly diagnosis. Which components and evaluation resources fit?"

The answer should provide relevant module choices, grounded comparisons, source locators, assumptions, and official URLs. Evaluate evidence support, constraint matching, URL correctness, and whether recommendations distinguish source-supported capabilities from proposed combinations.

## Next editing sequence

1. Completed: rewrite Introduction as a continuous argument, centering LLM interaction and Harness composition.
2. Audit section/subsection endings, prioritizing General Time-Series Harness and Task-Specific Harness; add comparative synthesis where substantive judgments are missing.
3. Correct self-description labels against source text and add structured resource links through the canonical ledger workflow.
4. Generate task/module/resource navigation from the same data; add a conversational interface only after retrieval and evidence checks are in place.
