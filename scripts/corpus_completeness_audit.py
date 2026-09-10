#!/usr/bin/env python3
"""Build a candidate-pool audit without treating the current ledger as complete."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references" / "manifest.csv"
LEDGER = ROOT / "paper_classification_ledger.csv"
SCREENING = ROOT / "time_series_agent_screening_audit.csv"
CHEN = ROOT / "references" / "reports" / "chen2026-system-coverage.csv"
CHANG = ROOT / "references" / "source_snapshots" / "changsurvey2026" / "agentic-systems.csv"
XU = ROOT / "references" / "source_snapshots" / "xu2026forecastagentsurvey" / "agentic-forecasting-systems.csv"
PROMPTS = ROOT / "references" / "source_snapshots" / "promptstoagents2026" / "high-autonomy-papers.csv"
CHEN_REGISTRY = ROOT / "references" / "reports" / "chen2026-missing-system-registry.csv"
SCOPE_DECISIONS = ROOT / "references" / "reports" / "production-bib-scope-decisions.csv"
OUTPUT = ROOT / "references" / "reports" / "corpus-completeness-audit.csv"
REPORT = ROOT / "references" / "reports" / "corpus-completeness-audit.md"

FIELDS = [
    "candidate_id",
    "citation_key",
    "title",
    "year",
    "candidate_source",
    "in_production_bib",
    "in_classification_ledger",
    "screening_decision",
    "coverage_status",
    "identity_status",
    "scholar_status",
    "review_note",
]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if None in (reader.fieldnames or ()) or any(None in row for row in rows):
            raise ValueError(f"Malformed CSV columns in {path}")
        return rows


def normalized(value: str) -> str:
    value = re.sub(r"\\[A-Za-z]+\{([^}]*)\}", r"\1", value)
    value = value.replace("{", "").replace("}", "")
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def normalized_doi(value: str) -> str:
    return value.strip().casefold().removeprefix("https://doi.org/")


def main() -> None:
    manifest = read(MANIFEST)
    ledger = {row["citation_key"]: row for row in read(LEDGER)}
    screening = {row["citation_key"]: row for row in read(SCREENING)}
    scope_decisions = {row["citation_key"]: row for row in read(SCOPE_DECISIONS)}
    rows = []

    for item in manifest:
        key = item["citation_key"]
        screen = screening.get(key, {})
        in_ledger = key in ledger
        decision = screen.get("decision", "")
        preliminary = scope_decisions.get(key, {})
        if in_ledger:
            status = "included_current_ledger"
            note = "Membership exists; original-paper claim and taxonomy evidence may still require review."
        elif decision.startswith("EXCLUDE") or decision == "CITE_ONLY_RELATED_WORK":
            status = "screened_not_included"
            note = screen.get("notes", "Existing screening decision; recheck when source coverage changes.")
        elif preliminary:
            decision = preliminary["decision"]
            if decision == "INCLUDE_CANDIDATE":
                status = "include_candidate_needs_coding"
            elif decision == "BOUNDARY_REVIEW":
                status = "needs_scope_review"
            else:
                status = (
                    "source_reviewed_not_included"
                    if preliminary["review_status"] == "source_reviewed"
                    else "preliminary_not_included"
                )
            note = preliminary["reason"] + " Evidence: " + preliminary["evidence_basis"]
        else:
            status = "needs_scope_review"
            note = "Bibliography membership alone does not decide corpus eligibility."
        rows.append(
            {
                "candidate_id": f"bib:{key}",
                "citation_key": key,
                "title": item["title_bib"],
                "year": item["year_bib"],
                "candidate_source": "production_bib",
                "in_production_bib": "Yes",
                "in_classification_ledger": "Yes" if in_ledger else "No",
                "screening_decision": decision,
                "coverage_status": status,
                "identity_status": item["identity_status"],
                "scholar_status": item["scholar_status"],
                "review_note": note,
            }
        )

    known_titles = {normalized(row["title"]): row for row in rows}
    known_arxiv = {
        item["arxiv_id"]: known_titles[normalized(item["title_bib"])]
        for item in manifest
        if item["arxiv_id"]
    }
    known_doi = {
        normalized_doi(item["doi"]): known_titles[normalized(item["title_bib"])]
        for item in manifest
        if item["doi"]
    }
    for item in read(CHEN):
        if item["in_production_bib"] == "Yes":
            continue
        titles = item["chen_titles"].split(" || ")
        for index, title in enumerate(titles, start=1):
            if normalized(title) in known_titles:
                continue
            suffix = f":{index}" if len(titles) > 1 else ""
            rows.append(
                {
                    "candidate_id": f"chen2026:{item['chen_method']}{suffix}",
                    "citation_key": "",
                    "title": title,
                    "year": item["chen_year"],
                    "candidate_source": "chen2026_table3",
                    "in_production_bib": "No",
                    "in_classification_ledger": "No",
                    "screening_decision": "",
                    "coverage_status": "needs_scope_review",
                    "identity_status": "source_cited",
                    "scholar_status": "pending",
                    "review_note": "Candidate identified from Chen et al. Table 3; inspect the original paper before inclusion or exclusion.",
                }
            )
            known_titles[normalized(title)] = rows[-1]

    for item in read(CHANG):
        title_key = normalized(item["title"])
        if title_key in known_titles:
            existing = known_titles[title_key]
            if "changsurvey2026" not in existing["candidate_source"]:
                existing["candidate_source"] += ";changsurvey2026_agent_tables"
            continue
        rows.append(
            {
                "candidate_id": f"changsurvey2026:{item['method']}",
                "citation_key": "",
                "title": item["title"],
                "year": item["year"],
                "candidate_source": "changsurvey2026_agent_tables",
                "in_production_bib": "No",
                "in_classification_ledger": "No",
                "screening_decision": "",
                "coverage_status": "needs_scope_review",
                "identity_status": "source_cited",
                "scholar_status": "pending",
                "review_note": f"Candidate has non-zero T-Agent in Chang et al. {item['source_locator']}; inspect the original paper before inclusion or exclusion.",
            }
        )
        known_titles[title_key] = rows[-1]

    for item in read(XU):
        title_key = normalized(item["title"])
        if title_key in known_titles:
            existing = known_titles[title_key]
            if "xu2026forecastagentsurvey" not in existing["candidate_source"]:
                existing["candidate_source"] += ";xu2026forecastagentsurvey_tables"
            continue
        rows.append(
            {
                "candidate_id": f"xu2026forecastagentsurvey:{item['method']}",
                "citation_key": "",
                "title": item["title"],
                "year": item["year"],
                "candidate_source": "xu2026forecastagentsurvey_tables",
                "in_production_bib": "No",
                "in_classification_ledger": "No",
                "screening_decision": "",
                "coverage_status": "needs_scope_review",
                "identity_status": "source_cited",
                "scholar_status": "pending",
                "review_note": f"Agent-oriented forecasting candidate from Xu et al. {item['source_locator']}; inspect the original paper before inclusion or exclusion.",
            }
        )
        known_titles[title_key] = rows[-1]

    for item in read(PROMPTS):
        title_key = normalized(item["title"])
        doi_candidates = [normalized_doi(part) for part in item["doi"].split(";") if part.strip()]
        existing = known_arxiv.get(item["arxiv_id"]) if item["arxiv_id"] else None
        if existing is None:
            existing = next((known_doi[doi] for doi in doi_candidates if doi in known_doi), None)
        if existing is None:
            existing = known_titles.get(title_key)
        if existing is not None:
            if "promptstoagents2026" not in existing["candidate_source"]:
                existing["candidate_source"] += ";promptstoagents2026_L3L4"
            continue
        rows.append(
            {
                "candidate_id": f"promptstoagents2026:{item['paper_id']}",
                "citation_key": "",
                "title": item["title"],
                "year": item["year"],
                "candidate_source": "promptstoagents2026_L3L4",
                "in_production_bib": "No",
                "in_classification_ledger": "No",
                "screening_decision": "",
                "coverage_status": "needs_scope_review",
                "identity_status": "source_cited",
                "scholar_status": "pending",
                "review_note": f"High-autonomy candidate coded {item['A3_code']} ({item['A3_workflow_autonomy']}) in From Prompts to Agents; inspect the original paper before inclusion or exclusion.",
            }
        )
        known_titles[title_key] = rows[-1]
        if item["arxiv_id"]:
            known_arxiv[item["arxiv_id"]] = rows[-1]
        for doi in doi_candidates:
            known_doi[doi] = rows[-1]

    # The registry preserves the full set of Chen Table 3 systems that were
    # absent from the production bibliography.  It is an identity/source
    # survey record only; it never upgrades a candidate to paper-verified.
    chen_registry = {normalized(row["title"]): row for row in read(CHEN_REGISTRY)}
    for row in rows:
        registry = chen_registry.get(normalized(row["title"]))
        if registry is None:
            continue
        if registry["original_paper_status"] == "paper_reviewed":
            row["coverage_status"] = "include_candidate_needs_coding"
            row["review_note"] = registry["paper_claim_summary"] + " Evidence: " + registry["paper_evidence_locator"]

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    counts = {status: sum(row["coverage_status"] == status for row in rows) for status in sorted({row["coverage_status"] for row in rows})}
    source_counts = {
        source: sum(row["candidate_source"] == source for row in rows)
        for source in sorted({row["candidate_source"] for row in rows})
    }
    report = [
        "# Corpus completeness audit",
        "",
        f"- Candidate work records: {len(rows)}",
        f"- Candidate sources: {source_counts}",
        f"- Coverage states: {counts}",
        "- Current-ledger membership is a status under review, not evidence of corpus completeness.",
        "- `needs_scope_review` is not an inclusion decision.",
        "- Google Scholar verification remains independent of candidate discovery and scope review.",
        "",
        "The 31 Chen-source records correspond to 30 systems absent from the production bibliography; ElliottAgents cites two underlying papers.",
    ]
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Candidates: {len(rows)}")
    for status, count in counts.items():
        print(f"{status}: {count}")


if __name__ == "__main__":
    main()
