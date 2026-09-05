"""Migration reports — summary, item, and failure exports.

Builds records from the job's existing state (:class:`MigrationStats`, the
manifest's per-item status, and the checkpoint) and exports them as CSV and JSON
through the records interchange — the same neutral form the data pipeline uses
for collections.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from office365.migration._util import iso, write_csv_json

if TYPE_CHECKING:
    from office365.migration.job import MigrationJob


@dataclass
class MigrationReport:
    """Record sets for a migration run (one summary row, per-item rows)."""

    summary: list[dict[str, object]] = field(default_factory=list)
    items: list[dict[str, object]] = field(default_factory=list)
    failures: list[dict[str, object]] = field(default_factory=list)


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
            "started_at": iso(job.started_at),
            "finished_at": iso(job.finished_at),
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


def export_reports(job: "MigrationJob", output_dir: str | Path) -> list[str]:
    """Write SummaryReport, ItemReport, and FailureReport (CSV + JSON).

    The failure report is only written when failures exist.

    Args:
        job: The migration job to report on.
        output_dir: Directory to write the report files into.

    Returns:
        List of written file paths.
    """
    report = build_report(job)
    written: list[str] = []
    for name, records in (
        ("SummaryReport", report.summary),
        ("ItemReport", report.items),
        ("FailureReport", report.failures),
    ):
        if not records:
            continue
        written += write_csv_json(output_dir, name, records)
    return written
