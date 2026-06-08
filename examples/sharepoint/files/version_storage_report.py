"""
Analyze file version storage across a SharePoint document library.

Reports the number of versions per file, their storage cost, and
identifies candidates for version cleanup (files with excessive
versions that consume disproportionate storage).

Inspired by Report-SPOFileVersions.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Sites.Read.All          Read files, libraries, and version history

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url, test_tenant


def format_bytes(size: int) -> str:
    """Format byte count to human-readable string."""
    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"
    elif size >= 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MB"
    elif size >= 1024:
        return f"{size / 1024:.2f} KB"
    return f"{size} B"


def analyze_version_storage(ctx: ClientContext, library_name: str = "Shared Documents") -> list[dict]:
    """Analyze file version storage in a document library.

    Args:
        ctx: Authenticated ClientContext.
        library_name: Name of the document library to scan.

    Returns:
        List of file dicts with version count, total version size, and current size.
    """
    results = []

    try:
        lib = ctx.web.lists.get_by_title(library_name)
        files = lib.root_folder.files.expand(["Versions"]).get().execute_query()
    except Exception as e:
        print(f"  Error accessing library '{library_name}': {e}")
        return results

    for f in files:
        version_count = 0
        total_version_size = 0
        current_size = getattr(f, "length", 0)

        try:
            versions = f.versions
            if versions:
                version_count = len(versions)
                for v in versions:
                    total_version_size += getattr(v, "size", 0) or 0
        except Exception:
            pass

        results.append({
            "name": getattr(f, "name", "Unknown"),
            "url": getattr(f, "server_relative_url", ""),
            "current_size": current_size,
            "version_count": version_count,
            "total_version_size": total_version_size,
            "storage_ratio": (total_version_size / current_size) if current_size > 0 else 0,
        })

    # Sort by version count descending
    results.sort(key=lambda r: r["version_count"], reverse=True)
    return results


def main():
    print("Analyzing file version storage...\n")

    ctx = ClientContext(test_site_url).with_client_secret(
        test_tenant, test_client_id, test_client_secret
    )

    report = analyze_version_storage(ctx, "Shared Documents")

    if not report:
        print("No files found or library inaccessible.")
        return

    total_versions = sum(r["version_count"] for r in report)
    total_storage = sum(r["total_version_size"] for r in report)

    print(f"Files analyzed:     {len(report)}")
    print(f"Total versions:     {total_versions}")
    print(f"Version storage:    {format_bytes(total_storage)}")
    print()

    # Top 10 files by version count
    print("=== Top 10 files by version count ===\n")
    print(f"{'File':50s} {'Versions':>10s} {'Version Size':>15s} {'Current Size':>15s} {'Ratio'}")
    print("-" * 100)
    for r in report[:10]:
        print(
            f"{r['name'][:48]:50s} "
            f"{r['version_count']:>10d} "
            f"{format_bytes(r['total_version_size']):>15s} "
            f"{format_bytes(r['current_size']):>15s} "
            f"{r['storage_ratio']:.1f}x"
        )

    # Files with excessive versions (20+)
    excessive = [r for r in report if r["version_count"] >= 20]
    if excessive:
        print(f"\n=== Files with 20+ versions (cleanup candidates) ===\n")
        for r in excessive:
            print(f"  {r['name']} — {r['version_count']} versions, {format_bytes(r['total_version_size'])}")


if __name__ == "__main__":
    main()
