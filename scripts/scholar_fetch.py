#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "lxml>=5.0",
#   "requests>=2.32",
# ]
# ///

"""Acquire raw Google Scholar Cite -> BibTeX receipts.

This script is intentionally conservative: it accepts only an exact-title
Scholar result, keeps one session and one bounded delay, and stops on a
challenge or rate limit. It never rotates proxies or rewrites the production
bibliography.
"""

from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import re
import time
import urllib.parse
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

import requests
from lxml import html


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references" / "manifest.csv"
SCHOLAR_DIR = ROOT / "references" / "scholar"
REPORT_DIR = ROOT / "references" / "reports"


def normalize_title(value: str) -> str:
    value = value.replace("{", "").replace("}", "")
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize_title(left), normalize_title(right)).ratio()


def challenged(response: requests.Response) -> bool:
    text = response.text.casefold()
    return response.status_code in {403, 429, 503} or any(
        marker in text
        for marker in ("captcha", "unusual traffic", "not a robot", "/sorry/")
    )


def scholar_results(page: str) -> list[tuple[str, str]]:
    tree = html.fromstring(page)
    results = []
    for result in tree.xpath(
        '//div[contains(concat(" ", normalize-space(@class), " "), " gs_ri ")]'
    ):
        title_nodes = result.xpath('.//h3[contains(@class, "gs_rt")]')
        if not title_nodes:
            continue
        title = " ".join(title_nodes[0].text_content().split())
        related_ids = []
        for anchor in result.xpath('.//a[@href]'):
            href = html_lib.unescape(anchor.get("href", ""))
            match = re.search(r"related:([^:]+):scholar\.google\.com", href)
            if match:
                related_ids.append(match.group(1))
        if related_ids:
            results.append((title, related_ids[0]))
    return results


def cite_bib(session: requests.Session, scholar_id: str) -> tuple[str, str]:
    cite_url = (
        "https://scholar.google.com/scholar?q=info:"
        f"{scholar_id}:scholar.google.com/&output=cite&scirp=0&hl=en"
    )
    response = session.get(cite_url, timeout=30)
    if challenged(response):
        raise RuntimeError(f"Scholar challenge or rate limit at Cite endpoint ({response.status_code})")
    match = re.search(r'<a[^>]+href="([^"]+)"[^>]*>BibTeX</a>', response.text)
    if not match:
        raise RuntimeError("Scholar Cite page did not expose a BibTeX link")
    bib_url = html_lib.unescape(match.group(1))
    bib_response = session.get(bib_url, timeout=30)
    if challenged(bib_response):
        raise RuntimeError(f"Scholar challenge or rate limit at BibTeX endpoint ({bib_response.status_code})")
    bib = bib_response.text.strip()
    if not bib.startswith("@"):
        raise RuntimeError("Scholar BibTeX response is not a BibTeX entry")
    return bib, cite_url


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--delay", type=float, default=3.0)
    args = parser.parse_args()

    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows = [row for row in rows if row["reference_kind"] == "paper"]
    rows = [row for row in rows if not (SCHOLAR_DIR / f"{row['citation_key']}.bib").exists()]
    rows = rows[args.start : args.start + args.limit]

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 Chrome/131 Safari/537.36"
            )
        }
    )
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "scholar-fetch.jsonl"
    SCHOLAR_DIR.mkdir(parents=True, exist_ok=True)
    processed = 0
    acquired = 0

    with report_path.open("a", encoding="utf-8") as report:
        for index, row in enumerate(rows, start=1):
            query = f'"{row["title_bib"]}"'
            identifier = row.get("doi") or row.get("arxiv_id")
            if identifier:
                query += f" {identifier}"
            search_url = "https://scholar.google.com/scholar?q=" + urllib.parse.quote_plus(query)
            try:
                response = session.get(search_url, timeout=30)
                if challenged(response):
                    raise RuntimeError(f"Scholar challenge or rate limit at search endpoint ({response.status_code})")
                candidates = scholar_results(response.text)
                matching = [item for item in candidates if similarity(row["title_bib"], item[0]) >= 0.92]
                event = {
                    "time": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                    "citation_key": row["citation_key"],
                    "search_url": search_url,
                    "candidates": [title for title, _ in candidates[:5]],
                    "matched": bool(matching),
                }
                if matching:
                    bib, cite_url = cite_bib(session, matching[0][1])
                    destination = SCHOLAR_DIR / f"{row['citation_key']}.bib"
                    destination.write_text(bib + "\n", encoding="utf-8")
                    event.update({"status": "saved", "scholar_title": matching[0][0], "cite_url": cite_url})
                    acquired += 1
                else:
                    event["status"] = "no_exact_result"
                print(row["citation_key"], event["status"])
                report.write(json.dumps(event, ensure_ascii=False) + "\n")
                report.flush()
                processed += 1
            except Exception as exc:
                event = {
                    "time": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                    "citation_key": row["citation_key"],
                    "search_url": search_url,
                    "status": "stopped" if "challenge" in str(exc).casefold() else "error",
                    "error": str(exc),
                }
                report.write(json.dumps(event, ensure_ascii=False) + "\n")
                report.flush()
                print(row["citation_key"], event["status"], str(exc))
                return 2 if event["status"] == "stopped" else 1
            if index < len(rows):
                time.sleep(args.delay)

    print(f"processed={processed} acquired={acquired} report={report_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
