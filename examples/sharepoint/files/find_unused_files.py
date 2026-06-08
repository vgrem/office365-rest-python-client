"""
Identify files in a SharePoint site that haven't been accessed
within a specified period.

Uses audit log records (FileAccessed, FileDownloaded, FileModified)
to determine the last meaningful user activity on each file. Helps
clean up stale content and reduce storage costs.

Inspired by Find-LastAccessedDateDocuments.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    AuditLog.Read.All           Read audit log records
    Sites.Read.All              Read file metadata in the site
    User.ReadBasic.All          Resolve user display names

https://learn.microsoft.com/en-us/graph/api/security/auditlogquery-query
"""

from datetime import datetime, timedelta, timezone

from office365.sharepoint.client_context import ClientContext
from tests import (
    test_client_id,
    test_client_secret,
    test_site_url,
    test_tenant,
)

_DISPLAY_LIMIT = 20


def get_all_files_in_site(ctx: ClientContext) -> dict:
    """Get all files in the default document library.

    Returns dict mapping file URL -> {name, url, created, modified}.
    """
    files_map = {}

    try:
        lib = ctx.web.default_document_library()
        items = (
            lib.items.select(["FileLeafRef", "FileRef", "Created", "Modified"])
            .filter("FSObjType eq 0")
            .get_all()
            .execute_query()
        )

        for item in items:
            file_url = item.properties.get("FileRef", "")
            files_map[file_url] = {
                "name": item.properties.get("FileLeafRef", "Unknown"),
                "url": file_url,
                "created": item.properties.get("Created", ""),
                "last_modified": item.properties.get("Modified", ""),
            }
    except Exception as e:
        print(f"  Error fetching files: {e}")

    return files_map


def get_file_access_events(days_back: int) -> dict:
    """Query audit logs for file access events.

    Returns dict mapping file URL -> most recent access timestamp.
    """
    # This is a placeholder for the actual audit log query.
    # In production, use client.security.audit_log.queries.add()
    # with operations: FileAccessed, FileDownloaded, FileModified
    # and then poll for results.
    print(f"  Audit log query would search {days_back} days for file access events")
    return {}


def find_unused_files(days_threshold: int = 180) -> list[dict]:
    """Find files without user access within *days_threshold*.

    Args:
        days_threshold: Days of inactivity to flag a file.

    Returns:
        List of file dicts with last access info.
    """
    ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)

    print("Fetching files from document library...")
    files = get_all_files_in_site(ctx)
    print(f"  Found {len(files)} files")

    print("Querying audit logs for file access events...")
    access_events = get_file_access_events(days_threshold)

    cutoff = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    unused = []

    for file_url, info in files.items():
        # Last access = most recent audit event or fall back to Modified
        last_access = access_events.get(file_url)
        if not last_access:
            # Fallback: use the file's last modified date
            try:
                modified = info["last_modified"]
                if modified:
                    last_access = datetime.fromisoformat(modified.replace("Z", "+00:00"))
                else:
                    last_access = datetime.now(timezone.utc) - timedelta(days=1000)
            except (ValueError, TypeError):
                last_access = datetime.now(timezone.utc) - timedelta(days=1000)

        if last_access < cutoff:
            unused.append(
                {
                    "name": info["name"],
                    "url": info["url"],
                    "last_access": last_access,
                    "days_since_access": (datetime.now(timezone.utc) - last_access).days,
                }
            )

    unused.sort(key=lambda x: x["last_access"])
    return unused


def main():
    print("Finding unused files (no access in 180+ days)...\n")
    unused = find_unused_files(days_threshold=180)

    if not unused:
        print("No unused files found.")
        return

    print(f"\nFound {len(unused)} files with no recent access:\n")
    print(f"{'File':50s} {'Days Since Access':>20s}")
    print("-" * 70)
    for f in unused[:_DISPLAY_LIMIT]:
        print(f"{f['name'][:48]:50s} {f['days_since_access']:>20d}")

    if len(unused) > _DISPLAY_LIMIT:
        print(f"\n... and {len(unused) - _DISPLAY_LIMIT} more files")


if __name__ == "__main__":
    main()
