"""Path scanner — SharePoint path/name constraints that block a migration."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.runtime.limits import hint


class PathScanner(BaseScanner):
    """Flags path/name length overruns and invalid characters."""

    category = "path"

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        path_limit = self.options.limit("max_path_length")
        name_limit = self.options.limit("max_name_length")
        for item in target.entity:
            path = item.properties.get("FileRef", "")
            name = item.properties.get("FileLeafRef", "")

            if len(path) > path_limit.value:
                self.flag(
                    report,
                    "blocker",
                    path,
                    hint(path_limit, value=len(path), context="path"),
                    "Shorten folder names or restructure hierarchy",
                    limit=path_limit,
                )

            if len(name) > name_limit.value:
                self.flag(
                    report,
                    "blocker",
                    path,
                    hint(name_limit, value=len(name), context="file name"),
                    "Rename file before migration",
                    limit=name_limit,
                )

            bad = [c for c in name if c in self.options.invalid_chars]
            if bad:
                self.flag(
                    report,
                    "blocker",
                    path,
                    f"File name contains invalid chars: {bad}",
                    "Rename file — remove invalid characters",
                )
