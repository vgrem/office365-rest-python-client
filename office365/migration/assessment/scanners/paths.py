"""Path scanner — SharePoint path/name constraints that block a migration."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner


class PathScanner(BaseScanner):
    """Flags path/name length overruns and invalid characters."""

    category = "path"

    def on_items(self, items, report: AssessmentReport, location: str = "") -> None:
        for item in items:
            path = item.properties.get("FileRef", "")
            name = item.properties.get("FileLeafRef", "")

            if len(path) > self.options.max_path_length:
                self.flag(
                    report,
                    "blocker",
                    path,
                    f"Path length {len(path)} exceeds SharePoint limit of {self.options.max_path_length}",
                    "Shorten folder names or restructure hierarchy",
                )

            if len(name) > self.options.max_name_length:
                self.flag(
                    report,
                    "blocker",
                    path,
                    f"File name length {len(name)} exceeds limit of {self.options.max_name_length}",
                    "Rename file before migration",
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
