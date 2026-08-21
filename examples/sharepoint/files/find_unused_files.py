"""
Identify files in a SharePoint site that haven't been accessed
within a specified period.

Uses the file's last modified date as a proxy for activity (a real
audit-log query would be more accurate but requires the beta
``/security/auditLog/queries`` API). Helps clean up stale content and
reduce storage costs.

Requires read access to the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse
from datetime import datetime, timedelta, timezone
from typing import List

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

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


def find_unused_files(ctx: ClientContext, days_threshold: int) -> List[dict]:
    """Find files whose last modified date is older than *days_threshold*."""
    print("Fetching files from document library...")
    files = get_all_files_in_site(ctx)
    print(f"  Found {len(files)} files")

    cutoff = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    unused = []

    for _, info in files.items():
        modified = info["last_modified"]
        try:
            last_access = datetime.fromisoformat(str(modified).replace("Z", "+00:00"))
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
    parser = argparse.ArgumentParser(description="Find unused files in the default document library")
    parser.add_argument("--days", type=int, default=180, help="days of inactivity to flag a file")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    unused = find_unused_files(ctx, args.days)

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
