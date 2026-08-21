"""
Demonstrates how to copy a file within a site
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Copy a file within a site with a new name")
    parser.add_argument(
        "--file-url", default="Shared Documents/Financial Sample.xlsx", help="server-relative file URL"
    )
    parser.add_argument(
        "--folder-url", default="Shared Documents/archive", help="server-relative destination folder URL"
    )
    parser.add_argument("--new-name", default="Financial 2023.xlsx", help="new file name")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    file_from = ctx.web.get_file_by_server_relative_url(args.file_url)
    file_to = file_from.copyto(args.folder_url, True, args.new_name).execute_query()
    print(f"File copied into '{file_to.server_relative_url}'")


if __name__ == "__main__":
    main()
