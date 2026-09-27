"""Thicket folders scan — the SPMT ``THICKET_FOLDER_UNSUPPORTED`` risk.

Folders whose name ends in ``_file`` or ``_files`` are treated as *thicket*
folders — the hidden linked folder SharePoint creates to store the supporting
content of an HTM file. SharePoint in Microsoft 365 can't create them, so a
migration carrying such a folder fails. This ``ITEMS``-container scan flags each
one so it can be renamed first.
"""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget

#: Folder-name suffixes SharePoint treats as thicket folders.
_THICKET_SUFFIXES = ("_file", "_files")


class ThicketFolderScanner(BaseScanner):
    """Flags folders whose name ends in ``_file``/``_files``."""

    category = "file"

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        for item in target.entity:
            if getattr(item, "file", None) is not None:
                continue  # a file, not a folder
            name = item.properties.get("FileLeafRef", "")
            if not name.lower().endswith(_THICKET_SUFFIXES):
                continue
            self.flag(
                report,
                "blocker",
                item.properties.get("FileRef", "") or name,
                f"Thicket folder '{name}' isn't supported in SharePoint in Microsoft 365",
                "Rename the folder so it no longer ends in '_file'/'_files'",
                risk_code="THICKET_FOLDER_UNSUPPORTED",
            )
