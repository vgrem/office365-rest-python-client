"""
Audit group membership changes — track who was added or removed from
Microsoft 365 and security groups.

Uses directory audit logs to detect Add member to group and Remove
member from group events. Useful for compliance monitoring and detecting
unauthorized group membership modifications.

Inspired by Report-GroupMembershipChanges.PS1 from the community.

Required delegated permissions:
    AuditLog.Read.All           Read directory audit logs
    Group.Read.All              Read group display names
    User.ReadBasic.All          Resolve user display names

https://learn.microsoft.com/en-us/graph/api/resources/directoryaudit
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def query_group_membership_changes(days_back: int = 30) -> list[dict]:
    """Query directory audit logs for group membership changes.

    Args:
        days_back: How many days to look back.

    Returns:
        List of change event dicts.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days_back)

    changes = []

    try:
        audit_logs = (
            client.audit_logs.directory_audits.filter(
                f"activityDateTime ge {start.strftime('%Y-%m-%dT%H:%M:%SZ')} and "
                f"activityDateTime le {end.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            )
            .get()
            .execute_query()
        )

        target_activities = {
            "Add member to group",
            "Remove member from group",
            "Add member to role",
            "Remove member from role",
        }

        for log in audit_logs:
            activity = getattr(log, "activity_display_name", "")
            if activity not in target_activities:
                continue

            # Parse target resource (the group)
            targets = getattr(log, "target_resources", [])
            group_name = "Unknown"
            member_name = "Unknown"
            member_upn = ""

            for t in targets or []:
                ttype = getattr(t, "type", "").lower()
                if ttype == "group":
                    group_name = getattr(t, "display_name", getattr(t, "id", "Unknown"))
                elif ttype == "user":
                    member_name = getattr(t, "display_name", "Unknown")
                    member_upn = getattr(t, "user_principal_name", "")

            changes.append(
                {
                    "timestamp": getattr(log, "activity_date_time", None),
                    "activity": activity,
                    "group": group_name,
                    "member": member_name,
                    "member_upn": member_upn,
                    "initiated_by": getattr(log, "initiated_by", {})
                    .get("user", {})
                    .get("user_principal_name", "Unknown"),
                }
            )
    except Exception as e:
        print(f"  Warning: could not query audit logs: {e}")

    changes.sort(key=lambda x: x["timestamp"] or datetime.min, reverse=True)
    return changes


def main():
    print("Group membership change audit (last 30 days)\n")
    changes = query_group_membership_changes(days_back=30)

    if not changes:
        print("No group membership changes found in directory audit logs.")
        return

    print(f"Found {len(changes)} changes:\n")
    for c in changes:
        ts = c["timestamp"].strftime("%Y-%m-%d %H:%M") if c["timestamp"] else "Unknown"
        action = "➕" if "Add" in c["activity"] else "➖"
        member = c["member_upn"] or c["member"]
        print(f"  {action} {c['activity']:28s}  {member:40s}  →  {c['group']:30s}  by {c['initiated_by']}  ({ts})")


if __name__ == "__main__":
    main()
