#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "bibtexparser==1.4.3",
# ]
# ///

"""Build and validate the survey's work-level classification ledger."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

import bibtexparser


ROOT = Path(__file__).resolve().parents[1]
MAIN_TEX = ROOT / "main.tex"
BIB_PATH = ROOT / "TS_AGENT_HARNESS_SURVEY.bib"
LEGACY_LEDGER = ROOT / "time_series_agent_ledger.csv"
SCREENING_AUDIT = ROOT / "time_series_agent_screening_audit.csv"
REFERENCE_MANIFEST = ROOT / "references" / "manifest.csv"
CATALOG = ROOT / "harness_component_catalog.csv"
LEDGER = ROOT / "paper_classification_ledger.csv"
JSON_LEDGER = ROOT / "paper_classification_ledger.json"
REPORT = ROOT / "references" / "reports" / "classification-audit.md"

TASK_AXES = (
    "forecasting_reasoning",
    "augmentation_synthesis",
    "anomaly_detection_diagnosis",
    "decision_support",
)

FIELDS = [
    "work",
    "citation_key",
    "paper_title",
    "authors",
    "bib_year",
    "first_public_date",
    "public_month",
    "publication_date_precision",
    "doi",
    "arxiv_id",
    "landing_url",
    "paper_claim_summary",
    "claim_evidence_basis",
    "claim_review_status",
    "llm_component_contribution",
    "primary_locus",
    "primary_contribution",
    "general_harness_contribution",
    "general_ts_harness_contribution",
    "task_specific_harness_contribution",
    "harness_modules",
    "harness_module_coding_basis",
    "task_family_original",
    "task_axis_forecasting_reasoning",
    "task_axis_augmentation_synthesis",
    "task_axis_anomaly_detection_diagnosis",
    "task_axis_decision_support",
    "task_axis_other",
    "task_axis_notes",
    "work_type",
    "claimed_as_agent",
    "agent_claim_evidence",
    "included_as",
    "identity_status",
    "scholar_status",
    "scholar_checked_at",
    "scholar_bib_path",
    "bib_sync_status",
    "classification_notes",
    "source_evidence_json",
    "taxonomy_schema_version",
    "llm_side_subdimensions",
    "general_harness_dimensions",
    "general_ts_harness_dimensions",
    "general_ts_specificity_reason",
    "task_specific_modules_json",
    "module_level_contributions_json",
    "taxonomy_review_status",
]

MODULE_RULES = {
    "Planning": r"plan|decompos|workflow|orchestrat|pipeline|role|routing|controller|human|user|interactive|copilot|assistant|support",
    "Memory and Context Engineering": r"memor|retriev|context|exemplar|knowledge bank|prior|history",
    "Tool Use": r"tool|code|sql|simulat|model outputs?|predictor|tsfm|statistical",
    "Control": r"validat|verif|gate|audit|faithful|constraint|supervisor|check|regression|calibrat",
    "Harness Optimization": r"optim|train|learn|distill|evol|refin|repair|reinforcement|reward|adapt",
    "Reasoning": r"reason|rationale|chain.of.thought|cot|explain|interpret|analy[sz]",
    "Acting": r"action|execut|edit|deploy|decision policy|observe.reason.act",
    "Environment Modeling": r"state|workspace|environment|observation|evidence|task files?",
    "Execution Environment": r"sandbox|interpreter|simulator|code execution|replay environment",
    "State Store and Artifacts": r"artifact|ledger|report|trace|rule histor|dataset|question bank",
    "Lifecycle Orchestration": r"lifecycle|workflow|intake|revision|report|handoff|generate.verify.refine",
    "Multi-Agent Scaling": r"multi.agent|debate|collaborat|agent group|collective|specialized analyzer",
    "Verification and Evaluation": r"interface|schema|protocol|task contract|structured output",
}

# These labels were corrected in the paper after the legacy 52-row CSV was
# frozen. They reproduce both the monthly cumulative curves and the published
# 5/9/63 counts under the current task-family-contract rubric in main.tex.
LOCUS_OVERRIDES = {
    "castr12026": "TSK",
    "calm2025": "TSK",
    "mas4ts2026": "GTS",
    "timeart2026": "TSK",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            for field in FIELDS:
                row.setdefault(field, "")
            writer.writerow(row)


def parse_json_value(raw: str, default):
    if not raw:
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return default


DIMENSION_NAMES = (
    "Interface and Interaction",
    "Memory and Context",
    "Tools and Execution",
    "Control, Verification, and Feedback",
    "Planning and Workflow",
    "Optimization and Evolution",
    "Coordination and Scaling",
)


def empty_dimensions() -> dict[str, list[str]]:
    return {name: [] for name in DIMENSION_NAMES}


def _add_dimension(out: dict[str, list[str]], name: str, labels: list[str]) -> None:
    for label in labels:
        if label not in out[name]:
            out[name].append(label)


def derive_general_dimensions(row: dict[str, str]) -> dict[str, list[str]]:
    """Map explicit harness module names to the seven comparison dimensions."""
    out = empty_dimensions()
    modules = [part.strip().lower() for part in row.get("harness_modules", "").split(";") if part.strip()]
    for module in modules:
        if "memory" in module or "context" in module:
            _add_dimension(out, "Memory and Context", ["memory_or_context"])
        if "tool" in module or "execution" in module:
            _add_dimension(out, "Tools and Execution", ["tool_or_execution"])
        if "control" in module or "verification" in module or "evaluation" in module:
            _add_dimension(out, "Control, Verification, and Feedback", ["control_or_verification"])
        if "planning" in module or "workflow" in module or "lifecycle" in module:
            _add_dimension(out, "Planning and Workflow", ["planning_or_workflow"])
        if "optimization" in module or "evolution" in module or "adapt" in module:
            _add_dimension(out, "Optimization and Evolution", ["optimization_or_evolution"])
        if "coordination" in module or "scaling" in module or "multi-agent" in module:
            _add_dimension(out, "Coordination and Scaling", ["coordination_or_scaling"])
        if any(token in module for token in ("interface", "interaction", "reasoning", "acting", "environment")):
            _add_dimension(out, "Interface and Interaction", ["interface_or_interaction"])
    return out


def derive_temporal_dimensions(row: dict[str, str]) -> dict[str, list[str]]:
    """Derive temporal dimensions from the recorded temporal-contract reason.

    These are coding aids, not paper-level findings.  The JSON records the
    basis and keeps the status pending until a PDF or source implementation is
    checked.
    """
    out = empty_dimensions()
    reasons = " ".join(parse_json_value(row.get("general_ts_specificity_reason", ""), [])).lower()
    text = " ".join(
        row.get(field, "")
        for field in ("general_ts_harness_contribution", "paper_claim_summary", "task_family_original")
    ).lower()
    joined = f"{reasons} {text}"
    if any(k in joined for k in ("window", "horizon", "frequency", "operation", "signal state", "time-series")):
        _add_dimension(out, "Interface and Interaction", ["temporal_interface"])
        _add_dimension(out, "Tools and Execution", ["temporal_operations"])
    if any(k in joined for k in ("memory", "context", "retrieval", "evidence", "market state", "provenance")):
        _add_dimension(out, "Memory and Context", ["time_indexed_context"])
    if any(k in joined for k in ("leakage", "contract", "validation", "diagnos", "anomaly")):
        _add_dimension(out, "Control, Verification, and Feedback", ["temporal_contract_check"])
    if any(k in joined for k in ("forecast", "workflow", "operation")):
        _add_dimension(out, "Planning and Workflow", ["temporal_workflow"])
    if any(k in joined for k in ("regime", "distribution shift", "adapt")):
        _add_dimension(out, "Optimization and Evolution", ["shift_or_regime_adaptation"])
    if any(k in joined for k in ("multi-agent", "coordination", "role")):
        _add_dimension(out, "Coordination and Scaling", ["temporal_coordination"])
    return out


def derive_task_dimensions(row: dict[str, str], temporal: dict[str, list[str]]) -> dict:
    """Create task-contract labels without copying the GH/GTS dictionaries."""
    tasks = parse_json_value(row.get("task_specific_modules_json", ""), {})
    output = {}
    for task_name, item in tasks.items():
        if not isinstance(item, dict) or not item.get("present"):
            output[task_name] = item
            continue
        dims = empty_dimensions()
        for name, labels in temporal.items():
            dims[name].extend(labels)
        if task_name == "forecasting_prediction":
            _add_dimension(dims, "Control, Verification, and Feedback", ["horizon_and_backtest_contract"])
            _add_dimension(dims, "Planning and Workflow", ["forecast_revision_workflow"])
        elif task_name == "augmentation_synthesis":
            _add_dimension(dims, "Tools and Execution", ["generator_and_transform_tools"])
            _add_dimension(dims, "Control, Verification, and Feedback", ["fidelity_and_utility_check"])
        elif task_name == "anomaly_detection_diagnosis":
            _add_dimension(dims, "Control, Verification, and Feedback", ["alert_and_diagnosis_contract"])
            _add_dimension(dims, "Planning and Workflow", ["detection_to_diagnosis_workflow"])
        elif task_name == "decision_support":
            _add_dimension(dims, "Control, Verification, and Feedback", ["risk_and_constraint_check"])
            _add_dimension(dims, "Planning and Workflow", ["action_policy_workflow"])
            _add_dimension(dims, "Coordination and Scaling", ["human_or_specialist_review"])
        item = dict(item)
        item["dimensions"] = dims
        item["dimension_coding_basis"] = "derived_from_task_contract_and_temporal_reason"
        item["dimension_review_status"] = "survey_coded_needs_pdf_review"
        output[task_name] = item
    return output


def exclusive_harness_layers(
    gh: dict[str, list[str]],
    gts: dict[str, list[str]],
    task: dict,
) -> tuple[dict[str, list[str]], dict[str, list[str]], dict]:
    """Keep each module at its deepest Harness layer.

    LLM-side labels are independent and are therefore not passed here.  For
    the nested Harness layers, a populated task contract owns its dimension;
    otherwise a populated GTS dimension owns it; GH receives only the
    remaining reusable runtime dimensions.
    """
    task_out = {}
    task_by_dim = {name: [] for name in DIMENSION_NAMES}
    for task_name, item in task.items():
        if not isinstance(item, dict):
            task_out[task_name] = item
            continue
        copied = dict(item)
        dims = copied.get("dimensions", empty_dimensions())
        for name in DIMENSION_NAMES:
            for label in dims.get(name, []):
                if label not in task_by_dim[name]:
                    task_by_dim[name].append(label)
        task_out[task_name] = copied

    gts_out = empty_dimensions()
    gh_out = empty_dimensions()
    for name in DIMENSION_NAMES:
        if task_by_dim[name]:
            continue
        if gts.get(name):
            gts_out[name] = list(gts[name])
            continue
        gh_out[name] = list(gh.get(name, []))
    return gh_out, gts_out, task_out


def module_contribution_record(row: dict[str, str]) -> dict:
    """Return module-level annotations with separate GH, GTS, and TSK coding."""
    gh_raw = parse_json_value(row.get("general_harness_dimensions", ""), {})
    gts_raw = parse_json_value(row.get("general_ts_harness_dimensions", ""), {})
    task_raw = parse_json_value(row.get("task_specific_modules_json", ""), {})
    gh = derive_general_dimensions(row)
    gts = derive_temporal_dimensions(row)
    gh_exclusive, gts_exclusive, task_exclusive = exclusive_harness_layers(
        gh, gts, derive_task_dimensions(row, gts)
    )
    return {
        "unit": "non-empty fine-grained module annotation",
        "llm_side": parse_json_value(row.get("llm_side_subdimensions", ""), []),
        "general_harness": gh_exclusive,
        "general_ts_harness": gts_exclusive,
        "task_specific": task_exclusive,
        "inclusive_dimensions": {
            "general_harness": gh,
            "general_ts_harness": gts,
            "task_specific": derive_task_dimensions(row, gts),
        },
        "source_dimensions": {
            "general_harness": gh_raw,
            "general_ts_harness": gts_raw,
            "task_specific": task_raw,
        },
        "coding_basis": {
            "general_harness": "derived_from_explicit_harness_modules",
            "general_ts_harness": "derived_from_temporal_specificity_reason_and_claim",
            "task_specific": "derived_from_task_contract_and_temporal_reason",
        },
        "review_status": "survey_coded_needs_pdf_review",
    }


def clean_latex(value: str) -> str:
    value = value.replace(r"\allowbreak", "")
    value = re.sub(r"\\(?:selfclaim|typeSMshort|typeBenchshort)\{\}", "", value)
    value = value.replace("--", "-")
    return " ".join(value.strip().split())


def parse_profiles() -> list[dict[str, str]]:
    source = MAIN_TEX.read_text(encoding="utf-8")
    profile_caption_markers = (
        r"\caption{Mechanism profiles of the ",
        r"\caption{Complete profiles of the ",
    )
    for marker in profile_caption_markers:
        if marker in source:
            start = source.index(marker)
            break
    else:
        raise ValueError("Cannot find the complete work-level profile table")
    end = source.index(r"\end{longtable}", start)
    row_re = re.compile(
        r"^(?:(.*?)\\citep\{([^}]+)\}|(.*?)(?:\\RepoMoirai|\\RepoLLMTSFD))(.*?) & "
        r"\\textbf\{GH:\} (.*?)\\newline"
        r"\\textbf\{GTS:\} (.*?)\\newline"
        r"\\textbf\{TSK:\} (.*?)\\\\\\midrule$"
    )
    profiles = []
    for line in source[start:end].splitlines():
        if (r"\citep{" not in line and r"\RepoMoirai" not in line and r"\RepoLLMTSFD" not in line) or r"\textbf{GH:}" not in line:
            continue
        match = row_re.match(line)
        if not match:
            raise ValueError(f"Cannot parse mechanism-profile row: {line[:160]}")
        work, key, alt_work, metadata, gh, gts, tsk = match.groups()
        if key is None:
            work = alt_work
            key = "moiraiagent2026" if r"\RepoMoirai" in line else "zhang2025llm"
        month_match = re.search(r"(?:^|\s)([A-Z][a-z]{2})'(\d{2})", metadata)
        public_month = ""
        if month_match:
            month_number = {
                "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
            }[month_match.group(1)]
            public_month = f"20{month_match.group(2)}-{month_number:02d}"
        task = metadata.split(r"\newline", 1)[-1]
        profiles.append(
            {
                "work": clean_latex(work),
                "citation_key": key,
                "public_month": public_month,
                "task_family_original": clean_latex(task),
                "work_type": "Benchmark" if r"\typeBenchshort{}" in metadata else "System-Method",
                "claimed_as_agent": "No" if r"\selfclaim{}" in metadata else "Yes",
                "general_harness_contribution": clean_latex(gh).rstrip("."),
                "general_ts_harness_contribution": clean_latex(gts).rstrip("."),
                "task_specific_harness_contribution": clean_latex(tsk).rstrip("."),
            }
        )
    return profiles


def infer_modules(profile: dict[str, str]) -> list[str]:
    text = " ".join(
        profile[field]
        for field in (
            "general_harness_contribution",
            "general_ts_harness_contribution",
            "task_specific_harness_contribution",
        )
    ).casefold()
    return [name for name, pattern in MODULE_RULES.items() if re.search(pattern, text)]


def infer_task_axes(task: str, contribution: str) -> tuple[dict[str, str], str, str]:
    text = f"{task} {contribution}".casefold()
    flags = {
        "forecasting_reasoning": bool(re.search(r"forecast|predict|reason|qa|question|inference|classif|interpret", text)),
        "augmentation_synthesis": bool(re.search(r"augment|synth|generat|annotation|caption|curat|construct", text)),
        "anomaly_detection_diagnosis": bool(re.search(r"anomal|diagnos|root.cause|fault|incident", text)),
        "decision_support": bool(re.search(r"decision|trading|deploy|monitor|care|alert|agricultur|business|revision", text)),
    }
    unmatched = [] if any(flags.values()) else [task]
    notes = "Multi-label coding; task axes follow the four task-oriented survey families."
    return ({name: "Yes" if value else "No" for name, value in flags.items()}, "; ".join(unmatched), notes)


def load_bib() -> dict[str, dict[str, str]]:
    with BIB_PATH.open(encoding="utf-8") as handle:
        return {entry["ID"]: entry for entry in bibtexparser.load(handle).entries}


def load_arxiv_dates() -> dict[str, str]:
    metadata = ROOT / "references" / "official" / "arxiv.jsonl"
    dates = {}
    with metadata.open(encoding="utf-8") as handle:
        for line in handle:
            item = json.loads(line)
            if item.get("arxiv_id") and item.get("published"):
                dates[item["arxiv_id"]] = item["published"][:10]
    return dates


def bootstrap(_: argparse.Namespace) -> None:
    legacy = {row["citation_key"]: row for row in read_csv(LEGACY_LEDGER)}
    screening = {row["citation_key"]: row for row in read_csv(SCREENING_AUDIT)}
    manifest = {row["citation_key"]: row for row in read_csv(REFERENCE_MANIFEST)}
    bib = load_bib()
    arxiv_dates = load_arxiv_dates()
    rows = []
    for profile in parse_profiles():
        key = profile["citation_key"]
        old = legacy.get(key, {})
        screen = screening.get(key, {})
        ref = manifest.get(key, {})
        entry = bib.get(key, {})
        locus = LOCUS_OVERRIDES.get(
            key, old.get("primary_locus") or screen.get("proposed_locus") or "REVIEW"
        )
        locus_field = {
            "GH": "general_harness_contribution",
            "GTS": "general_ts_harness_contribution",
            "TSK": "task_specific_harness_contribution",
        }.get(locus)
        primary = profile.get(locus_field, "") if locus_field else ""
        flags, other, task_notes = infer_task_axes(
            profile["task_family_original"], profile["task_specific_harness_contribution"]
        )
        modules = infer_modules(profile)
        exact_date = arxiv_dates.get(ref.get("arxiv_id", ""), screen.get("first_public_date", ""))
        public_month = profile["public_month"] or old.get("public_month", "")
        if exact_date:
            precision = "day"
        elif public_month:
            precision = "month"
        elif entry.get("year"):
            precision = "year"
        else:
            precision = "unknown"
        row = {field: "" for field in FIELDS}
        row.update(profile)
        row.update(
            {
                "paper_title": entry.get("title", ref.get("title_bib", "")),
                "authors": entry.get("author", ref.get("authors_bib", "")),
                "bib_year": entry.get("year", ref.get("year_bib", "")),
                "first_public_date": exact_date,
                "public_month": public_month,
                "publication_date_precision": precision,
                "doi": ref.get("doi", entry.get("doi", "")),
                "arxiv_id": ref.get("arxiv_id", ""),
                "landing_url": ref.get("landing_url", ""),
                "paper_claim_summary": primary,
                "llm_component_contribution": "",
                "claim_evidence_basis": "Maintained work-level mechanism profile in main.tex; direct paper locator pending",
                "claim_review_status": "survey_coded",
                "primary_locus": locus,
                "primary_contribution": primary,
                "harness_modules": "; ".join(modules),
                "harness_module_coding_basis": "Keyword-assisted mapping to harness_component_catalog.csv; human review required",
                "task_axis_forecasting_reasoning": flags["forecasting_reasoning"],
                "task_axis_augmentation_synthesis": flags["augmentation_synthesis"],
                "task_axis_anomaly_detection_diagnosis": flags["anomaly_detection_diagnosis"],
                "task_axis_decision_support": flags["decision_support"],
                "task_axis_other": other,
                "task_axis_notes": task_notes,
                "agent_claim_evidence": old.get("agent_claim_evidence", screen.get("evidence_basis", "")),
                "included_as": old.get("included_as", screen.get("decision", "maintained_corpus")),
                "identity_status": ref.get("identity_status", ""),
                "scholar_status": ref.get("scholar_status", "pending"),
                "scholar_checked_at": ref.get("scholar_checked_at", ""),
                "scholar_bib_path": ref.get("scholar_bib_path", ""),
                "bib_sync_status": "matched" if entry and ref else "review",
            }
        )
        rows.append(row)
    write_csv(rows)
    generate_json(rows)
    print(f"bootstrapped {len(rows)} records into {LEDGER.name}")


def generate_json(rows: list[dict[str, str]]) -> None:
    def parse_json_field(row: dict[str, str], field: str, default):
        raw = row.get(field, "")
        if not raw:
            return default
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return default

    output = []
    for row in rows:
        llm_subdimensions = parse_json_field(row, "llm_side_subdimensions", [])
        general_dimensions = derive_general_dimensions(row)
        general_ts_dimensions = derive_temporal_dimensions(row)
        gts_reason = parse_json_field(row, "general_ts_specificity_reason", [])
        task_modules = derive_task_dimensions(row, general_ts_dimensions)
        exclusive_gh, exclusive_gts, task_modules = exclusive_harness_layers(
            general_dimensions, general_ts_dimensions, task_modules
        )
        module_contributions = parse_json_field(
            row, "module_level_contributions_json", module_contribution_record(row)
        )
        llm_summary = row.get("llm_component_contribution", "")
        gts_review = row.get("taxonomy_review_status", "survey_coded_needs_pdf_review")
        output.append(
            {
                "work": row["work"],
                "citation": {
                    "key": row["citation_key"],
                    "title": row["paper_title"],
                    "authors": row["authors"],
                    "year": row["bib_year"],
                    "doi": row["doi"] or None,
                    "arxiv_id": row["arxiv_id"] or None,
                    "landing_url": row["landing_url"] or None,
                    "identity_status": row["identity_status"],
                    "scholar": {
                        "status": row["scholar_status"],
                        "checked_at": row["scholar_checked_at"] or None,
                        "receipt": row["scholar_bib_path"] or None,
                    },
                },
                "publication": {
                    "first_public_date": row["first_public_date"] or None,
                    "public_month": row["public_month"] or None,
                    "precision": row["publication_date_precision"],
                },
                "claim": {
                    "summary": row["paper_claim_summary"],
                    "evidence_basis": row["claim_evidence_basis"],
                    "review_status": row["claim_review_status"],
                },
                "source_evidence": json.loads(row["source_evidence_json"]) if row.get("source_evidence_json") else [],
                "harness": {
                    "primary_locus": row["primary_locus"],
                    "primary_contribution": row["primary_contribution"],
                    "modules": [part.strip() for part in row["harness_modules"].split(";") if part.strip()],
                    "contributions": {
                        "GH": row["general_harness_contribution"],
                        "GTS": row["general_ts_harness_contribution"],
                        "TSK": row["task_specific_harness_contribution"],
                    },
                },
                "tasks": {
                    "source_label": row["task_family_original"],
                    "axes": [name for name in TASK_AXES if row[f"task_axis_{name}"] == "Yes"],
                    "other": row["task_axis_other"] or None,
                },
                "work_type": row["work_type"],
                "claimed_as_agent": row["claimed_as_agent"] == "Yes",
                "schema_version": row.get("taxonomy_schema_version") or "2.1",
                "llm_side_contribution": {
                    "present": bool(llm_summary or llm_subdimensions),
                    "subdimensions": llm_subdimensions,
                    "summary": llm_summary,
                    "source_evidence": json.loads(row["source_evidence_json"]) if row.get("source_evidence_json") else [],
                    "review_status": "paper_verified" if row.get("claim_review_status") == "paper_verified" else ("survey_coded_needs_pdf_review" if llm_summary else "not_recorded"),
                },
                "general_harness_modules": {
                    "dimensions": exclusive_gh,
                    "inclusive_dimensions": general_dimensions,
                    "source_dimensions": parse_json_field(row, "general_harness_dimensions", {}),
                    "dimension_coding_basis": "derived_from_explicit_harness_modules",
                    "claim": row["general_harness_contribution"],
                    "source_evidence": json.loads(row["source_evidence_json"]) if row.get("source_evidence_json") else [],
                    "review_status": "paper_verified" if row.get("claim_review_status") == "paper_verified" else "survey_coded_needs_pdf_review",
                },
                "general_ts_harness_modules": {
                    "dimensions": exclusive_gts,
                    "inclusive_dimensions": general_ts_dimensions,
                    "source_dimensions": parse_json_field(row, "general_ts_harness_dimensions", {}),
                    "dimension_coding_basis": "derived_from_temporal_specificity_reason_and_claim",
                    "claim": row["general_ts_harness_contribution"],
                    "ts_specificity_reason": gts_reason,
                    "source_evidence": json.loads(row["source_evidence_json"]) if row.get("source_evidence_json") else [],
                    "review_status": "paper_verified" if row.get("claim_review_status") == "paper_verified" else ("needs_pdf_reclassification" if row["general_ts_harness_contribution"] else "not_recorded"),
                },
                "task_specific_modules": task_modules,
                "module_level_contributions": module_contributions,
                "taxonomy_review_status": row.get("taxonomy_review_status") or "survey_coded_needs_pdf_review",
            }
        )
    JSON_LEDGER.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync(_: argparse.Namespace) -> None:
    rows = read_csv(LEDGER)
    manifest = {row["citation_key"]: row for row in read_csv(REFERENCE_MANIFEST)}
    bib = load_bib()
    arxiv_dates = load_arxiv_dates()
    for row in rows:
        key = row["citation_key"]
        ref = manifest.get(key, {})
        entry = bib.get(key, {})
        for target, source, fallback in (
            ("paper_title", "title", "title_bib"),
            ("authors", "author", "authors_bib"),
            ("bib_year", "year", "year_bib"),
        ):
            row[target] = entry.get(source, ref.get(fallback, row[target]))
        for field in (
            "doi", "arxiv_id", "landing_url", "identity_status", "scholar_status",
            "scholar_checked_at", "scholar_bib_path",
        ):
            row[field] = ref.get(field, row[field])
        official_date = arxiv_dates.get(ref.get("arxiv_id", ""))
        if official_date:
            row["first_public_date"] = official_date
            row["public_month"] = official_date[:7]
            row["publication_date_precision"] = "day"
        row["bib_sync_status"] = "matched" if entry and ref else "review"
        row["module_level_contributions_json"] = json.dumps(
            module_contribution_record(row), ensure_ascii=False, sort_keys=True
        )
        row["taxonomy_schema_version"] = "2.1"
    write_csv(rows)
    generate_json(rows)
    print(f"synchronized Bib and manifest metadata for {len(rows)} records")


def validate(_: argparse.Namespace) -> None:
    rows = read_csv(LEDGER)
    bib = load_bib()
    manifest = {row["citation_key"]: row for row in read_csv(REFERENCE_MANIFEST)}
    catalog_names = {row["component_name"] for row in read_csv(CATALOG)}
    errors = []
    warnings = []
    keys = [row["citation_key"] for row in rows]
    if len(keys) != len(set(keys)):
        errors.append("duplicate citation keys in classification ledger")
    for row in rows:
        key = row["citation_key"]
        repo_only = manifest.get(key, {}).get("source_kind") == "github" and manifest.get(key, {}).get("pdf_expected", "").lower() == "false"
        if key not in bib and not repo_only:
            errors.append(f"{key}: missing from production BibTeX")
        if key not in manifest:
            errors.append(f"{key}: missing from reference manifest")
        if row["primary_locus"] not in {"GH", "GTS", "TSK"}:
            errors.append(f"{key}: invalid primary_locus={row['primary_locus']}")
        if not row["paper_claim_summary"]:
            errors.append(f"{key}: missing paper_claim_summary")
        if not row["primary_contribution"]:
            errors.append(f"{key}: missing primary_contribution")
        modules = {part.strip() for part in row["harness_modules"].split(";") if part.strip()}
        unknown = modules - catalog_names
        if unknown:
            errors.append(f"{key}: unknown Harness modules: {sorted(unknown)}")
        if not modules:
            warnings.append(f"{key}: no Harness module assigned")
        if not any(row[f"task_axis_{name}"] == "Yes" for name in TASK_AXES) and not row["task_axis_other"]:
            warnings.append(f"{key}: no task axis assigned")
        ref = manifest.get(key, {})
        if ref and row["scholar_status"] != ref.get("scholar_status", ""):
            errors.append(f"{key}: Scholar status differs from reference manifest")
    profile_keys = {row["citation_key"] for row in parse_profiles()}
    if set(keys) != profile_keys:
        warnings.append(
            f"ledger/profile key mismatch: ledger_only={sorted(set(keys)-profile_keys)}, "
            f"profile_only={sorted(profile_keys-set(keys))}"
        )
    locus = Counter(row["primary_locus"] for row in rows)
    generate_json(rows)
    task_counts = Counter()
    for row in rows:
        for name in TASK_AXES:
            if row[f"task_axis_{name}"] == "Yes":
                task_counts[name] += 1
    report = [
        "# Classification ledger audit",
        "",
        f"- Records: {len(rows)}",
        f"- Unique citation keys: {len(set(keys))}",
        f"- Primary loci: {dict(sorted(locus.items()))}",
        f"- Multi-label task-axis counts: {dict(sorted(task_counts.items()))}",
        f"- BibTeX keys matched: {sum(key in bib for key in keys)}/{len(rows)}",
        f"- Reference manifest keys matched: {sum(key in manifest for key in keys)}/{len(rows)}",
        "- Corpus completeness: not assessed by this structural validation",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        "",
        "## Errors",
        "",
        *(errors or ["None."]),
        "",
        "## Warnings",
        "",
        *(warnings or ["None."]),
    ]
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    if errors:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    subparsers.add_parser("bootstrap").set_defaults(func=bootstrap)
    subparsers.add_parser("sync").set_defaults(func=sync)
    subparsers.add_parser("validate").set_defaults(func=validate)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
