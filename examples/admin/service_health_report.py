"""
Message Center and Service Health report.

Pulls the tenant service health overview, active service incidents and the
message center announcements (major changes) into a single report.

Inspired by FetchServiceMessagesGraph.ps1 and Get-ServiceAlertsGraph.ps1
from Office 365 for IT Pros.

Requires delegated permission ``ServiceHealth.Read.All``.

https://learn.microsoft.com/en-us/graph/api/servicehealth-list
https://learn.microsoft.com/en-us/graph/api/serviceannouncement-list-issues
https://learn.microsoft.com/en-us/graph/api/serviceannouncement-list-messages
"""

import argparse
import csv

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

# Service issue statuses that no longer require attention.
RESOLVED_ISSUE_STATUSES = {
    "ServiceRestored",
    "PostIncidentReviewPublished",
    "Resolved",
    "ResolvedExternalConfirmed",
    "ResolvedExternalMitigated",
    "FalsePositive",
}


def main():
    parser = argparse.ArgumentParser(description="Message Center and Service Health report")
    parser.add_argument("--export", default=None, help="optional path to write a CSV report")
    args = parser.parse_args()

    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    announcement = client.admin.service_announcement

    health = announcement.health_overviews.get().execute_query()
    issues = announcement.issues.get().execute_query()
    messages = announcement.messages.get().execute_query()

    active_issues = [i for i in issues if i.properties.get("status") not in RESOLVED_ISSUE_STATUSES]
    major_changes = [m for m in messages if m.properties.get("isMajorChange")]

    print("Service health")
    for item in sorted(health, key=lambda x: str(x.properties.get("service", ""))):
        print(f"  {item.properties.get('service', '?'):40s} {item.properties.get('status', '?')}")

    print(f"\nActive incidents ({len(active_issues)})")
    for issue in active_issues:
        print(
            f"  [{issue.properties.get('classification', '?')}] {issue.properties.get('title', '?')}"
            f"  ({issue.properties.get('status', '?')})"
        )

    print(f"\nMessage center - major changes ({len(major_changes)})")
    for msg in major_changes:
        services = ", ".join(msg.properties.get("services", []) or ["?"])
        print(f"  {msg.properties.get('title', '?')}  [{services}]  {msg.properties.get('category', '?')}")

    if args.export:
        rows = [("service", "status")]
        rows += [(r.properties.get("service", "?"), r.properties.get("status", "?")) for r in health]
        rows += [("incident", r.properties.get("title", "?")) for r in active_issues]
        rows += [("message", r.properties.get("title", "?")) for r in major_changes]
        with open(args.export, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"\nReport written to {args.export}")


if __name__ == "__main__":
    main()
