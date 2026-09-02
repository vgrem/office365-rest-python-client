"""
Migration session — add a task, start, monitor, stop.

A job-centric batch: each task is a source → target :class:`MigrationJob` added
explicitly to a :class:`MigrationSession`, then started together. Bidirectional —
a task pairs any source/target adapter. Here: migrate a local directory tree
**into** a SharePoint document library with parallel uploads
(``MigrationOptions.concurrency``).

    python migrate_session.py --source ./data --library-url /sites/project/Shared Documents

Requires: write access to the target library.
"""

import argparse

from office365.migration import MigrationOptions, MigrationSession
from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.adapters.sharepoint import SharePointLibraryTarget
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Migrate a local tree into a SharePoint library via a session")
    parser.add_argument("--source", required=True, help="local directory to migrate")
    parser.add_argument("--library-url", required=True, help="server-relative library URL")
    parser.add_argument("--concurrency", type=int, default=4, help="parallel upload workers")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    folder = ctx.web.get_folder_by_server_relative_path(args.library_url)
    options = MigrationOptions(concurrency=args.concurrency)

    session = MigrationSession()
    job = session.add_task(
        FileSystemSource(args.source),
        SharePointLibraryTarget(folder, concurrency=args.concurrency),
        options=options,
        checkpoint_path="session-checkpoint.json",
    )
    print(f"Task: {job.source_label} -> {job.target_label}")

    session.start()
    for status in session.status():
        stats = status["stats"]
        print(
            f"[{status['phase']}] success={stats['success']} skipped={stats['skipped']} "
            f"errors={stats['errors']} transferred={stats['bytes_transferred'] / 1024 / 1024:.1f}MB"
        )


if __name__ == "__main__":
    main()
