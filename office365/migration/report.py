"""Migration reports — SPMT-style summary, item, and failure exports.

Builds records from the job's existing state (:class:`MigrationStats`, the
manifest's per-item status, and the checkpoint) and exports them as CSV and JSON
through the records interchange — the same neutral form the data pipeline uses
for collections.
"""

from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from office365.migration.job import MigrationJob


@dataclass
class MigrationReport:
    """Record sets for a migration run (one summary row, per-item rows)."""

    summary: List[Dict[str, object]] = field(default_factory=list)
    items: List[Dict[str, object]] = field(default_factory=list)
    failures: List[Dict[str, object]] = field(default_factory=list)


def build_report(job: "MigrationJob") -> MigrationReport:
    """Project a job's state into report records."""
    stats = job.stats
    summary = [
        {
            "source": job.source_label,
            "destination": job.target_label,
            "status": job.phase.value,
            "total_items": stats.total,
            "success": stats.success,
            "skipped": stats.skipped,
            "errors": stats.errors,
            "bytes_transferred": stats.bytes_transferred,
            "started_at": _iso(job.started_at),
            "finished_at": _iso(job.finished_at),
            "duration_secs": round(job.duration, 1) if job.duration is not None else None,
        }
    ]
    items = [
        {
            "source_path": item.source_path,
            "destination_path": item.dest_path,
            "size_bytes": item.size_bytes,
            "item_type": item.item_type,
            "status": item.status.value,
            "error": item.error or "",
        }
        for item in job.manifest.items
    ]
    failures = [row for row in items if row["status"] == "failed"]
    return MigrationReport(summary=summary, items=items, failures=failures)


def export_reports(job: "MigrationJob", output_dir: str | Path) -> List[str]:
    """Write SummaryReport, ItemReport, and FailureReport (CSV + JSON).

    Mirrors SPMT: the failure report is only written when failures exist.

    Args:
        job: The migration job to report on.
        output_dir: Directory to write the report files into.

    Returns:
        List of written file paths.
    """
    report = build_report(job)
    os.makedirs(output_dir, exist_ok=True)
    written: List[str] = []
    for name, records in (
        ("SummaryReport", report.summary),
        ("ItemReport", report.items),
        ("FailureReport", report.failures),
    ):
        if not records:
            continue
        written += _write(name, records, output_dir)
    return written


def _write(name: str, records: List[Dict[str, object]], output_dir: str | Path) -> List[str]:
    csv_path = os.path.join(output_dir, f"{name}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

    json_path = os.path.join(output_dir, f"{name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return [csv_path, json_path]


def _iso(value) -> str:
    if value is None:
        return ""
    return value.isoformat(timespec="seconds")
