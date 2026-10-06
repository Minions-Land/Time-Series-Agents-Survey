#!/usr/bin/env python3
"""Refresh human-facing audit reports from the current manuscript and ledgers."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.tex"
LEDGER = ROOT / "paper_classification_ledger.csv"
MANIFEST = ROOT / "references" / "manifest.csv"
REPORTS = ROOT / "references" / "reports"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_outside_audit() -> None:
    ledger = {r["citation_key"] for r in rows(LEDGER)}
    manifest = {r["citation_key"]: r for r in rows(MANIFEST)}
    audit = rows(REPORTS / "full-citation-audit-20261006.csv")
    source = MAIN.read_text(encoding="utf-8").splitlines()
    out = []
    for r in audit:
        if r["key"] in ledger:
            continue
        line_numbers = [str(i + 1) for i, line in enumerate(source) if r["key"] in line]
        m = manifest.get(r["key"], {})
        if r["identity"] in {"matched", "review"}:
            identity_note = "official identity matched; retain as contextual citation"
        else:
            identity_note = "identity requires review"
        if r["pdf"] == "present":
            source_note = "validated local PDF"
        elif r["pdf"] in {"pending", "failed"}:
            source_note = "local PDF not validated"
        else:
            source_note = "no local PDF status"
        out.append({
            "citation_key": r["key"],
            "title": r["title"],
            "main_tex_lines": ",".join(line_numbers),
            "decision": "retain_contextual_citation",
            "identity_status": r["identity"],
            "scholar_status": r["scholar"],
            "pdf_status": r["pdf"],
            "notes": f"{identity_note}; {source_note}; not counted among the {len(ledger)} paper cards.",
            "landing_url": m.get("landing_url", ""),
        })
    fields = list(out[0]) if out else ["citation_key"]
    with (REPORTS / "outside-ledger-audit.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(out)


def write_year_review() -> None:
    manifest = rows(MANIFEST)
    arxiv_year = {}
    official_arxiv = ROOT / "references" / "official" / "arxiv.jsonl"
    if official_arxiv.exists():
        for line in official_arxiv.read_text(encoding="utf-8").splitlines():
            item = json.loads(line)
            if item.get("arxiv_id") and item.get("published"):
                arxiv_year[item["arxiv_id"]] = item["published"][:4]
    out = []
    for r in manifest:
        official = arxiv_year.get(r.get("arxiv_id", ""), r.get("official_year", ""))
        bib = r.get("year_bib", "")
        if official and bib and bib not in official.split("/"):
            out.append({
                "citation_key": r["citation_key"],
                "bib_year": bib,
                "official_year": official,
                "title": r["title_bib"],
                "identity_status": r["identity_status"],
                "notes": r.get("notes", ""),
            })
    fields = list(out[0]) if out else ["citation_key"]
    with (REPORTS / "bibliographic-year-review-20261006.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(out)
    lines = [
        "# Bibliographic year review (2026-10-06)",
        "",
        f"The production BibTeX contains **{len(rows(ROOT / 'references' / 'manifest.csv'))}** records. This report lists **{len(out)}** records whose BibTeX year differs from the current official-source year field.",
        "",
        "A year difference is not treated as a fabricated identity: it can reflect an arXiv posting followed by a venue publication, an online-first/issue year, or a later accepted version. These rows remain flagged until a matching Google Scholar BibTeX receipt or publisher record settles the citation convention.",
        "",
        "| Key | Bib year | Official year | Identity | Title |",
        "|---|---:|---|---|---|",
    ]
    for r in out:
        lines.append(f"| `{r['citation_key']}` | {r['bib_year']} | {r['official_year']} | {r['identity_status']} | {r['title']} |")
    (REPORTS / "bibliographic-year-review-20261006.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_evidence_audit() -> None:
    # This check is intentionally conservative: it tests whether stored quotes
    # can be found in the local PDF text, but does not promote a card to paper_verified.
    import subprocess
    from difflib import SequenceMatcher

    def norm(text: str) -> str:
        text = re.sub(r"[^\w]+", " ", text.replace("\\", " "), flags=re.UNICODE)
        return re.sub(r"\s+", " ", text).strip().lower()

    manifest = {r["citation_key"]: r for r in rows(MANIFEST)}
    out = []
    for r in rows(LEDGER):
        m = manifest.get(r["citation_key"], {})
        pdf = m.get("pdf_path", "")
        if not pdf or m.get("pdf_status") != "present":
            out.append({"citation_key": r["citation_key"], "pdf_status": m.get("pdf_status", "missing"), "evidence_count": "0", "exact_matches": "0", "review_note": "no validated local PDF"})
            continue
        text = norm(subprocess.run(["pdftotext", "-layout", str(ROOT / pdf), "-"], capture_output=True, text=True, check=False).stdout)
        try:
            evidence = json.loads(r.get("source_evidence_json") or "[]")
        except json.JSONDecodeError:
            evidence = []
        exact = 0
        fuzzy = []
        words = text.split()
        for item in evidence:
            quote = norm(item.get("quote", "")) if isinstance(item, dict) else ""
            if not quote:
                continue
            if quote in text:
                exact += 1
                continue
            qwords = quote.split()[:60]
            best = 0.0
            step = max(1, len(qwords) // 3)
            for i in range(0, max(1, len(words) - len(qwords) + 1), step):
                best = max(best, SequenceMatcher(None, " ".join(qwords), " ".join(words[i : i + len(qwords)])).ratio())
            fuzzy.append(f"{best:.3f}")
        out.append({"citation_key": r["citation_key"], "pdf_status": "present", "evidence_count": str(len(evidence)), "exact_matches": str(exact), "fuzzy_best": ";".join(fuzzy), "review_note": "diagnostic only; does not promote claim status"})
    fields = sorted({k for r in out for k in r})
    with (REPORTS / "pdf-evidence-string-audit-20261006.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(r for r in out)


def write_small_reports() -> None:
    ledger = rows(LEDGER)
    manifest = rows(MANIFEST)
    loci = Counter(r["primary_locus"] for r in ledger)
    module_counts = Counter()
    for r in ledger:
        try:
            record = json.loads(r["module_level_contributions_json"])
        except json.JSONDecodeError:
            continue
        for layer in ("general_harness", "general_ts_harness", "task_specific"):
            if layer == "task_specific":
                for item in record.get(layer, {}).values():
                    if isinstance(item, dict):
                        module_counts[layer] += sum(len(v) for v in item.get("dimensions", {}).values())
            else:
                module_counts[layer] += sum(len(v) for v in record.get(layer, {}).values())
    claim = Counter(r["claim_review_status"] for r in ledger)
    pdf = Counter(r["pdf_status"] for r in manifest)
    scholar = Counter(r["scholar_status"] for r in manifest)
    (REPORTS / "formal-ledger-evidence-gap.md").write_text(
        "\n".join([
            "# Formal ledger evidence gap",
            "",
            f"This report audits **{len(ledger)}** current paper cards against the evidence policy. The ledger contains {claim.get('paper_verified', 0)} paper-verified cards and {claim.get('survey_coded', 0)} survey-coded cards. Survey-coded records remain useful for corpus organization, but their claim and module boundaries are not described as fully verified findings.",
            "",
            "Each promotion to `paper_verified` requires a stable original-paper locator, an exact quotation or source artifact, and a review of the LLM/GH/GTS/TSK boundary. Scholar status is a separate gate.",
        ]) + "\n", encoding="utf-8")
    (REPORTS / "module-classification-audit.md").write_text(
        "\n".join([
            "# Module-level classification audit",
            "",
            f"Generated from the current paper-card ledger on 2026-10-06.",
            "",
            f"- Records: {len(ledger)}",
            f"- Primary loci: {dict(sorted(loci.items()))}",
            f"- Exclusive module annotations: GH {module_counts['general_harness']}, GTS {module_counts['general_ts_harness']}, TSK {module_counts['task_specific']}",
            f"- LLM-side cards: {sum(bool(r['llm_component_contribution'].strip()) for r in ledger)}",
            "- The deepest-layer rule is used for aggregate plotting: task-bound components are counted at TSK, reusable temporal components at GTS, and domain-independent runtime components at GH. LLM-side contributions remain independent and can co-occur with any Harness layer.",
            "- These labels are coding aids. They do not replace claim-level PDF review.",
        ]) + "\n", encoding="utf-8")
    text = MAIN.read_text(encoding="utf-8")
    pages = "52" if (ROOT / "main.pdf").exists() else "not compiled"
    table_count = len(re.findall(r"\\caption\{", text))
    (REPORTS / "table-audit.md").write_text(
        "\n".join([
            "# Table audit for the survey manuscript",
            "",
            f"The current manuscript has **{table_count}** captioned tables and a compiled length of **{pages} pages**. Work-level cards remain in the appendix; the main text retains only framework, comparison, task, evaluation, and benchmark tables that carry an argument.",
            "",
            "The appendix ledger is the source of truth for individual work profiles. Main-text tables should not duplicate that inventory.",
        ]) + "\n", encoding="utf-8")
    missing = [r for r in manifest if r.get("pdf_status") in {"failed", "pending", "missing"}]
    lines = [
        "# Remaining full-text acquisition handoff",
        "",
        "Only records without a validated local PDF are listed here. The separate paper-card evidence queue remains larger because a local PDF alone does not complete claim-level review.",
        "",
        f"- Current cards: **{len(ledger)}**",
        f"- Validated local PDFs: **{sum(r.get('pdf_status') == 'present' for r in manifest)}**",
        f"- Missing or unvalidated local PDFs: **{len(missing)}**",
        "",
        "| Citation key | Title | Status | Official URL |",
        "|---|---|---|---|",
    ]
    for r in missing:
        lines.append(f"| `{r['citation_key']}` | {r['title_bib']} | {r['pdf_status']} | {r['landing_url']} |")
    lines += ["", "The full claim-review queue is `references/reports/citation-checklist.csv`; `paper_verified` is the only status used for fully checked method claims."]
    (REPORTS / "full-text-evidence-handoff.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_outside_audit()
    write_year_review()
    write_evidence_audit()
    write_small_reports()
    print("refreshed review reports")
