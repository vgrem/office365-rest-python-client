"""File scanner — file-size limits that need special handling."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.runtime.limits import hint


class FileScanner(BaseScanner):
    """Flags files exceeding the size limit."""

    category = "file"

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        limit = self.options.limit("large_file_bytes")
        for item in target.entity:
            path = item.properties.get("FileRef", "")
            size = (item.file.length if getattr(item, "file", None) is not None else None) or 0
            if size > limit.value:
                self.flag(
                    report,
                    "warning",
                    path,
                    hint(limit, value=size, context="file"),
                    "Use chunked upload or split the file",
                    limit=limit,
                )
