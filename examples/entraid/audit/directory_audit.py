"""
Report directory audit log activity over a time window.

Shows every audited directory operation (users, groups, apps, roles) with
who initiated it — a general compliance report, broader than the
group-membership-specific example.

Requires delegated permission ``AuditLog.Read.All``.

https://learn.microsoft.com/en-us/graph/api/directoryaudit-list
"""

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Report directory audit activity")
    parser.add_argument("--days", type=int, default=7, help="number of days to look back (default 7)")
    parser.add_argument(
        "--category", default=None, help="only show this category (e.g. UserManagement, GroupManagement)"
    )
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=args.days)
    audit_logs = (
        client.audit_logs.directory_audits.filter(
            f"activityDateTime ge {start.strftime('%Y-%m-%dT%H:%M:%SZ')} and "
            f"activityDateTime le {end.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        )
        .get()
        .execute_query()
    )

    if args.category:
        audit_logs = [log for log in audit_logs if (log.category or "").lower() == args.category.lower()]

    print(f"Directory audit activity, last {args.days} day(s) ({len(audit_logs)}):")
    for log in audit_logs:
        initiated = log.initiated_by.user_principal_name or "?"
        print(
            f"  {log.activity_datetime:%Y-%m-%d %H:%M}  {log.activity_display_name or '?':40s}  "
            f"{log.category or '?':20s}  by {initiated}"
        )


if __name__ == "__main__":
    main()
