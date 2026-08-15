"""Parallel download of SharePoint files with ThreadPoolExecutor.

Each worker thread uses its own ClientContext, since a ClientContext is not
thread-safe (shared query queue / current-query state).

Token-cache caveat: per-thread contexts each build their own MSAL app and
acquire their own access token (plus OIDC discovery on first use). For small
fan-out this is fine; for many/long-running downloads, prefer sharing a single
token via ``with_access_token(...)`` or an MSAL ``SerializableTokenCache``
(note: it isn't safe to persist concurrently without a lock).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse
import concurrent.futures
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url, test_tenant


def download_one(path: str, output_dir: str) -> str:
    """Download a single file using its own thread-safe context."""
    ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
    local_path = os.path.join(output_dir, os.path.basename(path))
    with open(local_path, "wb") as local_file:
        ctx.web.get_file_by_server_relative_path(path).download(local_file).execute_query()
    return local_path


def main():
    parser = argparse.ArgumentParser(description="Download SharePoint files in parallel")
    parser.add_argument("paths", nargs="+", help="server-relative file paths to download")
    parser.add_argument("--max-workers", type=int, default=4, help="number of parallel workers (default: 4)")
    parser.add_argument("--output-dir", default=None, help="local output directory (default: temp)")
    args = parser.parse_args()

    output_dir = args.output_dir or tempfile.mkdtemp()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {executor.submit(download_one, path, output_dir): path for path in args.paths}
        ok = 0
        for future in concurrent.futures.as_completed(futures):
            path = futures[future]
            try:
                local_path = future.result()
                ok += 1
                print(f"[OK] {path} -> {local_path}")
            except Exception as e:
                print(f"[FAIL] {path}: {e}")

    print(f"\nDownloaded {ok} of {len(args.paths)} files into {output_dir}")


if __name__ == "__main__":
    main()
