"""
Delete (or recycle) file versions.

Works for large files too (2 GB+): versions are enumerated with a minimal
property set and each deletion runs through ``execute_query_with_incremental_retry``
so slow, storage-heavy operations can't hang and transient failures are retried.

Examples:
    python delete.py --file-url "Shared Documents/report.docx"            # keep newest 1
    python delete.py --file-url "Shared Documents/big.mp4" --keep 5       # keep newest 5
    python delete.py --file-url "Shared Documents/big.mp4" --all          # delete every non-current version
    python delete.py --file-url "Shared Documents/big.mp4" --recycle      # recycle instead of hard-delete

https://learn.microsoft.com/en-us/graph/api/... (SharePoint versioning REST)
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

DEFAULT_KEEP = 1


def main():
    parser = argparse.ArgumentParser(description="Delete file versions")
    parser.add_argument("--file-url", required=True, help="server-relative file URL")
    parser.add_argument(
        "--keep",
        type=int,
        default=DEFAULT_KEEP,
        help=f"newest versions to keep (default: {DEFAULT_KEEP})",
    )
    parser.add_argument("--all", action="store_true", help="delete every version except the current one")
    parser.add_argument("--recycle", action="store_true", help="recycle versions instead of deleting them permanently")
    parser.add_argument("--timeout", type=int, default=30, help="request timeout in seconds (default: 30)")
    args = parser.parse_args()

    keep = 0 if args.all else args.keep
    if keep < 0:
        parser.error("--keep must be >= 0")

    ctx = (
        ClientContext(site_url)
        .with_username_and_password(tenant=tenant, client_id=client_id, username=username, password=password)
        .with_transport(timeout=args.timeout)
    )

    versions_col = ctx.web.get_file_by_server_relative_path(args.file_url).versions
    ctx.load(versions_col, ["ID", "VersionLabel", "IsCurrentVersion"]).execute_query()

    ordered = sorted(versions_col, key=lambda v: v.id or 0, reverse=True)
    to_remove = [v for v in ordered[keep:] if not v.is_current_version]

    print(f"{len(versions_col)} version(s), keeping {keep}; removing {len(to_remove)}:")
    for version in to_remove:
        assert version.id is not None
        if args.recycle:
            versions_col.recycle_by_id(version.id)
        else:
            versions_col.delete_by_id(version.id)
        ctx.execute_query_with_incremental_retry(max_retry=3)
        print(f"  {'recycled' if args.recycle else 'deleted'} {version.version_label or '?'}")


if __name__ == "__main__":
    main()
