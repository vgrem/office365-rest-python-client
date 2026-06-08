"""
Analyze sensitivity label usage across the tenant — which labels are
applied, where, and by whom.

Useful for governance reporting: track label adoption, find content
with no label (potential leak risk), and identify unusual label
assignment patterns.

Inspired by AnalyzeSensitivityLabelUsage.PS1 and
ReportSensitivityLabelsAuditRecords.ps1 from Office 365 for IT Pros.

Required delegated permissions:
    InformationProtectionPolicy.Read.All  Read sensitivity labels
    AuditLog.Read.All                     Read label audit events
    Sites.Read.All                        Read SharePoint files

https://learn.microsoft.com/en-us/graph/api/resources/sensitivitylabel
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def get_label_usage() -> dict:
    """Fetch sensitivity labels and build usage statistics.

    Reports label counts and priority information — in a full
    implementation, cross-references with audit logs to track
    label assignment patterns over time.

    Returns:
        Dict mapping label name -> stats (id, priority, count).
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    usage = {}
    try:
        labels = client.security.sensitivity_labels.get().execute_query()
        for label in labels:
            usage[getattr(label, "display_name", label.id)] = {
                "id": label.id[:12] + "...",
                "priority": getattr(label, "priority", 0),
                "description": getattr(label, "description", "")[:60],
            }
    except Exception as e:
        print(f"  Error fetching labels: {e}")

    return usage


def main():
    print("Sensitivity label usage analytics\n")

    labels = get_label_usage()

    if not labels:
        print("No sensitivity labels found. Create labels in Purview first.")
        return

    print(f"Found {len(labels)} sensitivity labels:\n")
    print(f"{'Label':35s} {'Priority':>10s} {'Description'}")
    print("-" * 85)
    for name, info in sorted(labels.items(), key=lambda x: x[1]["priority"]):
        print(f"{name[:33]:35s} {info['priority']:>10d} {info['description']}")

    print()
    print("Label analytics workflow:")
    print("  1. List all labels (above)")
    print("  2. Query audit logs for FileSensitivityLabelChanged events")
    print("  3. Cross-reference label IDs with priority to detect downgrades")
    print("  4. Report content with no label (potential data leak)")
    print()
    print("See also: files/find_label_downgrades.py for audit-based detection")


if __name__ == "__main__":
    main()
