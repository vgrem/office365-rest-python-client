"""
Download a folder into a zip archive with a tqdm progress bar.

Demonstrates the typed ``progress`` hook on ``download_folder`` (one hook call
per downloaded file). ``progress_bar`` is the optional tqdm adapter from
``office365.runtime.progress`` (install ``office365-rest-python-client[progress]``);
without tqdm it is a no-op, so the example still runs.
"""

import argparse
import os
import tempfile

from office365.runtime.progress import progress_bar
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Download a folder into a zip file, with a progress bar")
    parser.add_argument("--folder-url", default="Shared Documents/archive", help="server-relative folder URL")
    parser.add_argument("--output", default=None, help="output zip path (default: temp)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    folder = ctx.web.get_folder_by_server_relative_url(args.folder_url)
    output = args.output or os.path.join(tempfile.mkdtemp(), f"{os.path.basename(args.folder_url)}.zip")
    with open(output, "wb") as download_file:
        folder.download_folder_as_zip(
            download_file,
            progress=progress_bar(f"Downloading {os.path.basename(args.folder_url)}"),
            include_versions=True,
        ).execute_query()

    print(f"\nArchive written to {output}")


if __name__ == "__main__":
    main()
