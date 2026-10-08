"""
Upload a large file with a tqdm progress bar.

Demonstrates the typed ``progress`` hook: the library only requires a
``Callable[[Progress], None]``. ``progress_bar`` is the optional tqdm adapter
from ``office365.runtime.progress`` (install
``office365-rest-python-client[progress]``); without tqdm it is a no-op, so the
example still runs (or use ``rich``/``logging``/any callback).
"""

import argparse
import os

from office365.runtime.progress import progress_bar
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Upload a large file with a tqdm progress bar")
    parser.add_argument("--path", default="../../data/big_buck_bunny.mp4", help="local file path")
    parser.add_argument("--chunk-size", type=int, default=1_000_000, help="chunk size in bytes")
    parser.add_argument("--target-folder", default="Shared Documents/archive", help="server-relative target folder URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    target_folder = ctx.web.get_folder_by_server_relative_url(args.target_folder)
    with open(args.path, "rb") as f:
        uploaded = target_folder.files.create_upload_session(
            f, args.chunk_size, progress=progress_bar(f"Uploading {os.path.basename(args.path)}")
        ).execute_query()

    print(f"\nUploaded: {uploaded.server_relative_url}")


if __name__ == "__main__":
    main()
