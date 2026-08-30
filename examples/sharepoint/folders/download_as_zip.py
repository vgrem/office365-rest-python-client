"""
Demonstrates how to download folder content into a zip file.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def print_progress(file: File) -> None:
    print(f"File {file.server_relative_url} has been  downloaded")


def main():
    parser = argparse.ArgumentParser(description="Downloads folder content into a zip file")
    parser.add_argument("--list-title", default="Documents", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    from_folder = ctx.web.lists.get_by_title(args.list_title).root_folder
    zip_path = os.path.join(tempfile.mkdtemp(), "download.zip")
    with open(zip_path, "wb") as to_file:
        from_folder.download_folder(to_file, print_progress).execute_query()
        print(f"Files has been downloaded: {zip_path}")


if __name__ == "__main__":
    main()
