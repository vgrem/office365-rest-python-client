"""File scanner — file-size limits that need special handling."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner


class FileScanner(BaseScanner):
    """Flags files exceeding the size limit."""

    category = "file"

    def on_items(self, items, report: AssessmentReport, location: str = "") -> None:
        for item in items:
            path = item.properties.get("FileRef", "")
            size = (item.file.length if getattr(item, "file", None) is not None else None) or 0
            if size > self.options.large_file_bytes:
                self.flag(
                    report,
                    "warning",
                    path,
                    f"File size {size / 1024 / 1024 / 1024:.1f}GB exceeds the size limit",
                    "Use chunked upload or split the file",
                )
