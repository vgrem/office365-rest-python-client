"""
Gets the files from a folder.
If the 'recursive' flag is set to True, it traverses all sub folders.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from tests.settings import client_id, password, team_site_url, tenant, username


def print_file(f: File) -> None:
    print(f.server_relative_url)


def main():
    parser = argparse.ArgumentParser(description="Gets the files from a folder")
    parser.add_argument("--folder-url", default="Shared Documents", help="folder url")
    parser.add_argument("--recursive", action="store_true", default=True, help="traverse all sub folders")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    root_folder = ctx.web.get_folder_by_server_relative_path(args.folder_url)
    files = root_folder.get_files(args.recursive).execute_query()
    [print_file(f) for f in files]


if __name__ == "__main__":
    main()
