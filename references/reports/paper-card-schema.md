# Module-level paper card

The survey uses one paper card per reviewed work. The JSON ledger is the source of truth; the appendix renders a human-readable view of selected fields.

Each card contains:

- **Identity:** title, authors, year, DOI or landing page, BibTeX key, and identity status.
- **Claim:** the paper's central claim and contribution summary.
- **Evidence:** page or section locator, quotation, and evidence status.
- **LLM side:** whether the work changes temporal representation, alignment, instruction tuning, or reasoning capability.
- **Harness modules:** seven General Harness dimensions, reusable General Time-Series Harness modules, and task-specific modules.
- **Task contract:** forecasting, augmentation and synthesis, anomaly detection and diagnosis, decision support, or another explicitly recorded task.
- **Evaluation:** benchmark, process evidence, temporal-contract checks, task metrics, and deployment or decision evidence.
- **Review state:** source quality, Scholar/BibTeX status, and whether PDF-level review remains pending.

The ledger keeps inclusive source descriptions so that a paper can record contributions at several levels. Aggregate plots use an exclusive deepest-layer projection: task-bound modules count as Task-Specific Harness, reusable temporal modules as General Time-Series Harness, and domain-independent runtime modules as General Harness. The LLM-side field is independent of this projection.

New work extends the map by adding a card, adding a module under an existing dimension, or adding a task-specific branch with its own contract. It does not require rewriting the schema or changing the construction hierarchy.
