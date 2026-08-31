"""Assessment report export — write the issues to CSV and JSON.

Uses the report's records form (:meth:`AssessmentReport.to_records`), so the
report model stays format-agnostic while the caller gets the SPMT-style
downloadable assessment.
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
    """Write ``AssessmentReport.csv`` and ``AssessmentReport.json``.

    Args:
        report: The assessment result.
        output_dir: Directory to write the files into.

    Returns:
        List of written file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    records = report.to_records()

    csv_path = os.path.join(output_dir, "AssessmentReport.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_COLUMNS)
        writer.writeheader()
        writer.writerows(records)

    json_path = os.path.join(output_dir, "AssessmentReport.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return [csv_path, json_path]
