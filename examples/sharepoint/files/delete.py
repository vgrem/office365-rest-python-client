"""
Deletes a file from SharePoint site
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Delete a file from a SharePoint site")
    parser.add_argument("--file-url", default="Shared Documents/Financial Sample.xlsx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    # file.recycle().execute_query()
    # or delete permanently via delete_object:
    # file.delete_object().execute_query()
    print(f"Deleted file: {args.file_url}")

    print("Print deleted files...")
    result = ctx.web.get_recycle_bin_items().execute_query()
    for recycle_bin_item in result:
        print(recycle_bin_item)


if __name__ == "__main__":
    main()
