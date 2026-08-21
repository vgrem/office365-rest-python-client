"""
Demonstrates how to upload a CSV file to a SharePoint site
"""

import argparse
import os

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Upload a CSV file to a SharePoint site")
    parser.add_argument("--list-title", default="Documents", help="document library title")
    parser.add_argument("--path", default="../../data/Financial Sample.csv", help="path to the local file")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    folder = ctx.web.lists.get_by_title(args.list_title).root_folder
    with open(args.path, "r") as content_file:
        file_content = content_file.read().encode("utf-8-sig")
    file = folder.upload_file(os.path.basename(args.path), file_content).execute_query()
    print(f"File has been uploaded into: {file.server_relative_url}")


if __name__ == "__main__":
    main()
