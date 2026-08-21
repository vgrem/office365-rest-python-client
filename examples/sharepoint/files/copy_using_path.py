"""
Demonstrates how to copy a file within a site
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Copy a file within a site by path")
    parser.add_argument(
        "--file-path", default="Shared Documents/Financial Sample.xlsx", help="server-relative file path"
    )
    parser.add_argument(
        "--folder-path", default="Shared Documents/archive", help="server-relative destination folder path"
    )
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    file_from = ctx.web.get_file_by_server_relative_path(args.file_path)
    folder_to = ctx.web.get_folder_by_server_relative_path(args.folder_path)
    # folder_to = "Shared Documents/archive/2002/02"
    file_to = file_from.copyto_using_path(folder_to, True).execute_query()
    print(f"{file_from} copied into {file_to}")


if __name__ == "__main__":
    main()
