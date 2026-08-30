"""
Gets the files from a folder.
If the 'recursive' flag is set to True, it traverses all sub folders.

The ``progress`` hook fires once per scanned folder — each file is printed as
it is discovered via ``items`` (no separate result loop needed).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.runtime.operations import Progress
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from tests.settings import client_id, password, team_site_url, tenant, username


def print_files(p: Progress[File]) -> None:
    """Fired per scanned folder — print each file discovered in that folder."""
    for f in p.items or []:
        print(f.server_relative_url)


def main():
    parser = argparse.ArgumentParser(description="Gets the files from a folder")
    parser.add_argument("--folder-url", default="Documents_Archive", help="folder url")
    parser.add_argument("--recursive", action="store_true", default=True, help="traverse all sub folders")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    root_folder = ctx.web.get_folder_by_server_relative_path(args.folder_url)
    root_folder.get_files(args.recursive, progress=print_files).execute_query()


if __name__ == "__main__":
    main()
