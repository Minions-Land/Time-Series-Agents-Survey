# Module-level classification audit

Generated from `paper_classification_ledger.json` on 2026-09-13.

- Records: 139
- Raw GH/GTS dimension dictionaries identical: 139/139
- Raw task dictionaries copied from GH: 150/150 present task entries
- Derived GH annotations: 96 records with at least one exclusive module
- Derived GTS annotations: 16 records with at least one exclusive module
- Derived TSK annotations: 148 present task entries
- Non-empty derived GH/GTS dictionaries still identical: 0 records
- Coding status: all derived dimension labels are `survey_coded_needs_pdf_review`

The raw dictionaries are retained under `source_dimensions` for auditability. The
published module labels are derived separately and then made exclusive by depth: TSK owns a dimension whenever a task contract populates it; otherwise GTS owns
it when a temporal contract populates it; GH receives only the remaining reusable
runtime dimensions. LLM-side labels remain independent. General Harness labels
come from the recorded harness modules; GTS labels come from the temporal
specificity reason and claim; task-specific labels add the output contract for
forecasting, augmentation, anomaly diagnosis, or decision support. These labels are a coding aid, not a substitute for claim-level PDF
verification. A record is promoted to `paper_verified` only after its claim,
locator, and module boundary have been checked against the paper or its source
repository.
