"""
Demonstrates how to download file content.
Intended for small files (with a size less than 4 MB).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Download file content")
    parser.add_argument("--list-title", default="Site Pages", help="document library title")
    parser.add_argument("--file-name", default="Home.aspx", help="file name")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file = ctx.web.lists.get_by_title(args.list_title).root_folder.files.get_by_url(args.file_name)
    file.get_content().execute_query()
    print("[Ok] file content has been downloaded")


if __name__ == "__main__":
    main()
