"""
Auto-apply a retention label to files based on their age.

Scans a SharePoint document library and applies a retention label
to files that are older than a specified threshold but haven't yet
been labeled. Useful for applying a "default retention" to legacy
content without manual intervention.

Inspired by Auto-ApplyRetentionLabels.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    RecordsManagement.ReadWrite.All  Create and apply retention labels
    Sites.Read.All                   Read SharePoint files and metadata
    Files.ReadWrite.All              Apply labels to files

https://learn.microsoft.com/en-us/graph/api/resources/security-retentionlabel
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant

_SAMPLE_SIZE = 10


def get_retention_label_id(client: GraphClient, label_name: str) -> str | None:
    """Fetch a retention label by display name.

    Returns the label ID or None if not found.
    """
    try:
        labels = client.security.retention_labels.get().execute_query()
        for label in labels:
            if getattr(label, "display_name", "") == label_name:
                return label.id
    except Exception:
        pass
    return None


def find_files_without_label(ctx: ClientContext, age_days: int) -> list[dict]:
    """Find files older than *age_days* that have no retention label.

    Args:
        ctx: Authenticated SharePoint ClientContext.
        age_days: File age threshold.

    Returns:
        List of file dicts (name, url, created, modified).
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=age_days)
    unlabeled = []

    try:
        lib = ctx.web.default_document_library()
        items = (
            lib.items.select(["FileLeafRef", "FileRef", "Created", "ComplianceTag"])
            .filter("FSObjType eq 0")
            .get_all()
            .execute_query()
        )

        for item in items:
            created = item.properties.get("Created", "")
            compliance_tag = item.properties.get("ComplianceTag", None)

            if compliance_tag:
                continue  # already labeled

            try:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                continue

            if created_dt < cutoff:
                unlabeled.append(
                    {
                        "name": item.properties.get("FileLeafRef", "Unknown"),
                        "url": item.properties.get("FileRef", ""),
                        "created": created_dt,
                    }
                )
    except Exception as e:
        print(f"  Error scanning files: {e}")

    return unlabeled


def apply_label_to_file(ctx: ClientContext, file_url: str, label_name: str) -> bool:
    """Apply a retention/compliance label to a file.

    Note: The exact mechanism depends on your SharePoint/Graph version.
    This shows the conceptual pattern.
    """
    # In production, you'd set ComplianceTag on the list item.
    # Example:
    #   item = ctx.web.get_file_by_server_relative_url(file_url).list_item_all_fields
    #   item.set_property("ComplianceTag", label_name)
    #   item.update().execute_query()
    print(f"  Would apply '{label_name}' to {file_url}")
    return True


def main():
    print("Auto-apply retention labels to unlabelled files...\n")

    graph = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    # 1. Find the label
    label_name = "Default Retention — 7 years"
    label_id = get_retention_label_id(graph, label_name)

    if not label_id:
        print(f"Label '{label_name}' not found. Create it in Purview first.")
        print("Available labels can be listed via Graph API or Purview portal.")
        return

    print(f"Using label: {label_name} ({label_id[:12]}...)")

    # 2. Scan for unlabelled files older than 365 days
    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)

    files = find_files_without_label(ctx, age_days=365)
    print(f"Found {len(files)} older unlabelled files\n")

    # 3. Apply labels
    for f in files[:_SAMPLE_SIZE]:  # limit for safety
        apply_label_to_file(ctx, f["url"], label_name)

    if len(files) > _SAMPLE_SIZE:
        print(f"\n... and {len(files) - _SAMPLE_SIZE} more files would be labeled")
    print("\nReview the file list and uncomment the update call to apply.")


if __name__ == "__main__":
    main()
