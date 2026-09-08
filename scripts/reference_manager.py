#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "bibtexparser==1.4.3",
#   "pypdf>=5.0",
#   "requests>=2.32",
# ]
# ///

"""Build and validate the survey's reference corpus without rewriting its BibTeX."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import tempfile
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

import bibtexparser
import requests
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "TS_AGENT_HARNESS_SURVEY.bib"
REFS = ROOT / "references"
MANIFEST = REFS / "manifest.csv"
SOURCE_OVERRIDES = REFS / "source-overrides.csv"
ARXIV_METADATA = REFS / "official" / "arxiv.jsonl"
CROSSREF_METADATA = REFS / "official" / "crossref.jsonl"
OPENALEX_METADATA = REFS / "official" / "openalex.jsonl"
PDF_DIR = REFS / "pdfs"
SCHOLAR_DIR = REFS / "scholar"
REPORT_DIR = REFS / "reports"

MANIFEST_FIELDS = [
    "citation_key",
    "entry_type",
    "reference_kind",
    "title_bib",
    "authors_bib",
    "year_bib",
    "doi",
    "arxiv_id",
    "landing_url",
    "pdf_url",
    "source_kind",
    "openalex_id",
    "identity_status",
    "official_title",
    "official_authors",
    "official_year",
    "official_updated",
    "pdf_expected",
    "pdf_status",
    "pdf_path",
    "pdf_pages",
    "pdf_bytes",
    "scholar_status",
    "scholar_checked_at",
    "scholar_bib_path",
    "notes",
]

STATE_FIELDS = {
    "reference_kind",
    "openalex_id",
    "identity_status",
    "official_title",
    "official_authors",
    "official_year",
    "official_updated",
    "pdf_expected",
    "pdf_status",
    "pdf_path",
    "pdf_pages",
    "pdf_bytes",
    "scholar_status",
    "scholar_checked_at",
    "scholar_bib_path",
    "notes",
}

URL_RE = re.compile(r"https?://[^}\s,]+")
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?", re.I)
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
ATOM = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def is_true(value: str) -> bool:
    return value.strip().casefold() in {"1", "true", "yes"}


def clean_bib_value(value: str) -> str:
    return value.replace("\\url{", "").replace("}", "").strip()


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.replace("{", "").replace("}", "")
    value = re.sub(r"\\['\"`^~=.uvHckbdtr]\s*\{?([A-Za-z])\}?", r"\1", value)
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def title_similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize_title(left), normalize_title(right)).ratio()


def first_author_tokens(value: str, bib_order: bool = False) -> set[str]:
    first = value.split(" and ", 1)[0]
    if bib_order and "," in first:
        family, given = first.split(",", 1)
        first = f"{given} {family}"
    return set(normalize_title(first).split())


def load_bib() -> list[dict[str, str]]:
    with BIB_PATH.open(encoding="utf-8") as handle:
        database = bibtexparser.load(handle)
    return sorted(database.entries, key=lambda entry: entry["ID"])


def read_manifest() -> dict[str, dict[str, str]]:
    if not MANIFEST.exists():
        return {}
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        return {row["citation_key"]: row for row in csv.DictReader(handle)}


def read_source_overrides() -> dict[str, dict[str, str]]:
    if not SOURCE_OVERRIDES.exists():
        return {}
    with SOURCE_OVERRIDES.open(encoding="utf-8", newline="") as handle:
        return {row["citation_key"]: row for row in csv.DictReader(handle)}


def write_manifest(rows: list[dict[str, str]]) -> None:
    REFS.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=MANIFEST_FIELDS,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["citation_key"]))


def extract_urls(entry: dict[str, str]) -> list[str]:
    text = " ".join(entry.get(field, "") for field in ("url", "howpublished", "note"))
    return [url.rstrip(".;") for url in URL_RE.findall(text)]


def infer_source(entry: dict[str, str]) -> dict[str, str]:
    urls = extract_urls(entry)
    joined = " ".join(urls)
    arxiv_match = ARXIV_RE.search(joined)
    doi = clean_bib_value(entry.get("doi", ""))
    if not doi:
        doi_match = DOI_RE.search(entry.get("note", ""))
        doi = doi_match.group(0).rstrip(".,;") if doi_match else ""

    if arxiv_match:
        arxiv_id = arxiv_match.group(1)
        return {
            "doi": doi,
            "arxiv_id": arxiv_id,
            "landing_url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
            "source_kind": "arxiv",
        }
    if any("openreview.net/pdf" in url for url in urls):
        pdf_url = next(url for url in urls if "openreview.net/pdf" in url)
        return {"doi": doi, "arxiv_id": "", "landing_url": pdf_url, "pdf_url": pdf_url, "source_kind": "openreview"}
    if doi:
        return {"doi": doi, "arxiv_id": "", "landing_url": f"https://doi.org/{doi}", "pdf_url": "", "source_kind": "doi"}
    if urls:
        url = urls[0]
        kind = "github" if "github.com" in url else "ssrn" if "ssrn.com" in url else "official_url"
        return {"doi": "", "arxiv_id": "", "landing_url": url, "pdf_url": "", "source_kind": kind}
    return {"doi": "", "arxiv_id": "", "landing_url": "", "pdf_url": "", "source_kind": "metadata_only"}


def inventory(_: argparse.Namespace) -> None:
    previous = read_manifest()
    overrides = read_source_overrides()
    rows = []
    for entry in load_bib():
        key = entry["ID"]
        source = infer_source(entry)
        row = {field: "" for field in MANIFEST_FIELDS}
        row.update(
            {
                "citation_key": key,
                "entry_type": entry.get("ENTRYTYPE", ""),
                "reference_kind": "paper",
                "title_bib": entry.get("title", ""),
                "authors_bib": entry.get("author", ""),
                "year_bib": entry.get("year", ""),
                "pdf_expected": "true",
                **source,
            }
        )
        for field in STATE_FIELDS:
            if previous.get(key, {}).get(field):
                row[field] = previous[key][field]
        if previous.get(key) and not row["arxiv_id"] and previous[key].get("arxiv_id"):
            for field in ("arxiv_id", "landing_url", "pdf_url", "source_kind"):
                row[field] = previous[key].get(field, row[field])
        if previous.get(key) and not row["doi"] and previous[key].get("doi"):
            row["doi"] = previous[key]["doi"]
            if row["source_kind"] == "metadata_only":
                row["landing_url"] = previous[key].get("landing_url", row["landing_url"])
                row["pdf_url"] = previous[key].get("pdf_url", row["pdf_url"])
                row["source_kind"] = previous[key].get("source_kind", row["source_kind"])
        override = overrides.get(key)
        if override:
            for field in (
                "doi",
                "arxiv_id",
                "landing_url",
                "pdf_url",
                "source_kind",
                "reference_kind",
                "pdf_expected",
                "identity_status",
            ):
                if override.get(field):
                    row[field] = override[field]
            if override.get("arxiv_id") and row["identity_status"] != "matched":
                row["identity_status"] = "pending"
            if override.get("pdf_url") and row["pdf_status"] == "no_direct_pdf":
                row["pdf_status"] = "pending"
            if override.get("reason") and (not row["notes"] or override.get("identity_status")):
                row["notes"] = override["reason"]
        if not row["identity_status"]:
            row["identity_status"] = "pending"
        if not is_true(row["pdf_expected"]):
            row["pdf_status"] = "not_expected"
            row["pdf_path"] = ""
            row["pdf_pages"] = ""
            row["pdf_bytes"] = ""
        elif row["pdf_status"] == "not_expected":
            row["pdf_status"] = "pending" if row["pdf_url"] else "no_direct_pdf"
        elif not row["pdf_status"]:
            row["pdf_status"] = "pending" if row["pdf_url"] else "no_direct_pdf"
        if not row["scholar_status"]:
            row["scholar_status"] = "pending"
        rows.append(row)
    write_manifest(rows)
    print(f"wrote {len(rows)} entries to {MANIFEST.relative_to(ROOT)}")


def session_for(proxy: str | None) -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = "IJCAI2027-Time-Series-Agents-Survey reference audit"
    if proxy:
        session.proxies.update({"http": proxy, "https": proxy})
    return session


def parse_arxiv_feed(content: bytes) -> list[dict[str, object]]:
    root = ET.fromstring(content)
    records = []
    for entry in root.findall("atom:entry", ATOM):
        raw_id = entry.findtext("atom:id", default="", namespaces=ATOM)
        match = re.search(r"/abs/([0-9]{4}\.[0-9]{4,5})(v\d+)?", raw_id)
        if not match:
            continue
        authors = [node.findtext("atom:name", default="", namespaces=ATOM) for node in entry.findall("atom:author", ATOM)]
        record = {
            "arxiv_id": match.group(1),
            "version": (match.group(2) or "").lstrip("v"),
            "title": " ".join(entry.findtext("atom:title", default="", namespaces=ATOM).split()),
            "authors": authors,
            "published": entry.findtext("atom:published", default="", namespaces=ATOM),
            "updated": entry.findtext("atom:updated", default="", namespaces=ATOM),
            "comment": entry.findtext("arxiv:comment", default="", namespaces=ATOM),
            "journal_ref": entry.findtext("arxiv:journal_ref", default="", namespaces=ATOM),
            "doi": entry.findtext("arxiv:doi", default="", namespaces=ATOM),
            "landing_url": f"https://arxiv.org/abs/{match.group(1)}",
            "pdf_url": f"https://arxiv.org/pdf/{match.group(1)}",
        }
        records.append(record)
    return records


def sync_arxiv(args: argparse.Namespace) -> None:
    if not MANIFEST.exists():
        inventory(args)
    rows_by_key = read_manifest()
    overrides = read_source_overrides()
    arxiv_rows = [row for row in rows_by_key.values() if row["arxiv_id"]]
    session = session_for(args.proxy)
    records: dict[str, dict[str, object]] = {}
    ids = sorted({row["arxiv_id"] for row in arxiv_rows})
    for offset in range(0, len(ids), args.batch_size):
        batch = ids[offset : offset + args.batch_size]
        response = session.get(
            "https://export.arxiv.org/api/query",
            params={"id_list": ",".join(batch), "max_results": len(batch)},
            timeout=args.timeout,
        )
        response.raise_for_status()
        for record in parse_arxiv_feed(response.content):
            records[str(record["arxiv_id"])] = record
        print(f"arXiv metadata: {min(offset + len(batch), len(ids))}/{len(ids)}", file=sys.stderr)
        if offset + args.batch_size < len(ids):
            time.sleep(args.delay)

    retrieved_at = utc_now()
    ARXIV_METADATA.parent.mkdir(parents=True, exist_ok=True)
    with ARXIV_METADATA.open("w", encoding="utf-8") as handle:
        for arxiv_id in sorted(records):
            handle.write(json.dumps({**records[arxiv_id], "retrieved_at": retrieved_at}, ensure_ascii=False) + "\n")

    for row in arxiv_rows:
        record = records.get(row["arxiv_id"])
        if not record:
            row["identity_status"] = "not_found"
            row["notes"] = "No record returned by the official arXiv API."
            continue
        similarity = title_similarity(row["title_bib"], str(record["title"]))
        author_matches = first_author_tokens(row["authors_bib"], bib_order=True) == first_author_tokens(
            " and ".join(record["authors"])
        )
        year_matches = row["year_bib"] == str(record["published"])[:4]
        row["official_title"] = str(record["title"])
        row["official_authors"] = " and ".join(record["authors"])
        row["official_year"] = str(record["published"])[:4]
        row["official_updated"] = str(record["updated"])
        title_revision_approved = overrides.get(row["citation_key"], {}).get("allow_title_revision", "").lower() == "true"
        if similarity >= 0.92 or (similarity >= 0.85 and author_matches and year_matches) or (
            title_revision_approved and author_matches and year_matches
        ):
            row["identity_status"] = "matched"
        else:
            row["identity_status"] = "review" if similarity >= 0.75 else "mismatch"
        row["notes"] = (
            f"arXiv title similarity={similarity:.3f}; "
            f"first_author_match={author_matches}; year_match={year_matches}; "
            f"title_revision_approved={title_revision_approved}"
        )
    write_manifest(list(rows_by_key.values()))
    counts = Counter(row["identity_status"] for row in arxiv_rows)
    print(json.dumps(counts, sort_keys=True))


def discover_openalex(args: argparse.Namespace) -> None:
    if not MANIFEST.exists():
        inventory(args)
    rows_by_key = read_manifest()
    bib_by_key = {entry["ID"]: entry for entry in load_bib()}
    candidates = [row for row in rows_by_key.values() if not row["arxiv_id"]]
    session = session_for(args.proxy)
    discoveries = []
    for index, row in enumerate(candidates, 1):
        try:
            response = session.get(
                "https://api.openalex.org/works",
                params={"search": normalize_title(row["title_bib"]), "per-page": args.per_page},
                timeout=args.timeout,
            )
            response.raise_for_status()
            results = response.json().get("results", [])
        except Exception as exc:
            row["notes"] = f"OpenAlex lookup failed: {type(exc).__name__}: {exc}"
            write_manifest(list(rows_by_key.values()))
            print(f"OpenAlex {index}/{len(candidates)} {row['citation_key']}: failed: {exc}", file=sys.stderr)
            continue
        ranked = []
        for result in results:
            title = result.get("display_name") or ""
            authorships = result.get("authorships") or []
            authors = [item.get("author", {}).get("display_name", "") for item in authorships]
            similarity = title_similarity(row["title_bib"], title)
            first_match = bool(authors) and first_author_tokens(row["authors_bib"], bib_order=True) == first_author_tokens(
                " and ".join(authors)
            )
            result_year = str(result.get("publication_year") or "")
            year_match = result_year == row["year_bib"]
            ranked.append((similarity + (0.03 if first_match else 0) + (0.02 if year_match else 0), result, similarity, first_match, year_match, authors))
        if not ranked:
            row["identity_status"] = "not_found"
            row["notes"] = "No OpenAlex candidate returned."
            write_manifest(list(rows_by_key.values()))
            continue
        _, result, similarity, first_match, year_match, authors = max(ranked, key=lambda item: item[0])
        openalex_id = (result.get("id") or "").rsplit("/", 1)[-1]
        doi = (result.get("doi") or "").removeprefix("https://doi.org/")
        best_oa = result.get("best_oa_location") or {}
        primary = result.get("primary_location") or {}
        oa_pdf = best_oa.get("pdf_url") or ""
        oa_landing = best_oa.get("landing_page_url") or ""
        primary_landing = primary.get("landing_page_url") or ""
        arxiv_match = ARXIV_RE.search(" ".join([oa_pdf, oa_landing, primary_landing]))
        identity_candidate = similarity >= 0.90 and first_match
        accepted = identity_candidate and year_match
        if identity_candidate:
            row["openalex_id"] = openalex_id
            row["official_title"] = result.get("display_name") or ""
            row["official_authors"] = " and ".join(authors)
            row["official_year"] = str(result.get("publication_year") or "")
            if doi and not row["doi"]:
                row["doi"] = doi
        else:
            source = infer_source(bib_by_key[row["citation_key"]])
            row.update(source)
            row["openalex_id"] = ""
            row["official_title"] = ""
            row["official_authors"] = ""
            row["official_year"] = ""
        if identity_candidate and arxiv_match:
            arxiv_id = arxiv_match.group(1)
            row["arxiv_id"] = arxiv_id
            row["landing_url"] = f"https://arxiv.org/abs/{arxiv_id}"
            row["pdf_url"] = f"https://arxiv.org/pdf/{arxiv_id}"
            row["source_kind"] = "arxiv"
            row["identity_status"] = "pending"
            row["pdf_status"] = "pending"
        elif accepted:
            row["landing_url"] = f"https://doi.org/{row['doi']}" if row["doi"] else (oa_landing or primary_landing)
            if oa_pdf:
                row["pdf_url"] = oa_pdf
                row["pdf_status"] = "pending"
                row["source_kind"] = "openalex_oa"
            elif row["doi"]:
                row["source_kind"] = "doi"
            row["identity_status"] = "matched"
        else:
            row["identity_status"] = "review"
        row["notes"] = (
            f"OpenAlex title similarity={similarity:.3f}; "
            f"first_author_match={first_match}; year_match={year_match}"
        )
        discoveries.append(
            {
                "citation_key": row["citation_key"],
                "openalex_id": openalex_id,
                "title": result.get("display_name") or "",
                "authors": authors,
                "year": result.get("publication_year"),
                "doi": doi,
                "best_oa_landing_page_url": oa_landing,
                "best_oa_pdf_url": oa_pdf,
                "primary_landing_page_url": primary_landing,
                "title_similarity": round(similarity, 4),
                "first_author_match": first_match,
                "year_match": year_match,
                "retrieved_at": utc_now(),
            }
        )
        write_manifest(list(rows_by_key.values()))
        print(f"OpenAlex {index}/{len(candidates)} {row['citation_key']}: {row['identity_status']}")
        if index < len(candidates):
            time.sleep(args.delay)

    OPENALEX_METADATA.parent.mkdir(parents=True, exist_ok=True)
    with OPENALEX_METADATA.open("w", encoding="utf-8") as handle:
        for record in discoveries:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    write_manifest(list(rows_by_key.values()))
    print(json.dumps(Counter(row["identity_status"] for row in candidates), sort_keys=True))


def crossref_years(record: dict[str, object]) -> list[str]:
    years = []
    for field in ("published-print", "published-online", "published", "issued"):
        date_parts = (record.get(field) or {}).get("date-parts", [])
        if date_parts and date_parts[0]:
            year = str(date_parts[0][0])
            if year not in years:
                years.append(year)
    return years


def sync_crossref(args: argparse.Namespace) -> None:
    if not MANIFEST.exists():
        inventory(args)
    rows_by_key = read_manifest()
    candidates = [row for row in rows_by_key.values() if row["doi"] and not row["arxiv_id"]]
    session = session_for(args.proxy)
    records = []
    for index, row in enumerate(candidates, 1):
        try:
            response = session.get(
                "https://api.crossref.org/works/" + urllib.parse.quote(row["doi"], safe=""),
                timeout=args.timeout,
            )
            response.raise_for_status()
            record = response.json()["message"]
            titles = record.get("title") or []
            title = titles[0] if titles else ""
            authors = [
                " ".join(part for part in (author.get("given", ""), author.get("family", "")) if part).strip()
                for author in record.get("author") or []
            ]
            years = crossref_years(record)
            similarity = title_similarity(row["title_bib"], title)
            author_matches = bool(authors) and first_author_tokens(row["authors_bib"], bib_order=True) == first_author_tokens(
                " and ".join(authors)
            )
            year_matches = row["year_bib"] in years
            row["official_title"] = title
            row["official_authors"] = " and ".join(authors)
            row["official_year"] = "/".join(years)
            row["official_updated"] = (record.get("indexed") or {}).get("date-time", "")
            row["identity_status"] = "matched" if similarity >= 0.92 and author_matches and year_matches else "review"
            row["notes"] = (
                f"Crossref title similarity={similarity:.3f}; "
                f"first_author_match={author_matches}; year_match={year_matches}; "
                f"official_years={','.join(years)}"
            )
            records.append(
                {
                    "citation_key": row["citation_key"],
                    "doi": row["doi"],
                    "title": title,
                    "authors": authors,
                    "years": years,
                    "container_title": record.get("container-title") or [],
                    "volume": record.get("volume") or "",
                    "issue": record.get("issue") or "",
                    "page": record.get("page") or "",
                    "type": record.get("type") or "",
                    "url": record.get("URL") or "",
                    "retrieved_at": utc_now(),
                }
            )
            print(f"Crossref {index}/{len(candidates)} {row['citation_key']}: {row['identity_status']}")
        except Exception as exc:
            row["notes"] = f"Crossref lookup failed: {type(exc).__name__}: {exc}"
            print(f"Crossref {index}/{len(candidates)} {row['citation_key']}: failed: {exc}", file=sys.stderr)
        finally:
            write_manifest(list(rows_by_key.values()))
        if index < len(candidates):
            time.sleep(args.delay)

    CROSSREF_METADATA.parent.mkdir(parents=True, exist_ok=True)
    with CROSSREF_METADATA.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(Counter(row["identity_status"] for row in candidates), sort_keys=True))


def validate_pdf(path: Path) -> tuple[int, int]:
    if path.stat().st_size < 20_000:
        raise ValueError("file is smaller than 20 KB")
    with path.open("rb") as handle:
        if handle.read(5) != b"%PDF-":
            raise ValueError("missing PDF signature")
    reader = PdfReader(path)
    pages = len(reader.pages)
    if pages < 1:
        raise ValueError("PDF has no pages")
    return pages, path.stat().st_size


def validate_pdfs(_: argparse.Namespace) -> None:
    if not MANIFEST.exists():
        inventory(argparse.Namespace())
    rows_by_key = read_manifest()
    counts = Counter()
    failures = []
    for row in rows_by_key.values():
        destination = PDF_DIR / f"{row['citation_key']}.pdf"
        if not is_true(row["pdf_expected"]):
            counts["not_expected"] += 1
            if destination.exists():
                failures.append({"citation_key": row["citation_key"], "error": "unexpected PDF for non-paper reference"})
            continue
        if not destination.exists():
            counts["missing"] += 1
            if row["pdf_status"] in {"downloaded", "present"}:
                row["pdf_status"] = "missing"
            continue
        try:
            pages, size = validate_pdf(destination)
            row["pdf_status"] = "present"
            row["pdf_path"] = str(destination.relative_to(ROOT))
            row["pdf_pages"] = str(pages)
            row["pdf_bytes"] = str(size)
            counts["valid"] += 1
        except Exception as exc:
            row["pdf_status"] = "invalid"
            row["notes"] = f"Local PDF validation failed: {type(exc).__name__}: {exc}"
            failures.append({"citation_key": row["citation_key"], "error": str(exc)})
            counts["invalid"] += 1
    write_manifest(list(rows_by_key.values()))
    print(json.dumps({"counts": dict(sorted(counts.items())), "failures": failures}, ensure_ascii=False))


def download(args: argparse.Namespace) -> None:
    if not MANIFEST.exists():
        inventory(args)
    rows_by_key = read_manifest()
    eligible = []
    for row in rows_by_key.values():
        if not is_true(row["pdf_expected"]):
            continue
        destination = PDF_DIR / f"{row['citation_key']}.pdf"
        identity_allows_download = row["identity_status"] == "matched" or (
            args.allow_unverified and row["identity_status"] == "pending"
        )
        already_recorded = row["pdf_status"] in {"downloaded", "present"} and destination.exists()
        if row["pdf_url"] and identity_allows_download and (args.force or not already_recorded):
            eligible.append(row)
    if args.limit is not None:
        eligible = eligible[: args.limit]
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    session = session_for(args.proxy)
    failures = []
    for index, row in enumerate(eligible, 1):
        destination = PDF_DIR / f"{row['citation_key']}.pdf"
        temp_path: Path | None = None
        try:
            if destination.exists() and not args.force:
                pages, size = validate_pdf(destination)
                status = "present"
            else:
                with tempfile.NamedTemporaryFile(dir=PDF_DIR, suffix=".part", delete=False) as tmp:
                    temp_path = Path(tmp.name)
                    with session.get(row["pdf_url"], stream=True, timeout=args.timeout) as response:
                        response.raise_for_status()
                        for chunk in response.iter_content(chunk_size=1024 * 256):
                            if chunk:
                                tmp.write(chunk)
                pages, size = validate_pdf(temp_path)
                temp_path.replace(destination)
                status = "downloaded"
            row["pdf_status"] = status
            row["pdf_path"] = str(destination.relative_to(ROOT))
            row["pdf_pages"] = str(pages)
            row["pdf_bytes"] = str(size)
            print(f"PDF {index}/{len(eligible)} {row['citation_key']}: {status} ({pages} pages)")
        except Exception as exc:  # continue so a single source does not erase batch progress
            if temp_path and temp_path.exists():
                temp_path.unlink()
            row["pdf_status"] = "failed"
            row["notes"] = f"PDF download failed: {type(exc).__name__}: {exc}"
            failures.append({"citation_key": row["citation_key"], "url": row["pdf_url"], "error": str(exc)})
            print(f"PDF {index}/{len(eligible)} {row['citation_key']}: failed: {exc}", file=sys.stderr)
        finally:
            write_manifest(list(rows_by_key.values()))
        if index < len(eligible):
            time.sleep(args.delay)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with (REPORT_DIR / "download-failures.json").open("w", encoding="utf-8") as handle:
        json.dump({"generated_at": utc_now(), "failures": failures}, handle, indent=2, ensure_ascii=False)
    print(f"completed={len(eligible) - len(failures)} failed={len(failures)}")


def scholar_check(_: argparse.Namespace) -> None:
    if not MANIFEST.exists():
        inventory(argparse.Namespace())
    rows_by_key = read_manifest()
    checked = 0
    for path in sorted(SCHOLAR_DIR.glob("*.bib")):
        key = path.stem
        if key not in rows_by_key:
            print(f"unrecognized Scholar receipt: {path.name}", file=sys.stderr)
            continue
        with path.open(encoding="utf-8") as handle:
            entries = bibtexparser.load(handle).entries
        if len(entries) != 1:
            rows_by_key[key]["scholar_status"] = "review"
            rows_by_key[key]["notes"] = f"Scholar receipt contains {len(entries)} entries."
            continue
        candidate = entries[0]
        title_score = title_similarity(rows_by_key[key]["title_bib"], candidate.get("title", ""))
        year_matches = not candidate.get("year") or candidate.get("year") == rows_by_key[key]["year_bib"]
        bib_first_author = first_author_tokens(rows_by_key[key]["authors_bib"], bib_order=True)
        scholar_first_author = first_author_tokens(candidate.get("author", ""))
        author_matches = bool(bib_first_author) and bool(scholar_first_author) and bool(
            bib_first_author & scholar_first_author
        )
        rows_by_key[key]["scholar_status"] = (
            "verified" if title_score >= 0.92 and year_matches and author_matches else "review"
        )
        rows_by_key[key]["scholar_checked_at"] = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat()
        rows_by_key[key]["scholar_bib_path"] = str(path.relative_to(ROOT))
        rows_by_key[key]["notes"] = (
            f"Scholar title similarity={title_score:.3f}; year_match={year_matches}; "
            f"first_author_match={author_matches}"
        )
        checked += 1
    write_manifest(list(rows_by_key.values()))
    print(f"processed {checked} Scholar BibTeX receipts")


def audit(_: argparse.Namespace) -> None:
    if not MANIFEST.exists():
        inventory(argparse.Namespace())
    rows = list(read_manifest().values())
    identity = Counter(row["identity_status"] for row in rows)
    pdf = Counter(row["pdf_status"] for row in rows)
    scholar = Counter(row["scholar_status"] for row in rows)
    abbreviated_authors = [row["citation_key"] for row in rows if " and others" in row["authors_bib"]]
    no_stable_id = [
        row["citation_key"]
        for row in rows
        if row["reference_kind"] == "paper" and not row["doi"] and not row["arxiv_id"]
    ]
    identity_issues = [row["citation_key"] for row in rows if row["identity_status"] in {"review", "mismatch", "not_found"}]
    expected_rows = [row for row in rows if is_true(row["pdf_expected"])]
    present_pdf = [row for row in expected_rows if (PDF_DIR / f"{row['citation_key']}.pdf").exists()]
    missing_expected_pdf = [
        row["citation_key"]
        for row in expected_rows
        if not (PDF_DIR / f"{row['citation_key']}.pdf").exists()
    ]
    missing_local_pdf = [
        row["citation_key"]
        for row in expected_rows
        if row["pdf_url"] and not (PDF_DIR / f"{row['citation_key']}.pdf").exists()
    ]
    no_pdf_expected = [row["citation_key"] for row in rows if not is_true(row["pdf_expected"])]
    browser_assisted = [
        row["citation_key"]
        for row in expected_rows
        if row["source_kind"] in {"openreview", "pmc", "ssrn"}
        and not (PDF_DIR / f"{row['citation_key']}.pdf").exists()
    ]

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = [
        "# Reference audit",
        "",
        f"- Bib entries: {len(rows)}",
        f"- Identity status: {dict(sorted(identity.items()))}",
        f"- PDF status: {dict(sorted(pdf.items()))}",
        f"- References expecting a paper PDF: {len(expected_rows)}",
        f"- Expected paper PDFs present: {len(present_pdf)}",
        f"- Expected paper PDFs missing: {len(missing_expected_pdf)}",
        f"- Non-paper references with no PDF expected: {len(no_pdf_expected)}",
        f"- Google Scholar status: {dict(sorted(scholar.items()))}",
        f"- Entries with abbreviated `and others` authors: {len(abbreviated_authors)}",
        f"- Entries without DOI or arXiv ID: {len(no_stable_id)}",
        "",
        "## Blocking identity issues",
        "",
        ", ".join(identity_issues) if identity_issues else "None.",
        "",
        "## Direct-source PDFs not present",
        "",
        ", ".join(missing_local_pdf) if missing_local_pdf else "None.",
        "",
        "## Expected paper PDFs not present",
        "",
        ", ".join(missing_expected_pdf) if missing_expected_pdf else "None.",
        "",
        "## References for which no paper PDF is expected",
        "",
        ", ".join(no_pdf_expected) if no_pdf_expected else "None.",
        "",
        "## Browser-assisted acquisition pending",
        "",
        ", ".join(browser_assisted) if browser_assisted else "None.",
        "",
        "## Incomplete author lists",
        "",
        ", ".join(abbreviated_authors) if abbreviated_authors else "None.",
        "",
        "## Entries requiring stable-identity research",
        "",
        ", ".join(no_stable_id) if no_stable_id else "None.",
        "",
        "A structurally valid BibTeX entry is not counted as Scholar-verified. Only a matching raw receipt in `references/scholar/` changes that status.",
        "",
    ]
    (REPORT_DIR / "reference-audit.md").write_text("\n".join(report), encoding="utf-8")

    with (REPORT_DIR / "scholar-queue.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["citation_key", "title", "year", "status", "scholar_search_url"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            query = f'"{row["title_bib"]}"'
            if row["doi"]:
                query += f' "{row["doi"]}"'
            elif row["arxiv_id"]:
                query += f' "{row["arxiv_id"]}"'
            writer.writerow(
                {
                    "citation_key": row["citation_key"],
                    "title": row["title_bib"],
                    "year": row["year_bib"],
                    "status": row["scholar_status"],
                    "scholar_search_url": "https://scholar.google.com/scholar?q=" + urllib.parse.quote_plus(query),
                }
            )
    print((REPORT_DIR / "reference-audit.md").read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("inventory", help="Rebuild the manifest from the production BibTeX").set_defaults(func=inventory)

    openalex = subparsers.add_parser("discover-openalex", help="Discover missing stable identities and open-access locations")
    openalex.add_argument("--per-page", type=int, default=5)
    openalex.add_argument("--delay", type=float, default=0.2)
    openalex.add_argument("--timeout", type=float, default=45.0)
    openalex.add_argument("--proxy")
    openalex.set_defaults(func=discover_openalex)

    arxiv = subparsers.add_parser("sync-arxiv", help="Compare entries with official arXiv metadata")
    arxiv.add_argument("--batch-size", type=int, default=20)
    arxiv.add_argument("--delay", type=float, default=3.0)
    arxiv.add_argument("--timeout", type=float, default=45.0)
    arxiv.add_argument("--proxy")
    arxiv.set_defaults(func=sync_arxiv)

    crossref = subparsers.add_parser("sync-crossref", help="Compare DOI-only entries with official Crossref metadata")
    crossref.add_argument("--delay", type=float, default=0.2)
    crossref.add_argument("--timeout", type=float, default=45.0)
    crossref.add_argument("--proxy")
    crossref.set_defaults(func=sync_crossref)

    acquire = subparsers.add_parser("download", help="Download identity-matched PDFs from direct official URLs")
    acquire.add_argument("--limit", type=int)
    acquire.add_argument("--delay", type=float, default=0.6)
    acquire.add_argument("--timeout", type=float, default=120.0)
    acquire.add_argument("--proxy")
    acquire.add_argument("--force", action="store_true")
    acquire.add_argument("--allow-unverified", action="store_true")
    acquire.set_defaults(func=download)

    subparsers.add_parser("validate-pdfs", help="Validate every locally acquired reference PDF").set_defaults(
        func=validate_pdfs
    )
    subparsers.add_parser("scholar-check", help="Validate raw Scholar BibTeX receipts").set_defaults(func=scholar_check)
    subparsers.add_parser("audit", help="Generate completeness and Scholar queues").set_defaults(func=audit)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
