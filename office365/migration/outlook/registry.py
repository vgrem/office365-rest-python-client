"""Outlook scan registry — the product-scoped ScanDefinitions.

Outlook scans live in their own registry (SharePoint scans live in
``office365.migration.sharepoint.registry``);
:class:`~office365.migration.outlook.assessor.MailboxAssessor` consumes it via
:func:`outlook_scan_pairs`.
"""

from __future__ import annotations

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.registry import ScanDefinition, scan_pairs
from office365.migration.assessment.scanners.base import BaseScanner
from office365.migration.outlook.scanner import MailboxFolderScan, OutlookOptions

OUTLOOK_SCANS: list[ScanDefinition] = [
    ScanDefinition(
        name="MailFolders",
        scanner=MailboxFolderScan,
        container=ScanContainer.MAIL_FOLDER,
        properties={"large_folder_items": 100_000},
    ),
]


def outlook_scan_pairs(options: OutlookOptions | None = None) -> list[tuple[ScanDefinition, BaseScanner]]:
    """The enabled ``(definition, scanner)`` pairs from :data:`OUTLOOK_SCANS`."""
    return scan_pairs(OUTLOOK_SCANS, options or OutlookOptions())
