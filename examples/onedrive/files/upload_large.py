"""
Upload a large file using a resumable upload session.

Reads from disk in chunks with progress reporting.
No full file loaded into memory.

Requires delegated permission Files.ReadWrite.
"""

import os
from pathlib import Path

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    local_path = Path("../../../tests/data/big_buck_bunny.mp4")
    file_size = os.path.getsize(local_path)

    def print_progress(uploaded_bytes: int) -> None:
        pct = uploaded_bytes / file_size * 100
        print(f"  Uploaded {uploaded_bytes:,} / {file_size:,} bytes ({pct:.1f}%)")

    print(f"Uploading {local_path.name} ({file_size:,} bytes)...")
    uploaded = client.me.drive.root.resumable_upload(str(local_path), chunk_uploaded=print_progress).execute_query()
    print(f"Uploaded: {uploaded.web_url}")


if __name__ == "__main__":
    main()
