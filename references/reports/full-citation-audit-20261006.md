# Full citation and evidence audit (2026-10-06)

This report is generated from the current `main.tex`, production BibTeX, reference manifest, and module-level ledger. Stable identity, Google Scholar receipts, PDFs, and claim evidence are reported separately.

## Counts

- Unique citation keys in `main.tex`: **151**; total citation occurrences: **296**.
- Production BibTeX entries: **151**; missing cited keys: **0**; uncited production entries: **0**.
- Classification cards: **130** (128 production-Bib cards and 2 repository-only records).
- Contextual/component citations outside the paper-card ledger: **23**; these are background, survey, model, benchmark, or infrastructure sources rather than additional paper cards.
- Claim review states: **{'paper_verified': 5, 'survey_coded': 125}**; cards with source-evidence JSON: **128/130**.
- Identity status: **{'matched': 150, 'review': 1}**.
- PDF status for cited works: **{'failed': 1, 'pending': 1, 'present': 149}**.
- Scholar receipt status: **{'pending': 125, 'review': 5, 'verified': 21}**.

## Issues requiring attention

- Stable-identity review: chen2025trace
- Scholar receipts with title/year/author mismatch: climateagent2025, elliottagents2025, finmem2023, tradingagents2024, trafficr12025
- Cited works without a validated local PDF: 2; see `reference-audit.md` for the list.
- Cards whose claim evidence is not yet marked `paper_verified`: 125; these remain usable as survey-coded records but must not be described as full-text verified.

## Interpretation

An arXiv or DOI match confirms bibliographic identity; it does not confirm a Google Scholar Cite-to-BibTeX receipt or a claim-level reading. The production bibliography contains no abbreviated author lists, no undefined citation keys, and no duplicate arXiv identities. Three unmatched Scholar receipts are retained under `references/scholar/unmatched/` and are excluded from verification because their titles identify different works.
