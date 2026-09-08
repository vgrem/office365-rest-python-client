"""
Inventory and download a specific user's OneDrive recursively — no ``/me``.

Resolves the drive via ``users/{upn}/drive``, walks the whole tree with the
paged ``get_files()``/``get_folders()`` scans, then archives every file into a
zip with ``download_folder()``.

    python export_user_drive.py --user bob@contoso.onmicrosoft.com

Requires application permission ``Files.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list-drive
https://learn.microsoft.com/en-us/graph/api/driveitem-list-children
"""

import argparse
import os
import tempfile

from office365.graph_client import GraphClient
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.runtime.operations import Progress
from tests.settings import client_id, client_secret, tenant, user_principal


def progress_bar(description: str):
    """tqdm-backed hook — the library only needs a ``Callable[[Progress], None]``."""
    from tqdm import tqdm

    bar = tqdm(desc=description)

    def hook(p: Progress[DriveItem]) -> None:
        bar.update(p.done - bar.n)

    return hook


def main():
    parser = argparse.ArgumentParser(description="Download a user's OneDrive recursively")
    parser.add_argument("--user", default=user_principal, help="user principal name (UPN) of the drive owner")
    parser.add_argument("--output", default=None, help="path to the output zip file")
    parser.add_argument("--no-progress", action="store_true", help="do not show tqdm progress bars")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("Files.Read.All")
    )

    drive = client.users[args.user].drive.get().execute_query()
    root = drive.root.get().execute_query()

    folders_hook = None if args.no_progress else progress_bar("Folders")
    files_hook = None if args.no_progress else progress_bar("Files")
    folders = root.get_folders(recursive=True, progress=folders_hook).execute_query()
    files = root.get_files(recursive=True, progress=files_hook).execute_query()

    total_size = sum(f.size or 0 for f in files)
    print(f"'{args.user}' drive ({drive.drive_type}):")
    print(f"  {len(folders):,} folders, {len(files):,} files ({total_size:,} bytes)\n")

    output = args.output or os.path.join(tempfile.gettempdir(), f"onedrive_{str(args.user).split('@')[0]}.zip")
    with open(output, "wb") as to_file:
        root.download_folder(to_file).execute_query()
    print(f"Downloaded {len(files):,} files to {output} ({os.path.getsize(output):,} bytes)")


if __name__ == "__main__":
    main()
