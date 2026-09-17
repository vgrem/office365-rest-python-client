"""Assessment report export — write the issues and per-scan detail reports.

Uses the report's records form (:meth:`AssessmentReport.to_records`) and the
per-scan detail records (:attr:`AssessmentReport.scan_reports`), so the report
model stays format-agnostic while the caller gets the downloadable
assessment. Scan detail files land in a ``ScannerReports`` subfolder, mirroring
SMAT's output layout (``<ScanName>-detail.csv``).
"""

from __future__ import annotations

import os
from pathlib import Path

from office365.migration.assessment.report import AssessmentReport
from office365.migration.report_io import write_formats

_COLUMNS = ["severity", "category", "location", "message", "suggestion"]


def export_assessment(report: AssessmentReport, output_dir: str | Path) -> list[str]:
    """Write the aggregate issues plus each scan's detail report.

    Args:
        report: The assessment result.
        output_dir: Directory to write the files into.

    Returns:
        List of written file paths.
    """
    written = write_formats(report.to_records(), output_dir, "AssessmentReport", columns=_COLUMNS)
    written += export_scan_reports(report, output_dir)
    return written


def export_scan_reports(report: AssessmentReport, output_dir: str | Path) -> list[str]:
    """Write each scan's SMAT-style detail report (``ScannerReports/<Scan>-detail``).

    Only scans that produced rows are written. Returns the written paths.
    """
    written: list[str] = []
    for scan in report.scan_reports.values():
        if not scan.records:
            continue
        written += write_formats(
            scan.to_records(),
            os.path.join(output_dir, "ScannerReports"),
            f"{scan.name}-detail",
            columns=list(scan.columns),
        )
    return written
