"""
Demonstrates how to download a folder into a zip archive, including each
file's version history.

``Folder.download_folder_as_zip(include_versions=True)`` writes the current content
to the zip root and every previous version under
``versions/<path>/v<label>`` — a ready-made backup of a library folder.
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from tests.settings import client_id, password, site_url, tenant, username


def print_progress(file: File) -> None:
    print(f"Downloaded: {file.server_relative_url}")


def main():
    parser = argparse.ArgumentParser(description="Download a folder into a zip file, with version history")
    parser.add_argument("--folder-url", default="Shared Documents/archive", help="server-relative folder URL")
    parser.add_argument("--output", default=None, help="output zip path (default: temp)")
    parser.add_argument("--no-versions", action="store_true", help="skip version history")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    folder = ctx.web.get_folder_by_server_relative_url(args.folder_url)
    output = args.output or os.path.join(tempfile.mkdtemp(), f"{os.path.basename(args.folder_url)}.zip")
    with open(output, "wb") as download_file:
        folder.download_folder_as_zip(
            download_file,
            print_progress,
            include_versions=not args.no_versions,
        ).execute_query()

    print(f"Archive written to {output}")


if __name__ == "__main__":
    main()
