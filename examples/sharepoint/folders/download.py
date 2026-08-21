"""
Demonstrates how to enumerate folder files and download their content.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def download_files(source_folder, download_path: str) -> None:
    files = source_folder.files.get().execute_query()
    for file in files:
        print(f"Downloading file: {file.properties.get('ServerRelativeUrl', '?')} ...")
        file_name = file.name or file.properties.get("LeafName") or "download.bin"
        local_file_path = os.path.join(download_path, str(file_name))
        with open(local_file_path, "wb") as local_file:
            file.download(local_file).execute_query()
        print(f"[Ok] file has been downloaded: {local_file_path}")


def main():
    parser = argparse.ArgumentParser(description="Download all files from a library folder")
    parser.add_argument("--list-title", default="Documents", help="document library title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    from_folder = ctx.web.lists.get_by_title(args.list_title).root_folder
    download_files(from_folder, tempfile.mkdtemp())


if __name__ == "__main__":
    main()
