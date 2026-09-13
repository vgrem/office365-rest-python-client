"""Outlook (mail) assessor — walks a user's mailbox folders and runs the scans.

The first non-SharePoint product slice: instead of walking a web/list tree, the
walker enumerates the mailbox's mail-folder tree (``mailFolders`` ->
``childFolders``), builds ``MAIL_FOLDER`` payloads with the folder's counts and
dispatches to the registered scans. Reuses the shared :class:`AssessmentReport`
/ :class:`ScanReport` / issue model and exporters.
"""

from __future__ import annotations

from office365.migration._util import coerce_int
from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.runner import ScanRunner
from office365.migration.outlook.registry import outlook_scan_pairs
from office365.migration.outlook.scanner import MailFolderData, OutlookOptions

# Graph mailFolder properties the walker selects
_FOLDER_COLUMNS = ["displayName", "totalItemCount", "unreadItemCount", "childFolderCount"]


class MailboxAssessor:
    """Assesses a user's mailbox — folder inventory with large-folder flags.

    Example:
        >>> report = MailboxAssessor(client.me).assess()
        >>> print(report.scan_report(MailboxFolderScan).to_csv())
    """

    def __init__(self, user, options: OutlookOptions | None = None) -> None:
        self._user = user
        self._options = options or OutlookOptions()
        self.folder_count = 0
        self.message_count = 0

    def assess(self, progress=None) -> AssessmentReport:
        """Scan the user's mail-folder tree (eager, Graph reads only)."""
        runner = ScanRunner(outlook_scan_pairs(self._options))
        report = runner.report

        def _walk(folders, parent_path: str) -> None:
            for folder in folders:
                name = folder.display_name or folder.id
                path = f"{parent_path}/{name}" if parent_path else name
                folder_data = MailFolderData(
                    path=path,
                    item_count=coerce_int(folder.total_item_count),
                    unread_count=coerce_int(folder.unread_item_count),
                    child_count=coerce_int(folder.child_folder_count),
                )
                self.folder_count += 1
                self.message_count += folder_data.item_count or 0
                runner.dispatch(ScanContainer.MAIL_FOLDER, folder_data, path)
                try:
                    children = folder.child_folders.select(_FOLDER_COLUMNS).get().execute_query()
                except Exception as e:  # noqa: BLE001 — unreadable subtree is a warning, not fatal
                    runner.flag_access(path, e)
                    continue
                if children:
                    _walk(children, path)

        try:
            root_folders = self._user.mail_folders.select(_FOLDER_COLUMNS).get().execute_query()
        except Exception as e:  # noqa: BLE001
            runner.flag_access("mailbox", e)
            root_folders = []

        if root_folders:
            _walk(root_folders, "")

        runner.collect()
        return report
