"""Outlook (mail) assessment for the migration toolkit.

Reuses the shared assessment model (containers, scans, reports, export); the
product-specific part is the mailbox walker (:class:`MailboxAssessor`) and its
scanners (e.g. the ``MailFolders`` folder inventory).
"""

from office365.migration.outlook.assessor import MailboxAssessor
from office365.migration.outlook.registry import OUTLOOK_SCANS, outlook_scan_pairs
from office365.migration.outlook.scanner import MailboxFolderRecord, MailboxFolderScan, MailFolderData, OutlookOptions

__all__ = [
    "OUTLOOK_SCANS",
    "MailFolderData",
    "MailboxAssessor",
    "MailboxFolderRecord",
    "MailboxFolderScan",
    "OutlookOptions",
    "outlook_scan_pairs",
]
