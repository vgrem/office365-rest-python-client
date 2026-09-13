"""Outlook (mail) assessment scanner — mailbox folder inventory.

The first Outlook product scanner: per mail folder it reports the folder path
and item/unread/child counts (SMAT ``LargeSites``-style typed rows) and flags
folders above a large-folder item threshold (migration pagination/throughput
risk). Driven by the :class:`MailboxAssessor` walker over ``MAIL_FOLDER``
container payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import (
    AssessmentOptions,
    BaseScanner,
    ScanTarget,
)

_LARGE_FOLDER_ITEMS = 100_000


@dataclass
class OutlookOptions(AssessmentOptions):
    """Mail-assessment options (SharePoint options plus Outlook thresholds)."""

    large_folder_items: int = _LARGE_FOLDER_ITEMS  # folders above this are flagged


@dataclass
class MailFolderData:
    """A MAIL_FOLDER payload handed to the folder scan (plain, testable data)."""

    path: str
    item_count: int | None = 0
    unread_count: int | None = 0
    child_count: int | None = 0


@dataclass
class MailboxFolderRecord:
    """One row of the ``MailFolders`` detail report (field names ARE the columns)."""

    FolderPath: str | None = None
    ItemCount: int | None = None
    UnreadItemCount: int | None = None
    ChildFolderCount: int | None = None


class MailboxFolderScan(BaseScanner[MailboxFolderRecord]):
    """MAIL_FOLDER-container scan: folder inventory + large-folder flags."""

    category = "mail"
    scan_name = "MailFolders"
    record_type = MailboxFolderRecord
    container = ScanContainer.MAIL_FOLDER

    def run(self, target: ScanTarget[MailFolderData], report: AssessmentReport) -> None:
        folder = target.entity
        item_count = int(folder.item_count or 0)
        unread = int(folder.unread_count or 0)
        child_count = int(folder.child_count or 0)
        self.records.append(
            MailboxFolderRecord(
                FolderPath=folder.path,
                ItemCount=item_count,
                UnreadItemCount=unread,
                ChildFolderCount=child_count,
            )
        )
        options = cast(OutlookOptions, self.options)
        if item_count > options.large_folder_items:
            self.flag(
                report,
                "warning",
                folder.path,
                f"Folder contains {item_count:,} items — large mailboxes are slower and riskier to migrate",
                "Archive or split the folder, then re-scan",
            )
