"""
Demonstrates how to move a file within a site.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.move_operations import MoveOperations
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Move a file within a site")
    parser.add_argument(
        "--file-path", default="Shared Documents/Financial Sample.xlsx", help="server-relative file path"
    )
    parser.add_argument(
        "--folder-path", default="Shared Documents/Archive", help="server-relative destination folder path"
    )
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    file_from = ctx.web.get_file_by_server_relative_path(args.file_path)
    # folder_to = ctx.web.get_folder_by_server_relative_url("Shared Documents")
    folder_to = args.folder_path

    file_to = file_from.move_to_using_path(folder_to, MoveOperations.overwrite).execute_query()
    print(f"'{file_from}' moved into '{file_to.server_relative_path}'")


if __name__ == "__main__":
    main()
