# Paper classification ledger

`paper_classification_ledger.csv` is the maintained work-level source for the
survey taxonomy. `paper_classification_ledger.json` is its generated structured mirror. Version
2.5 maintains separate LLM-side, General Harness, General Time-Series Harness, and
four-task module records. Each row represents one reviewed work and keeps four kinds of data
distinct:

1. Bibliographic identity and publication time from the production BibTeX,
   reference manifest, and official metadata.
2. A concise paper-claim summary and its evidence/review status.
3. Harness coding: all applicable GH, GTS, and TSK contributions, a historical work-level
   contribution summary, and modules from
   `harness_component_catalog.csv`.
4. Multi-label task coding under four axes: forecasting and prediction;
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
- `module_level_contributions` makes the aggregation unit explicit: each reviewed module ID is one contribution unit, so one
  paper can contribute multiple units across layers and task families.

Empty arrays are valid. A paper can populate multiple records, and
`taxonomy_review_status` distinguishes paper-verified entries from records
that still need PDF-level reclassification.

The three Harness contribution fields are not mutually exclusive. A work may
use or extend mechanisms at every layer. `primary_locus` is retained as a
descriptive field for the paper-level record; module-level plots and counts use
the explicit fine-grained annotations instead. The GTS/TSK boundary follows the counterfactual in
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
Harness module vocabulary, task coverage, Scholar-state agreement, and membership agreement with the maintained contribution profile in `main.tex`.

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

## Module identity and the unified taxonomy (2026-10-15)

All Harness chapters and records use the same seven mechanism dimensions.
Contribution scope (GH, GTS, TSK) and supported tasks are coordinates on that
same record, not alternative taxonomies. LLM-side contributions remain separate.
The historical component catalog supplies fine-grained aliases, not another
chapter-level classification. `primary_locus` is historical work metadata and
is never a plotting unit.

`reviewed_modules_json` in the maintained CSV contains the source-reviewed
module list. Each module has a stable ID, name, one layer, mechanism dimensions,
task memberships, scope reason, role, and page/section evidence. Generation
preserves this list and projects it into the existing layer fields. A shared
module may have multiple task memberships or dimension labels but counts once.
Distinct modules in the same dimension may occupy different layers.

The 2026-10-15 full audit covers all 138 examined records. Of these, 134
paper-supported works and two repository-supported resources contribute 292
modules; GridMind and Tree-of-Evidence remain background records with zero
contribution modules. Review evidence is in `reviews/20261015_full_audit/`.
The 300 PDF excerpts and two repository excerpts pass transcription/locator
checks. These checks verify quotation accuracy; scope judgments are recorded
separately in each module's `scope_reason`.

`other_tasks` extends the same task coordinate for classification, imputation,
annotation, question answering, data quality, and other source-supported outputs.
A TSK module must have a value in `tasks` or `other_tasks`. Module roles distinguish
methods, model training, training data, infrastructure, and evaluation.
`review_audit` preserves evaluated settings, inspected pages, corrections, and
record disposition. Repository verification never becomes paper verification.
The timeline counts only reviewed module IDs; no inferred candidates are included.

After a reviewed-card change, run `classification_manager.py sync`,
`classification_manager.py validate`, `sync_reviewed_manuscript.py`, and
`make_contribution_timeline.py`; then compile the manuscript. The manuscript
synchronizer updates only the appendix snapshot and reviewed rows, not prose.

## Current maintenance workflow

See [ledger maintenance](../docs/ledger-maintenance.md) for schema 2.5, preserved task aliases, attributed official links and read-only checks. The complete 2026-10-16 boundary review and independent adjudications are in `references/reviews/20261016_boundary_audit/`. Historical review files are preserved; the CSV remains the current source.
