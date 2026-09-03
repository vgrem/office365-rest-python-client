"""
Import a local zip archive's file/folder hierarchy into a SharePoint document library.

Reads a zip (e.g. an open-data archive like plotly/datasets) and uploads its
entries into the library at their literal relative paths via
``Folder.upload_folder_from_zip`` — in-memory, one entry at a time, deferred
(a single ``execute_query`` drives the uploads).

    python import_lib.py --zip /tmp/dataset.zip

Notes:
- For a sequential, single-context upload of a local directory instead, use
  ``Folder.upload_folder``; for a fast parallel transfer use the migration
  toolkit (``MigrationJob`` + ``SharePointLibraryTarget(concurrency=…)``).
- The target library is expected to be fresh: folders are not overwritten, so
  re-running against the same library may fail on duplicates.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse
import zipfile
from pathlib import Path

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.lists.templates.type import ListTemplateType
from tests.settings import client_id, password, team_site_url, tenant, username
from tqdm import tqdm


def zip_file_count(zip_path: Path) -> int:
    """Number of file entries in a zip (directory entries are skipped)."""
    with zipfile.ZipFile(zip_path) as zf:
        return sum(1 for name in zf.namelist() if not name.endswith("/"))


def progress_bar(total: int):
    """Compact tqdm progress hook for the upload."""
    bar = tqdm(total=total, desc="Uploading")

    def hook(p) -> None:
        bar.update(p.done - bar.n)
        if p.done >= p.total:
            bar.close()

    return hook


def main():
    parser = argparse.ArgumentParser(description="Import a local zip archive into a SharePoint library")
    parser.add_argument("--zip", default="/tmp/datasets.zip", help="local zip archive with a file/folder hierarchy")
    parser.add_argument("--list-title", default="Data_Import", help="target document library title")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    zip_path = Path(args.zip)
    if not zip_path.exists():
        parser.error(f"zip not found: {zip_path}")

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    lib = ctx.web.lists.ensure_list(
        title=args.list_title, template_type=ListTemplateType.DocumentLibrary
    ).execute_query()

    total = zip_file_count(zip_path)
    hook = progress_bar(total) if not args.no_progress else None
    lib.root_folder.upload_folder_from_zip(zip_path, progress=hook).execute_query()
    print(f"Imported {total} files from '{zip_path}' into '{lib.title}'")


if __name__ == "__main__":
    main()
