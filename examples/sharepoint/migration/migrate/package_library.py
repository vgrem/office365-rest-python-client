"""
Build a SharePoint Migration API package from a local folder — offline.

**Optional, tenant-free** companion to ``migrate_library_serverside.py``: it shows
exactly what a server-side migration uploads — the manifest XML plus the content
blobs — with no SharePoint and no Azure. Use it to learn or inspect the package;
the real migration builds this internally, so it is **not** a prerequisite step.

Run it from this folder (it defaults to the repo sample data ``examples/data``):

    python package_library.py
    python package_library.py --source ./my-files --out ./package

Requires: nothing beyond the library.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.package import FileSystemStaging, PackageBuilder
from tests.settings import team_site_url


def main():
    parser = argparse.ArgumentParser(description="Build a Migration API package from a local folder (offline)")
    parser.add_argument("--source", default="../../../data", help="local folder (default: examples/data)")
    parser.add_argument("--out", default=str(Path(tempfile.gettempdir()) / "spo-package"), help="output directory")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_dir():
        parser.error(f"not a directory: {source} — run this script from its own folder, or pass --source")

    files = FileSystemSource(source)
    builder = PackageBuilder(team_site_url, list_title="Documents")
    for item in files.list_items():
        builder.add_file(
            item.dest_path,
            files.read(item),
            time_created=item.created,
            time_last_modified=item.modified,
        )

    package = builder.build()
    FileSystemStaging(args.out).stage(package)

    print(f"{len(package.content)} content blob(s) + {len(package.blobs())} manifest file(s):")
    for name in package.blobs():
        print(f"  manifest/{name}")
    print(f"Written to {args.out}")


if __name__ == "__main__":
    main()
