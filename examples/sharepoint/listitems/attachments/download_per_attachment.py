"""
Demonstrates how to download list item attachments.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Download list item attachments")
    parser.add_argument("--list-title", default="Company Tasks", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    source_list = ctx.web.lists.get_by_title(args.list_title)
    download_path = tempfile.mkdtemp()

    items = source_list.items.get().execute_query()
    for item in items:
        attachment_files = item.attachment_files.get().execute_query()
        for attachment_file in attachment_files:
            file_name = attachment_file.file_name or "attachment.bin"
            download_file_name = os.path.join(download_path, os.path.basename(file_name))
            with open(download_file_name, "wb") as fh:
                attachment_file.download(fh).execute_query()
            print(f"{attachment_file.server_relative_url} has been downloaded into {download_file_name}")


if __name__ == "__main__":
    main()
