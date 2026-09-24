"""Browser file handling scan — the SMAT ``BrowserFileHandling`` report.

The target enforces the "Strict" browser file handling setting, so ``.htm`` /
``.html`` files no longer open in the browser — users are prompted to download
them. This ``ITEMS``-container report lists the affected files.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.migration.sharepoint.scanners.smat import SiteScanRecord, file_extension, site_url

#: Extensions affected by the Strict browser file handling change.
HTML_EXTENSIONS = frozenset({".htm", ".html"})


@dataclass
class BrowserFileHandlingRecord(SiteScanRecord):
    """One row of the SMAT ``BrowserFileHandling-detail`` report."""

    File: str | None = None
    TimeCreated: datetime | None = None
    TimeModified: datetime | None = None
    ModifiedBy: str | None = None
    ScanID: str | None = None


class BrowserFileHandlingScanner(BaseScanner[BrowserFileHandlingRecord]):
    """Reports ``.htm``/``.html`` files affected by Strict browser handling."""

    category = "file"
    scan_name = "BrowserFileHandling"
    record_type = BrowserFileHandlingRecord

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        location = site_url(target.location)
        for item in target.entity:
            if file_extension(item) not in HTML_EXTENSIONS:
                continue
            file = getattr(item, "file", None)
            modified_by = file.modified_by if file is not None else None
            self.records.append(
                BrowserFileHandlingRecord(
                    SiteURL=location,
                    File=item.properties.get("FileRef", ""),
                    TimeCreated=file.time_created if file is not None else None,
                    TimeModified=file.time_last_modified if file is not None else None,
                    ModifiedBy=(modified_by.login_name or modified_by.title) if modified_by is not None else None,
                    ScanID=report.scan_id or None,
                )
            )
