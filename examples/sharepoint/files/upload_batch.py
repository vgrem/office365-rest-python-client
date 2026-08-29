"""
Demonstrates how to upload many files in a single batch request.

Each small file is queued as an upload and all of them are submitted with one
``execute_batch`` call — far fewer round-trips than one request per file.
"""

import argparse
import os

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

MAX_SMALL_FILE = 4 * 1024 * 1024


def main():
    parser = argparse.ArgumentParser(description="Bulk upload files to a SharePoint library")
    parser.add_argument("--source-dir", default="../../data", help="local directory with files to upload")
    parser.add_argument("--target-folder", default="Shared Documents/batch", help="server-relative target folder URL")
    parser.add_argument("--batch-size", type=int, default=100, help="files per batch request")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    local_files = [name for name in os.listdir(args.source_dir) if os.path.isfile(os.path.join(args.source_dir, name))]
    if not local_files:
        print(f"No files found in {args.source_dir}")
        return

    target_folder = ctx.web.get_folder_by_server_relative_url(args.target_folder)

    queued = 0
    for name in local_files:
        local_path = os.path.join(args.source_dir, name)
        with open(local_path, "rb") as f:
            content = f.read()
        if len(content) > MAX_SMALL_FILE:
            print(f"Skipping {name}: over 4 MB — use upload_large.py")
            continue
        target_folder.upload_file(name, content)  # queue
        queued += 1

    ctx.execute_batch(items_per_batch=args.batch_size)
    print(f"Uploaded {queued} file(s) to {args.target_folder}")


if __name__ == "__main__":
    main()
