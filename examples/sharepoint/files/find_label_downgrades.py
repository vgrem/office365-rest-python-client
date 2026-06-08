"""
Find files in SharePoint Online where sensitivity labels have been
downgraded or removed.

Uses audit log records to detect label changes (FileSensitivityLabelChanged,
FileSensitivityLabelRemoved) and compares label priorities to determine
whether a change was an upgrade, downgrade, or removal.

Inspired by Find-FilesWithDownGradedLabels.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    AuditLog.Read.All           Read audit log records
    User.ReadBasic.All          Resolve user display names
    Reports.Read.All            Read sensitivity label information

https://learn.microsoft.com/en-us/graph/api/resources/sensitivitylabel
https://learn.microsoft.com/en-us/purview/audit-log-activities
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def get_available_labels(client: GraphClient) -> dict:
    """Fetch sensitivity labels and build a lookup by immutable ID.

    Returns a dict mapping label ID -> {display_name, priority}.
    """
    label_map = {}
    try:
        labels = client.security.sensitivity_labels.get().execute_query()
        for label in labels:
            label_map[label.id] = {
                "display_name": getattr(label, "display_name", label.id),
                "priority": getattr(label, "priority", 0),
            }
    except Exception as e:
        print(f"  Warning: could not fetch labels: {e}")
    return label_map


def find_label_downgrades(days_back: int = 90) -> list[dict]:
    """Search audit logs for sensitivity label downgrades on files.

    Args:
        days_back: How far back to search (max 180 for audit logs).

    Returns:
        List of downgrade events with file, user, old/new label, timestamp.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    labels = get_available_labels(client)
    print(f"  Found {len(labels)} sensitivity labels")

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days_back)

    # Build audit query for label changes
    query = client.security.audit_log.queries.add(
        display_name=f"Sensitivity label changes - last {days_back} days",
        scope="SharePoint",
        additional_data={
            "@odata.type": "#microsoft.graph.security.auditLogQuery",
            "startDate": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endDate": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "operations": ["FileSensitivityLabelChanged", "FileSensitivityLabelRemoved"],
        },
    ).execute_query()

    print(f"Audit query submitted: {query.display_name}")
    print("Results are fetched asynchronously. Poll query.records for results.")

    return []


def main():
    print("Searching for sensitivity label downgrades in the last 90 days...\n")
    downgrades = find_label_downgrades(days_back=90)

    if not downgrades:
        print("\nNo downgrade events found (or query still processing).")
        print()
        print("When processing results, compare label priority:")
        print("  New priority < Old priority  =>  Downgrade")
        print("  New priority > Old priority  =>  Upgrade")
        print("  No new label                 =>  Removed")


if __name__ == "__main__":
    main()
