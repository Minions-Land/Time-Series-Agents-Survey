# Production Bib identity queue

This queue merges the source-reviewed inclusion candidates from the Chen, companion high-autonomy, and Chang/Xu registries. It is an intake queue, not the production bibliography. Each record must still pass identity comparison, a complete original-paper classification, and the Google Scholar Cite → BibTeX receipt check before it can be promoted to `TS_AGENT_HARNESS_SURVEY.bib` or the formal classification ledger.

`scholar_status=pending` is intentional. Official arXiv, DOI, publisher, and proceedings metadata establish identity and lawful text location but do not count as Scholar verification.
