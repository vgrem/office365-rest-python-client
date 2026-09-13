"""
Export a SharePoint list to local JSON records — migrate "from SharePoint".

``SharePointListSource`` projects list items into JSON records, persisted by
``JsonFileTarget`` under a list-specific folder in the system temp dir
(``--target`` overrides). If the source is a **document library**, its file and
folder tree (including empty folders) is also exported into ``<target>/files``.

Requires: read access to the source list/library.
"""

from __future__ import annotations

import argparse
import os
import tempfile

from office365.migration import ConflictResolution, MigrationJob, MigrationOptions
from office365.migration.adapters.filesystem import FileSystemTarget, JsonFileTarget
from office365.migration.sharepoint.adapters import SharePointLibrarySource, SharePointListSource
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

_DOCUMENT_LIBRARY_TEMPLATE = 101


def export_dir(list_title: str | None) -> str:
    return os.path.join(tempfile.gettempdir(), f"{list_title or 'list'}")


def main():
    parser = argparse.ArgumentParser(description="Export a SharePoint list to local JSON records")
    parser.add_argument("--list-title", default="Documents", help="source list title")
    parser.add_argument("--target", default=None, help="output directory for the export")
    parser.add_argument("--select", default=None, help="comma-separated fields to export")
    args = parser.parse_args()
    args.target = args.target or export_dir(args.list_title)

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    list_obj = ctx.web.lists.get_by_title(args.list_title)
    list_obj.ensure_properties(["BaseTemplate"]).execute_query()
    is_library = list_obj.base_template == _DOCUMENT_LIBRARY_TEMPLATE

    options = MigrationOptions(conflict_resolution=ConflictResolution.OVERWRITE)

    # 1) item metadata as JSON records
    source = SharePointListSource(list_obj, select=args.select.split(",") if args.select else None)
    job = MigrationJob(source, JsonFileTarget(args.target), options=options)
    print("Planning list items…", flush=True)
    manifest = job.plan()
    print(f"Planned {len(manifest)} list items -> {args.target}")
    for warning in source.warnings:
        print(f"Warning: {warning}")

    print("Migrating…", flush=True)
    stats = job.run()
    print(stats.summary())
    report = job.verify()
    print(report.summary())

    # 2) a document library also exports its file/folder tree
    if is_library:
        files_dir = os.path.join(args.target, "files")
        lib_source = SharePointLibrarySource(list_obj.root_folder)
        job = MigrationJob(lib_source, FileSystemTarget(files_dir, include_folders=True), options=options)
        print("Planning library files…", flush=True)
        manifest = job.plan()
        print(f"Document library detected — planned {len(manifest)} files/folders -> {files_dir}")

        print("Migrating…", flush=True)
        stats = job.run()
        print(stats.summary())
        report = job.verify()
        print(report.summary())


if __name__ == "__main__":
    main()
