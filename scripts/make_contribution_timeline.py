#!/usr/bin/env python3
"""Render the module-level contribution timeline from the classification ledger."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "paper_classification_ledger.json"
OUT_PNG = ROOT / "artifacts" / "contribution_timeline.png"
OUT_CSV = ROOT / "artifacts" / "module_contribution_timeline.csv"


def count_dimensions(value: dict) -> int:
    dimensions = value.get("dimensions", value) if isinstance(value, dict) else {}
    return sum(len(labels) for labels in dimensions.values() if isinstance(labels, list))


def contribution_counts(record: dict) -> dict[str, int]:
    module = record.get("module_level_contributions", {})
    llm = module.get("llm_side", [])
    task = module.get("task_specific", {})
    return {
        "LLM-side": len(llm) if isinstance(llm, list) else 0,
        "General Harness": count_dimensions(module.get("general_harness", {})),
        "General Time-Series Harness": count_dimensions(module.get("general_ts_harness", {})),
        "Task-Specific Harness": sum(count_dimensions(item) for item in task.values() if isinstance(item, dict)),
    }


def main() -> None:
    records = json.loads(LEDGER.read_text(encoding="utf-8"))
    monthly: dict[str, Counter] = {}
    for record in records:
        month = record.get("publication", {}).get("public_month")
        if month and len(month) == 4 and month.isdigit():
            # Year-only records are plotted at January and remain marked as
            # year precision in the ledger; this keeps them visible without
            # inventing a month in the source metadata.
            month = f"{month}-01"
        if month and not (len(month) == 7 and month[4] == "-" and month[:4].isdigit() and month[5:].isdigit()):
            year = record.get("publication", {}).get("first_public_date")
            month = f"{year}-01" if year and len(year) == 4 and year.isdigit() else None
        if not month:
            continue
        monthly.setdefault(month, Counter()).update(contribution_counts(record))

    months = sorted(monthly)
    running = Counter()
    rows = []
    cumulative = {name: [] for name in contribution_counts(records[0])}
    for month in months:
        running.update(monthly[month])
        row = {"public_month": month}
        for name in cumulative:
            cumulative[name].append(running[name])
            row[name] = running[name]
        rows.append(row)

    OUT_CSV.write_text("", encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["public_month", *cumulative])
        writer.writeheader()
        writer.writerows(rows)

    dates = [datetime.strptime(month, "%Y-%m") for month in months]
    colors = {
        "General Harness": "#1f4e79",
        "General Time-Series Harness": "#c88719",
        "Task-Specific Harness": "#2f7d5c",
        "LLM-side": "#7851a9",
    }
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10})
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    # Keep all four layers in one plot. GH and GTS can legitimately share the
    # same cumulative value when one module has both labels; hollow GH markers
    # keep that independently counted curve visible in print.
    ax.plot(dates, cumulative["General Time-Series Harness"], lw=2.5, label="General Time-Series Harness", color=colors["General Time-Series Harness"], zorder=2)
    ax.plot(dates, cumulative["Task-Specific Harness"], lw=2.5, label="Task-Specific Harness", color=colors["Task-Specific Harness"], zorder=3)
    ax.plot(dates, cumulative["LLM-side"], lw=2.5, label="LLM-side", color=colors["LLM-side"], zorder=4)
    ax.plot(
        dates,
        cumulative["General Harness"],
        lw=1.8,
        ls="--",
        dashes=(5, 2),
        marker="o",
        markevery=max(1, len(dates) // 10),
        ms=4.5,
        mfc="white",
        mec=colors["General Harness"],
        label="General Harness",
        color=colors["General Harness"],
        zorder=5,
    )
    ax.set_title("Module-level contributions across the reviewed corpus")
    ax.set_yscale("log")
    ax.set_ylabel("Cumulative module annotations (log scale)")
    ax.legend(frameon=False, ncol=2, loc="upper left", fontsize=8.5)
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    fig.autofmt_xdate(rotation=0, ha="center")
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
