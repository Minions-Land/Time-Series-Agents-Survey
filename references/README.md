# Reference corpus

This directory connects every citation in `TS_AGENT_HARNESS_SURVEY.bib` to an
official identity, an optional local PDF, and an explicit Google Scholar check.
The production bibliography remains the root-level `.bib` file used by LaTeX.

## Layout

- `manifest.csv`: one row per BibTeX key, including whether the item is a paper
  and whether a PDF is expected, plus its authoritative acquisition state.
- `official/arxiv.jsonl`: metadata returned by the official arXiv API.
- `official/crossref.jsonl`: metadata returned by the official Crossref API for
  DOI-only entries.
- `source-overrides.csv`: stable identifiers manually confirmed against an
  official source when the production BibTeX does not yet carry them.
- `pdfs/<citation-key>.pdf`: locally acquired papers. PDFs are intentionally
  excluded from ordinary Git history; the manifest and acquisition script are
  tracked instead.
- `scholar/<citation-key>.bib`: raw BibTeX exported from the matching Google
  Scholar result in a normal browser session.
- `reports/reference-audit.md`: generated completeness and integrity report.
- `reports/scholar-queue.csv`: generated queue of entries awaiting Scholar review.

## Source policy

Work identity is resolved in this order: DOI, arXiv identifier, another stable
official identifier, then normalized title plus first author and year. Metadata
from a publisher, proceedings site, Crossref, or arXiv establishes the work
identity and lawful source. It does not count as Google Scholar verification.
Google Scholar verification requires a raw BibTeX receipt exported from the
matching Scholar result; only that receipt can change `scholar_status` to
`verified`. Scholar may merge versions, abbreviate venues, or omit a DOI, so the
receipt is compared against the higher-priority identity evidence rather than
silently replacing it.

PDFs are acquired only from lawful sources such as arXiv, a publisher or
proceedings site, OpenReview, or an institutional repository. A GitHub project
without a paper and a metadata-only record are retained in the manifest with a
clear status rather than being represented by a fabricated PDF.

## Commands

The script uses `uv` inline dependencies, so it does not modify the system Python
environment.

```bash
uv run scripts/reference_manager.py inventory
uv run scripts/reference_manager.py discover-openalex
uv run scripts/reference_manager.py sync-arxiv
uv run scripts/reference_manager.py sync-crossref
uv run scripts/reference_manager.py download
uv run scripts/reference_manager.py validate-pdfs
uv run scripts/reference_manager.py scholar-check
uv run scripts/reference_manager.py audit
uv run scripts/scholar_fetch.py --limit 10
```

`inventory` is non-destructive: it rebuilds bibliographic columns while retaining
existing identity, PDF, and Scholar states. `discover-openalex` fills missing
stable identifiers and lawful open-access locations, but leaves discovered arXiv
records pending until `sync-arxiv` compares them with the official API. A PDF
becomes eligible for download only after the corresponding identity check.
Source overrides are discovery receipts, not permission to rewrite the
production bibliography; arXiv overrides still pass through `sync-arxiv`.

For Scholar verification, search the exact title in the user's normal browser,
confirm the matching work, choose **Cite -> BibTeX**, and save the returned entry
as `scholar/<citation-key>.bib`. `scholar-check` compares that receipt with the
production Bib and records the date. A title or year mismatch remains `review`;
the script never silently rewrites the production bibliography. An arXiv,
Crossref, OpenAlex, publisher, or proceedings record without this raw Scholar
receipt remains `pending`, even when its metadata is otherwise complete.

The receipt must be copied from the BibTeX view opened by Scholar's **Cite**
control for the matching result. A manually reconstructed entry, an arXiv export,
or a publisher/Crossref export is not a Scholar receipt.

`scholar_fetch.py` is a bounded convenience helper for exact-title searches. It
uses one normal session, saves only a matching raw receipt, and stops on HTTP
403/429/503 or a Scholar challenge. It does not rotate proxies, retry around a
challenge, or rewrite `TS_AGENT_HARNESS_SURVEY.bib`. Manual browser acquisition
remains the fallback for entries left pending.
