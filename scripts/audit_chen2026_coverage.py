#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "bibtexparser==1.4.3",
# ]
# ///

"""Audit coverage of the 47 systems in Chen et al. (2026), Table 3."""

from __future__ import annotations

import csv
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import bibtexparser


ROOT = Path(__file__).resolve().parents[1]
CHEN_SOURCE = ROOT / "references" / "source_snapshots" / "chen2026tsagentsurvey"
CHEN_TABLE = CHEN_SOURCE / "appendix_02_methods.tex"
CHEN_BIB = CHEN_SOURCE / "custom.bib"
PRODUCTION_BIB = ROOT / "TS_AGENT_HARNESS_SURVEY.bib"
LEDGER = ROOT / "paper_classification_ledger.csv"
OUTPUT = ROOT / "references" / "reports" / "chen2026-system-coverage.csv"

FIELDS = [
    "chen_method",
    "problem_type",
    "chen_year",
    "chen_citation_keys",
    "chen_titles",
    "matched_citation_keys",
    "in_production_bib",
    "in_classification_ledger",
    "match_basis",
    "coverage_status",
    "notes",
]


def load_bib(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return {entry["ID"]: entry for entry in bibtexparser.load(handle).entries}


def normalize(value: str) -> str:
    value = re.sub(r"\\[A-Za-z]+\{([^}]*)\}", r"\1", value)
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def identifier(entry: dict[str, str], kind: str) -> str:
    if kind == "doi":
        return entry.get("doi", "").casefold().removeprefix("https://doi.org/")
    text = " ".join(entry.values())
    match = re.search(r"(?:arxiv:|abs/)(\d{4}\.\d{4,5})", text, re.I)
    return match.group(1) if match else ""


def parse_table() -> list[dict[str, str]]:
    source = CHEN_TABLE.read_text(encoding="utf-8")
    start = source.index("TimeSeriesScientist")
    end = source.index(r"\bottomrule", start)
    rows = []
    pattern = re.compile(
        r"\s*(.*?) \\cite\{([^}]+)\} & (\d{4}) & ([^&]+) & ([^&]+) &"
    )
    for line in source[start:end].splitlines():
        match = pattern.match(line)
        if match:
            method, keys, year, _source, problem = match.groups()
            rows.append(
                {
                    "chen_method": method.strip(),
                    "chen_citation_keys": keys.strip(),
                    "chen_year": year,
                    "problem_type": problem.strip(),
                }
            )
    return rows


def main() -> int:
    if not CHEN_TABLE.exists() or not CHEN_BIB.exists():
        print(f"Missing Chen source snapshot: {CHEN_SOURCE}", file=sys.stderr)
        return 1

    chen_bib = load_bib(CHEN_BIB)
    production_bib = load_bib(PRODUCTION_BIB)
    ledger_keys = {
        row["citation_key"]
        for row in csv.DictReader(LEDGER.open(encoding="utf-8", newline=""))
    }
    output_rows = []

    for row in parse_table():
        chen_keys = row["chen_citation_keys"].split(",")
        titles = []
        matches = []
        bases = []
        for chen_key in chen_keys:
            cited = chen_bib[chen_key]
            title = cited.get("title", "")
            titles.append(title)
            candidates = []
            for production_key, production_entry in production_bib.items():
                same_arxiv = bool(identifier(cited, "arxiv")) and identifier(
                    cited, "arxiv"
                ) == identifier(production_entry, "arxiv")
                same_doi = bool(identifier(cited, "doi")) and identifier(
                    cited, "doi"
                ) == identifier(production_entry, "doi")
                similarity = SequenceMatcher(
                    None,
                    normalize(title),
                    normalize(production_entry.get("title", "")),
                ).ratio()
                basis = "arxiv_id" if same_arxiv else "doi" if same_doi else "title"
                score = 1.0 if same_arxiv or same_doi else similarity
                candidates.append((score, production_key, basis))
            score, production_key, basis = max(candidates)
            if score >= 0.93:
                matches.append(production_key)
                bases.append(basis)

        all_in_bib = len(matches) == len(chen_keys)
        all_in_ledger = all_in_bib and all(key in ledger_keys for key in matches)
        status = (
            "in_classification_ledger"
            if all_in_ledger
            else "bib_only"
            if all_in_bib
            else "not_in_production_bib"
        )
        output_rows.append(
            {
                **row,
                "chen_titles": " || ".join(titles),
                "matched_citation_keys": ";".join(matches),
                "in_production_bib": "Yes" if all_in_bib else "No",
                "in_classification_ledger": "Yes" if all_in_ledger else "No",
                "match_basis": ";".join(bases),
                "coverage_status": status,
                "notes": (
                    "Identity match only; inclusion and Harness coding require original-paper review and bibliography verification."
                    if not all_in_ledger
                    else "Matched by bibliographic identity to the maintained contribution corpus."
                ),
            }
        )

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    bib_count = sum(row["in_production_bib"] == "Yes" for row in output_rows)
    ledger_count = sum(row["in_classification_ledger"] == "Yes" for row in output_rows)
    print(f"Chen systems: {len(output_rows)}")
    print(f"In production BibTeX: {bib_count}/{len(output_rows)}")
    print(f"In classification ledger: {ledger_count}/{len(output_rows)}")
    return 0 if len(output_rows) == 47 else 1


if __name__ == "__main__":
    raise SystemExit(main())
