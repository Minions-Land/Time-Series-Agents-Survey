# Paper classification ledger

`paper_classification_ledger.csv` is the maintained work-level source for the
survey taxonomy. `paper_classification_ledger.json` is its generated structured mirror. Version
2.0 adds separate LLM-side, General Harness, General Time-Series Harness, and
four-task module records. Each row represents one reviewed work and keeps four kinds of data
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

The version-2 taxonomy fields are deliberately independent and multi-label:

- `llm_side_contribution` records temporal representation/alignment,
  instruction/interaction/reasoning, and LLM adaptation.
- `general_harness_modules` records the seven General Harness dimensions and
  fine-grained module labels used by the reviewed Time-Series Agent work.
- `general_ts_harness_modules` records only mechanisms with a temporal
  dependency and stores `ts_specificity_reason` plus source evidence.
- `task_specific_modules` contains the same seven-module lens under the four
  task families: forecasting/prediction, augmentation/synthesis,
  anomaly/diagnosis, and decision support.

Empty arrays are valid. A paper can populate multiple records, and
`taxonomy_review_status` distinguishes paper-verified entries from records
that still need PDF-level reclassification.

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

## Competitor coverage

`reports/chen2026-system-coverage.csv` audits the 47 systems in Table 3 of
Chen et al., *LLM Agents for Time-Series: A Survey*, against both the production
BibTeX and this classification ledger. The audit is generated from the cited
table rows and bibliographic records in the official arXiv source snapshot, so
method aliases are resolved through paper identity rather than name guessing.
An absent system remains a coverage candidate until its original paper has
been reviewed for scope and its bibliography has been verified; absence does
not by itself imply either inclusion or exclusion.

`reports/corpus-completeness-audit.csv` is the broader candidate queue. It
combines every production-BibTeX entry with systems found in the Chen et al.
table that are absent from that bibliography. Its `needs_scope_review` status
is deliberately non-committal: neither citation by a prior survey nor presence
in our bibliography proves that a work satisfies our runtime-scope rule.

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

Regenerate the Chen et al. coverage audit with:

```bash
uv run scripts/audit_chen2026_coverage.py
python3 scripts/corpus_completeness_audit.py
```

When adding a paper:

1. Add and verify the BibTeX/reference identity under the policy in
   `references/README.md`.
2. Read the paper and record a source-locatable claim summary.
3. Record the LLM-side contribution separately from General Harness,
   General-Time-Series Harness, and task-specific modules. Record all
   applicable dimensions and preserve the source locator and temporal-binding
   reason.
4. Select one or more of the four task axes and preserve a more specific task
   label in `task_family_original` or `task_axis_other`.
5. Add the corresponding work profile to the manuscript, run `sync`, and run
   `validate` before compiling.
