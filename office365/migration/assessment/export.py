"""Assessment report export — write the issues and per-scan detail reports.

Uses the report's records form (:meth:`AssessmentReport.to_records`) and the
per-scan detail records (:attr:`AssessmentReport.scan_reports`), so the report
model stays format-agnostic while the caller gets the downloadable
assessment. Scan detail files land in a ``ScannerReports`` subfolder, mirroring
SMAT's output layout (``<ScanName>-detail.csv``).
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import List

from office365.migration.assessment.report import AssessmentReport

_COLUMNS = ["severity", "category", "location", "message", "suggestion"]


def export_assessment(report: AssessmentReport, output_dir: str | Path) -> List[str]:
    """Write the aggregate issues plus each scan's detail report.

    Args:
        report: The assessment result.
        output_dir: Directory to write the files into.

    Returns:
        List of written file paths.
    """
    written = _write_csv_json(
        output_dir,
        "AssessmentReport",
        _COLUMNS,
        report.to_records(),
    )
    written += export_scan_reports(report, output_dir)
    return written


def export_scan_reports(report: AssessmentReport, output_dir: str | Path) -> List[str]:
    """Write each scan's SMAT-style detail report (``ScannerReports/<Scan>-detail``).

    Only scans that produced rows are written. Returns the written paths.
    """
    written: List[str] = []
    for scan in report.scan_reports.values():
        if not scan.records:
            continue
        written += _write_csv_json(
            os.path.join(output_dir, "ScannerReports"),
            f"{scan.name}-detail",
            list(scan.columns),
            scan.to_records(),
        )
    return written


def _write_csv_json(dir_: str | Path, stem: str, columns: list[str], records: list[dict]) -> List[str]:
    os.makedirs(dir_, exist_ok=True)
    csv_path = os.path.join(str(dir_), f"{stem}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, restval="n/a")
        writer.writeheader()
        writer.writerows(records)

    json_path = os.path.join(str(dir_), f"{stem}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return [csv_path, json_path]
