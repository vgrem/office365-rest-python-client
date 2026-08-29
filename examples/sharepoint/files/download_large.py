"""
Demonstrates how to download large files.
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def print_download_progress(bytes_read: int) -> None:
    print(f"\rDownloaded {bytes_read:,} bytes...", end="")


def main():
    parser = argparse.ArgumentParser(description="Download a large file from a SharePoint site")
    parser.add_argument(
        "--file-url",
        default="Shared Documents/archive/big_buck_bunny.mp4",
        help="server-relative file URL",
    )
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    source_file = ctx.web.get_file_by_server_relative_path(args.file_url)
    local_file_name = os.path.join(tempfile.mkdtemp(), os.path.basename(args.file_url))
    with open(local_file_name, "wb") as local_file:
        source_file.download_session(local_file, print_download_progress).execute_query()
    print(f"[Ok] file has been downloaded: {local_file_name}")


if __name__ == "__main__":
    main()
