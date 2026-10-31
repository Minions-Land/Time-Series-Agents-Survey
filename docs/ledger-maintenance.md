# Maintaining the survey evidence ledger

`paper_classification_ledger.csv` is the maintained source. `reviewed_modules_json` stores concrete contributions; `paper_classification_ledger.json`, appendix profiles and the cumulative figure are generated views. One module ID has one scope. The LLM side is independent; Harness scopes use the most specific supported layer: domain-independent runtime (GH), reusable temporal operation (GTS), or task-conditioned procedure (TSK). Several tasks alone do not establish GTS. Training data that directly develops an LLM's temporal capability belongs on the LLM side; a numerical-series synthesis procedure retains its task contract.

## Version and labels

`references/taxonomy_schema.json` is the version authority for record fields and controlled vocabulary. Version 2.5 adds attributed external resources, boundary-review records and original task values. Version 2.6 adds module-level `reuse_evidence`: a GH or GTS module is `demonstrated` when its source applies it to two or more task families (module tasks, else work tasks) and `inferred` otherwise; LLM-side and TSK modules are `not_applicable`. The migration fills the field only when it is absent, so a reviewed value survives later runs. Work-level and module-level public task labels use the same canonical names. Legacy CSV boolean column names remain storage keys; export maps them to the canonical task vocabulary. Original prose labels and pre-migration aliases are retained. Historical review files are immutable evidence, not the current taxonomy authority.

## Resources

Cards link to original repositories, project pages, datasets, benchmark sites, documentation and model artifacts. Each resource has a type, URL, source path, page/section locator, attribution evidence and an availability result. A related-work URL is not an official resource for the citing paper. A live URL does not establish author ownership; conversely, an inaccessible author-provided link may still be correctly attributed. `not_found_in_source` means no attributed resource was found in the inspected source; it does not assert that no resource exists.

## Review and generation

1. Read the task definition, method and relevant evaluation passages. Record a module-level keep/change/uncertain decision and source-located rationale. Keep module IDs stable through scope corrections.
2. Independently review disputed changes and record the final decision. Maintain the canonical CSV only after adjudication. Preserve the review history in `references/reviews/`.
3. Generate JSON, appendix profiles and timeline from the same maintained records. The timeline excludes explicitly undated modules and reports that omission.
4. Run read-only structural checks, tests and LaTeX compilation; inspect affected pages before publishing.

```bash
uv run --with bibtexparser==1.4.3 python scripts/check_ledger_consistency.py
PYTHONPATH=scripts uv run --with bibtexparser==1.4.3 python -m unittest discover -s scripts/tests
python scripts/make_contribution_timeline.py
python scripts/sync_reviewed_manuscript.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

`check_ledger_consistency.py` does not write files. The older `classification_manager.py validate` command regenerates JSON and its audit report. Metadata synchronization and schema migration are explicit writing operations. Structural checks establish consistency, while module-level review records document the semantic decisions.
