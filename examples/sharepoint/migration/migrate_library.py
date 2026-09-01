"""
Migrate a document library to/from a local directory — bidirectional.

- Export (default): enumerate the library's files recursively (with progress)
  and download them preserving the folder structure.
- Import (``--import DIR``): upload a local tree into the library with
  **parallel** workers (``--concurrency``), sharing a rate limiter that paces
  the fleet on ``Retry-After`` / ``X-SharePointHealthScore``.

Requires: read access to the library (export), write access (import).
"""

import argparse

from office365.migration import MigrationJob, MigrationOptions
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget
from office365.migration.adapters.sharepoint import SharePointLibrarySource, SharePointLibraryTarget
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Migrate a document library to/from a local directory")
    parser.add_argument("--library-url", required=True, help="server-relative library URL")
    parser.add_argument("--import", dest="import_dir", help="local directory to import INTO the library")
    parser.add_argument("--target", help="local output directory (export only)")
    parser.add_argument("--concurrency", type=int, default=4, help="parallel upload workers (import only)")
    args = parser.parse_args()

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
    else:
        if not args.target:
            parser.error("--target is required for export")
        job = MigrationJob(SharePointLibrarySource(folder), FileSystemTarget(args.target))

    job.plan()
    stats = job.run()
    print(stats.summary())
    print(job.verify().summary())


if __name__ == "__main__":
    main()
