"""Checked-out files scan — the SMAT ``CheckedOutFiles`` report.

Only checked-in content is migrated: a file a user has checked out is read as its
last checked-in version, so uncommitted edits are lost. This ``ITEMS``-container
report lists the files that are checked out and by whom, and raises a per-list
warning (data-loss risk).
"""

from __future__ import annotations

from dataclasses import dataclass

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.migration.sharepoint.scanners.smat import SiteScanRecord, site_url


@dataclass
class CheckedOutFilesRecord(SiteScanRecord):
    """One row of the SMAT ``CheckedOutFiles-detail`` report."""

    File: str | None = None
    CheckedOutUser: str | None = None
    ScanID: str | None = None


class CheckedOutFilesScanner(BaseScanner[CheckedOutFilesRecord]):
    """Reports checked-out files (SMAT ``CheckedOutFiles``) and warns per list."""

    category = "file"
    scan_name = "CheckedOutFiles"
    record_type = CheckedOutFilesRecord

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        page: list[CheckedOutFilesRecord] = []
        for item in target.entity:
            file = getattr(item, "file", None)
            if file is None or not file.check_out_type:
                continue  # 0/None = not checked out
            user = file.checked_out_by_user
            page.append(
                CheckedOutFilesRecord(
                    SiteURL=site_url(target.location),
                    File=item.properties.get("FileRef", ""),
                    CheckedOutUser=(user.login_name or user.title) if user is not None else None,
                    ScanID=report.scan_id or None,
                )
            )
        if page:
            self.records.extend(page)
            self.flag(
                report,
                "warning",
                target.location or "list",
                f"{len(page)} checked-out file(s) — only the last checked-in version migrates",
                "Ask users to check in their files before migrating",
            )
