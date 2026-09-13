# Module-level classification audit

Generated from `paper_classification_ledger.json` on 2026-09-13.

- Records: 139
- Raw GH/GTS dimension dictionaries identical: 139/139
- Raw task dictionaries copied from GH: 150/150 present task entries
- Derived GH/GTS dimension dictionaries identical: 0/139
- Coding status: all derived dimension labels are `survey_coded_needs_pdf_review`

The raw dictionaries are retained under `source_dimensions` for auditability. The
published module labels are derived separately: General Harness labels come from
the recorded harness modules; General Time-Series Harness labels come from the
recorded temporal-specificity reason and claim; task-specific labels add the
output contract for forecasting, augmentation, anomaly diagnosis, or decision
support. These labels are a coding aid, not a substitute for claim-level PDF
verification. A record is promoted to `paper_verified` only after its claim,
locator, and module boundary have been checked against the paper or its source
repository.
