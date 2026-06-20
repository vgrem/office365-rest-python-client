"""
Audit group membership changes — track who was added or removed from
Microsoft 365 and security groups.

Uses directory audit logs to detect group membership modifications.
Useful for compliance monitoring and detecting unauthorized changes.

Required delegated permissions:
    AuditLog.Read.All           Read directory audit logs
    Group.Read.All              Read group display names
    User.ReadBasic.All          Resolve user display names

https://learn.microsoft.com/en-us/graph/api/resources/directoryaudit
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

TARGET_ACTIVITIES = {
    "Add member to group",
    "Remove member from group",
    "Add member to role",
    "Remove member from role",
}


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=30)

    audit_logs = (
        client.audit_logs.directory_audits.filter(
            f"activityDateTime ge {start.strftime('%Y-%m-%dT%H:%M:%SZ')} and "
            f"activityDateTime le {end.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        )
        .get()
        .execute_query()
    )

    changes = []
    for log in audit_logs:
        if log.activity_display_name not in TARGET_ACTIVITIES:
            continue

        changes.append(
            {
                "timestamp": log.activity_datetime,
                "activity": log.activity_display_name,
                "group": str(next((t for t in log.target_resources if (t.type or "").lower() == "group"), "")),
                "member": str(next((t for t in log.target_resources if (t.type or "").lower() == "user"), "")),
                "initiated_by": str(log.initiated_by),
            }
        )

    if not changes:
        print("No group membership changes found in the last 30 days.")
        return

    changes.sort(key=lambda x: x["timestamp"] or datetime.min, reverse=True)

    print(f"Group membership changes (last 30 days): {len(changes)} found\n")
    for c in changes:
        ts = c["timestamp"].strftime("%Y-%m-%d %H:%M") if c["timestamp"] else "?"
        action = "[+]" if "Add" in c["activity"] else "[-]"
        print(f"  {action} {c['activity']:28s}  {c['member']:40s}  ->  {c['group']:30s}  by {c['initiated_by']}  ({ts})")


if __name__ == "__main__":
    main()
