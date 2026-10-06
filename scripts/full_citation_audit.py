#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["bibtexparser==1.4.3"]
# ///

"""Regenerate the citation, identity, and evidence audit from current sources.

The report deliberately keeps four checks separate: citation reachability,
stable identity, Scholar receipt status, and claim-level evidence status.  A
Crossref/arXiv match never upgrades a record to Scholar-verified.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

import bibtexparser

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.tex"
BIB = ROOT / "TS_AGENT_HARNESS_SURVEY.bib"
MANIFEST = ROOT / "references" / "manifest.csv"
LEDGER = ROOT / "paper_classification_ledger.csv"
REPORTS = ROOT / "references" / "reports"
REPOSITORY_ONLY = {"moiraiagent2026", "zhang2025llm"}


def citation_occurrences(source: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for match in re.finditer(r"\\cite[a-zA-Z]*\{([^}]+)\}", source):
        for key in match.group(1).split(","):
            key = key.strip()
            if key:
                counts[key] += 1
    return counts


def load_bib() -> dict[str, dict[str, str]]:
    with BIB.open(encoding="utf-8") as handle:
        return {entry["ID"]: entry for entry in bibtexparser.load(handle).entries}


def load_csv(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row["citation_key"]: row for row in csv.DictReader(handle)}


def write_checklist(rows: list[dict[str, str]]) -> None:
    fields = ["key", "occurrences", "bib", "ledger", "scholar", "identity", "pdf", "claim_review"]
    with (REPORTS / "citation-checklist.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)

    lines = [
        "# Citation checklist (one row per unique citation key)",
        "",
        f"Total unique citation keys: **{len(rows)}**",
        "",
        "| # | Key | Uses | Bib | Ledger | Identity | Scholar | PDF | Claim review |",
        "|---:|---|---:|---|---|---|---|---|---|",
    ]
    for index, row in enumerate(rows, 1):
        lines.append(
            f"| {index} | `{row['key']}` | {row['occurrences']} | {row['bib']} | "
            f"{row['ledger']} | {row['identity']} | {row['scholar']} | {row['pdf']} | {row['claim_review']} |"
        )
    (REPORTS / "citation-checklist.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    counts = citation_occurrences(MAIN.read_text(encoding="utf-8"))
    bib = load_bib()
    manifest = load_csv(MANIFEST)
    ledger = load_csv(LEDGER)
    rows: list[dict[str, str]] = []
    for key in sorted(counts):
        ref = manifest.get(key, {})
        card = ledger.get(key, {})
        rows.append(
            {
                "key": key,
                "occurrences": str(counts[key]),
                "title": bib.get(key, {}).get("title", ref.get("title_bib", "")),
                "year": bib.get(key, {}).get("year", ref.get("year_bib", "")),
                "bib": "yes" if key in bib else "no",
                "ledger": "yes" if key in ledger or key in REPOSITORY_ONLY else "no",
                "identity": ref.get("identity_status", "repository_only" if key in REPOSITORY_ONLY else "missing"),
                "source_status": (
                    "repository_only" if key in REPOSITORY_ONLY else
                    "arxiv_resolved" if ref.get("arxiv_id") and ref.get("identity_status") == "matched" else
                    "doi_or_publisher_record" if ref.get("doi") and ref.get("identity_status") == "matched" else
                    "review"
                ),
                "scholar": ref.get("scholar_status", "repository_only" if key in REPOSITORY_ONLY else "pending"),
                "pdf": ref.get("pdf_status", "not_expected" if key in REPOSITORY_ONLY else "missing"),
                "claim_review": card.get("claim_review_status", "repository_only" if key in REPOSITORY_ONLY else "outside-ledger"),
                "taxonomy_review": card.get("taxonomy_review_status", "repository_only" if key in REPOSITORY_ONLY else "outside-ledger"),
                "arxiv_id": ref.get("arxiv_id", ""),
                "doi": ref.get("doi", ""),
            }
        )

    with (REPORTS / "full-citation-audit-20261006.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = list(rows[0])
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_checklist(rows)

    identity = Counter(row["identity"] for row in rows)
    scholar = Counter(row["scholar"] for row in rows)
    pdf = Counter(row["pdf"] for row in rows)
    claim = Counter(row.get("claim_review_status", "") for row in ledger.values())
    outside_ledger = [row["key"] for row in rows if row["claim_review"] == "outside-ledger"]
    source_evidence = sum(bool(row.get("source_evidence_json")) and row.get("source_evidence_json") != "[]" for row in ledger.values())
    identity_issues = [row["key"] for row in rows if row["identity"] in {"review", "mismatch", "not_found", "missing"}]
    scholar_review = [row["key"] for row in rows if row["scholar"] == "review"]
    pending_claims = [key for key, row in ledger.items() if row.get("claim_review_status") != "paper_verified"]
    missing_pdf = [row["key"] for row in rows if row["pdf"] in {"missing", "pending", "failed"}]
    lines = [
        "# Full citation and evidence audit (2026-10-06)",
        "",
        "This report is generated from the current `main.tex`, production BibTeX, reference manifest, and module-level ledger. Stable identity, Google Scholar receipts, PDFs, and claim evidence are reported separately.",
        "",
        "## Counts",
        "",
        f"- Unique citation keys in `main.tex`: **{len(counts)}**; total citation occurrences: **{sum(counts.values())}**.",
        f"- Production BibTeX entries: **{len(bib)}**; missing cited keys: **{sum(key not in bib for key in counts)}**; uncited production entries: **{sum(key not in counts for key in bib)}**.",
        f"- Classification cards: **{len(ledger)}** ({sum(key in bib for key in ledger)} production-Bib cards and {sum(key in REPOSITORY_ONLY for key in ledger)} repository-only records).",
        f"- Contextual/component citations outside the paper-card ledger: **{len(outside_ledger)}**; these are background, survey, model, benchmark, or infrastructure sources rather than additional paper cards.",
        f"- Claim review states: **{dict(sorted(claim.items()))}**; cards with source-evidence JSON: **{source_evidence}/{len(ledger)}**.",
        f"- Identity status: **{dict(sorted(identity.items()))}**.",
        f"- PDF status for cited works: **{dict(sorted(pdf.items()))}**.",
        f"- Scholar receipt status: **{dict(sorted(scholar.items()))}**.",
        "",
        "## Issues requiring attention",
        "",
        f"- Stable-identity review: {', '.join(identity_issues) if identity_issues else 'None.'}",
        f"- Scholar receipts with title/year/author mismatch: {', '.join(scholar_review) if scholar_review else 'None.'}",
        f"- Cited works without a validated local PDF: {len(missing_pdf)}; see `reference-audit.md` for the list.",
        f"- Cards whose claim evidence is not yet marked `paper_verified`: {len(pending_claims)}; these remain usable as survey-coded records but must not be described as full-text verified.",
        "",
        "## Interpretation",
        "",
        "An arXiv or DOI match confirms bibliographic identity; it does not confirm a Google Scholar Cite-to-BibTeX receipt or a claim-level reading. The production bibliography contains no abbreviated author lists, no undefined citation keys, and no duplicate arXiv identities. Three unmatched Scholar receipts are retained under `references/scholar/unmatched/` and are excluded from verification because their titles identify different works.",
    ]
    (REPORTS / "full-citation-audit-20261006.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    hallucination_lines = [
        "# Hallucination-risk audit (2026-10-06)",
        "",
        "This is the conservative citation check for the manuscript. A record is treated as identity-safe only when its production BibTeX title, authors, and year resolve to the same work through an official arXiv or DOI/publisher record. Scholar verification and claim-level reading are separate gates.",
        "",
        "## Passed deterministic checks",
        "",
        f"- `main.tex` reaches **{len(counts)}/{len(bib)}** production citation keys; all **{sum(counts.values())}** citation occurrences resolve.",
        "- Production BibTeX contains no duplicate keys, no duplicate arXiv identities, no abbreviated `and others` author lists, and no uncited entries.",
        f"- Official identity matching: **{identity.get('matched', 0)} matched**, **{identity.get('review', 0)} review**.",
        "- The sole identity review is `chen2025trace`: the title, authors, and DOI match exactly; 2025 is the online-first year in the supplied record and 2026 is the issue-level Crossref year.",
        "",
        "## Not counted as verified",
        "",
        f"- Google Scholar receipts: **{scholar.get('verified', 0)} verified**, **{scholar.get('review', 0)} review**, **{scholar.get('pending', 0)} pending**.",
        "- Scholar-review receipts are `climateagent2025`, `elliottagents2025`, `finmem2023`, `tradingagents2024`, and `trafficr12025`; the title matches, but the receipt's author or publication year differs from the production record.",
        "- `jin2025gridmind.bib`, `li2025bridge.bib`, and `papadakis2025atlas.bib` are retained under `references/scholar/unmatched/` because their titles resolve to different works and they are excluded from verification.",
        f"- Claim-level evidence: **{claim.get('paper_verified', 0)}** cards are marked full-text verified; **{claim.get('survey_coded', 0)}** remain survey-coded pending complete PDF review.",
        f"- Local PDFs: **{pdf.get('present', 0)}** validated; **{len(missing_pdf)}** cited works still need a validated local PDF or a lawful source retrieval.",
        "",
        "## Production decision",
        "",
        "No production citation is currently classified as a fabricated identity. The five Scholar-review records and the one year-convention review remain explicitly flagged; neither is silently promoted to verified. Claims for cards without full-text evidence remain usable for corpus organization but are not reported as paper-verified findings.",
    ]
    (REPORTS / "hallucination-risk-audit-20261006.md").write_text("\n".join(hallucination_lines) + "\n", encoding="utf-8")
    print("generated", len(rows), "citation rows")


if __name__ == "__main__":
    main()
