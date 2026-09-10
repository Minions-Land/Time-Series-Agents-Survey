# Paper classification ledger

`paper_classification_ledger.csv` is the maintained work-level source for the
survey taxonomy. `paper_classification_ledger.json` is its generated structured
mirror. Each row represents one reviewed work and keeps four kinds of data
distinct:

1. Bibliographic identity and publication time from the production BibTeX,
   reference manifest, and official metadata.
2. A concise paper-claim summary and its evidence/review status.
3. Harness coding: all applicable GH, GTS, and TSK contributions, the primary
   contribution locus used for aggregate counts, and modules from
   `harness_component_catalog.csv`.
4. Multi-label task coding under four axes: forecasting and reasoning;
   augmentation and synthesis; anomaly detection and diagnosis; and decision
   support.

The three Harness contribution fields are not mutually exclusive. A work may
use or extend mechanisms at every layer. `primary_locus` answers the narrower
question used by the paper's aggregate statistics: where does the paper's main
runtime contribution enter? The GTS/TSK boundary follows the counterfactual in
the manuscript. If the temporal state, action space, tool semantics, reward, or
verifier can survive a change of task family without redesign, the mechanism is
GTS; if one of those core elements is tied to a fixed task output contract, it
is TSK.

Task axes are also multi-label. They describe where a Harness mechanism is
instantiated. A forecasting system that synthesizes training data and supports
a downstream decision may therefore carry three task flags.

## Evidence fields

- `paper_claim_summary` records the main claim currently used by the survey.
- `claim_evidence_basis` states where that summary came from.
- `claim_review_status=survey_coded` means the claim has been inherited from
  the maintained work-level mechanism profile. It does not assert that a new
  line-by-line reread was performed during ledger creation.
- After checking the original paper, replace the evidence basis with a stable
  locator such as a section, page, figure, or table, and update the review
  status to `paper_verified`.
- `harness_module_coding_basis` records whether module assignment is automatic
  or human-reviewed. The initial ledger uses keyword-assisted candidates and
  explicitly requires human review.

## Maintenance

The CSV is the editable source. Regenerate and validate the JSON mirror with:

```bash
uv run scripts/classification_manager.py sync
uv run scripts/classification_manager.py validate
```

`sync` updates bibliographic and Scholar fields from
`TS_AGENT_HARNESS_SURVEY.bib` and `references/manifest.csv`; it preserves claim
and classification judgments. `validate` checks unique keys, allowed loci,
Harness module vocabulary, task coverage, Scholar-state agreement, and exact
membership agreement with the 77-work mechanism profile in `main.tex`.

Use `bootstrap` only to reconstruct the initial ledger from the current
manuscript and historical CSV files. It overwrites classification judgments and
is not the normal update command.

When adding a paper:

1. Add and verify the BibTeX/reference identity under the policy in
   `references/README.md`.
2. Read the paper and record a source-locatable claim summary.
3. Record all applicable GH/GTS/TSK mechanisms and choose a primary locus only
   for the aggregate statistic.
4. Select one or more task axes and preserve a more specific task label in
   `task_family_original` or `task_axis_other`.
5. Add the corresponding work profile to the manuscript, run `sync`, and run
   `validate` before compiling.
