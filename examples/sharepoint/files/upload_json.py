"""
Demonstrates how to upload a JSON file to a SharePoint site
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Upload a JSON file to a SharePoint site")
    parser.add_argument("--list-title", default="Documents", help="document library title")
    parser.add_argument("--path", default="../../data/countries.json", help="path to the local file")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    folder = ctx.web.lists.get_by_title(args.list_title).root_folder
    with open(args.path, "r") as f:
        file = folder.files.upload(f).execute_query()
    print(f"File has been uploaded into: {file.server_relative_url}")


if __name__ == "__main__":
    main()
