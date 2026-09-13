"""
Assess a user's mailbox for migration readiness (folder inventory).

Walks the mailbox's mail-folder tree and reports each folder's item/unread/
child counts (the ``MailFolders`` scan) plus flags for folders over a large
item-count threshold. The report (issues + scan details) is written as one
``AssessmentReport.json`` under the system temp dir (``--output`` overrides).

    python scan_mailbox.py --user-id me@contoso.onmicrosoft.com

Requires delegated ``Mail.Read`` (``client.me``), or ``Mail.Read.All`` with a
``--user-id`` for app-only access.
"""

import argparse
import json
import os
import tempfile

from office365.graph_client import GraphClient
from office365.migration import MailboxAssessor, OutlookOptions
from office365.migration.assessment.report import AssessmentReport
from tests.settings import client_id, password, tenant, username

_LARGE_FOLDER_ITEMS = 100_000


def write_report(report: AssessmentReport, output_dir: str) -> str:
    """Write the assessment (issues + scan details) as one ``AssessmentReport.json``."""
    data = {
        "issues": report.to_records(),
        "scans": {name: scan.to_records() for name, scan in report.scan_reports.items()},
    }
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "AssessmentReport.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path


def main():
    parser = argparse.ArgumentParser(description="Assess a user's mailbox for migration readiness")
    parser.add_argument("--user-id", default=None, help="target user (app-only); defaults to the signed-in user")
    parser.add_argument("--output", default=tempfile.gettempdir(), help="directory for the AssessmentReport.json")
    parser.add_argument("--large-folder-items", type=int, default=_LARGE_FOLDER_ITEMS, help="large-folder threshold")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    user = client.users[args.user_id] if args.user_id else client.me

    print(f"Assessing mailbox of {args.user_id or 'signed-in user'}…", flush=True)
    assessor = MailboxAssessor(user, OutlookOptions(large_folder_items=args.large_folder_items))
    report = assessor.assess()

    print(f"Folders: {assessor.folder_count} | Items: {assessor.message_count} | Blockers: {len(report.blockers)}")
    for scan in report.scan_reports.values():
        rows = scan.to_records()
        over = [row for row in rows if (row["ItemCount"] or 0) > args.large_folder_items]
        print(f"{scan.name}: {len(rows)} folder(s), {len(over)} over {args.large_folder_items:,} items")
        for row in over:
            print(f"  - {row['FolderPath']}: {row['ItemCount']:,} items")

    for issue in report.blockers + report.warnings:
        print(f"[{issue.category}] {issue.location}: {issue.message}")
        if issue.suggestion:
            print(f"    -> {issue.suggestion}")

    print("Report:", write_report(report, args.output))


if __name__ == "__main__":
    main()
