"""
Query audit logs for file sharing events in SharePoint Online and OneDrive.

Uses the Microsoft Graph AuditLog Query API to find SharingSet events
within a date range. Useful for security monitoring — identify when
users share files inside or outside the organization.

Inspired by Report-FileSharingAuditEvents.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    AuditLog.Read.All       Read audit log records
    User.ReadBasic.All      Resolve user display names

https://learn.microsoft.com/en-us/graph/api/security/auditlogquery-query
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def query_file_sharing_events(days_back: int = 30) -> list[dict]:
    """Query audit logs for file sharing events.

    Args:
        days_back: Number of days to look back from now.

    Returns:
        List of sharing event dicts with user, file, target, timestamp.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(
        test_client_id, test_client_secret
    )

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days_back)

    # Build the audit log query for sharing events
    query = client.security.audit_log.queries.add(
        display_name=f"File sharing audit {start_date.date()} to {end_date.date()}",
        filter_operator=None,
        scope="SharePoint",
        # Note: In production, use the full auditLogQuery API.
        # This example shows the pattern; pagination and result
        # retrieval vary by API version.
        additional_data={
            "@odata.type": "#microsoft.graph.security.auditLogQuery",
            "startDate": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endDate": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "operations": ["SharingSet"],
        },
    ).execute_query()

    print(f"Audit query created: {query.display_name}")
    print(f"Status: {query.status}")

    # Results are typically retrieved asynchronously.
    # Check query.status and poll query.records when complete.
    return []


def main():
    print("Setting up file sharing audit query for the last 30 days...")
    events = query_file_sharing_events(days_back=30)

    if not events:
        print("No sharing events found (or query still running).")
        print("The auditLogQuery API is asynchronous — poll query.records")
        print("to retrieve results once the status is 'succeeded'.")


if __name__ == "__main__":
    main()
