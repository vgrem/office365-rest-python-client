"""
Migrate a document library to/from a local directory — bidirectional.

- Export (default): enumerate the library's files recursively and download
  them preserving the folder structure into a folder named after the library
  under the system temp dir (``--target`` overrides).
- Import (``--import DIR``): upload a local tree into the library with
  **parallel** workers (``--concurrency``), sharing a rate limiter that paces
  the fleet on ``Retry-After`` / ``X-SharePointHealthScore``.

Requires: read access to the library (export), write access (import).
"""

from __future__ import annotations

import argparse
import os
import tempfile

from office365.migration import ConflictResolution, MigrationJob, MigrationOptions
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget
from office365.migration.sharepoint.adapters import SharePointLibrarySource, SharePointLibraryTarget
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def export_dir(library_url: str) -> str:
    name = library_url.strip("/").rsplit("/", 1)[-1] or "library"
    return os.path.join(tempfile.gettempdir(), f"lib-export-{name}")


def main():
    parser = argparse.ArgumentParser(description="Migrate a document library to/from a local directory")
    parser.add_argument("--library-url", required=True, help="server-relative library URL")
    parser.add_argument("--import", dest="import_dir", help="local directory to import INTO the library")
    parser.add_argument("--target", default=None, help="local output directory (export only)")
    parser.add_argument("--concurrency", type=int, default=4, help="parallel upload workers (import only)")
    args = parser.parse_args()
    args.target = args.target or export_dir(args.library_url)

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    folder = ctx.web.get_folder_by_server_relative_url(args.library_url)

    if args.import_dir:
        options = MigrationOptions(concurrency=args.concurrency)
        job = MigrationJob(
            FileSystemSource(args.import_dir),
            SharePointLibraryTarget(folder, concurrency=args.concurrency),
            options=options,
        )
        print(f"Importing {args.import_dir} -> {args.library_url}")
    else:
        # Export mirrors the library — overwrite a previous export rather than
        # skip on stale files.
        options = MigrationOptions(concurrency=1, conflict_resolution=ConflictResolution.OVERWRITE)
        job = MigrationJob(
            SharePointLibrarySource(folder),
            FileSystemTarget(args.target, include_folders=True),
            options=options,
        )
        print(f"Exporting {args.library_url} -> {args.target}")

    print("Planning…", flush=True)
    manifest = job.plan()
    print(f"Planned {len(manifest)} files/folders")

    print("Migrating…", flush=True)
    stats = job.run()
    print(stats.summary())
    print(job.verify().summary())


if __name__ == "__main__":
    main()
