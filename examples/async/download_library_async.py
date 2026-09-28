"""
Download every file in a SharePoint library concurrently (async).

Lists the files of a library, then downloads them with a bounded number of
in-flight requests. Progress is reported as each download finishes, and each
file is retried on transient (throttling / 5xx) failures.

Each download runs on its own cloned context, which shares the parent's
credentials and HTTP connection pool — one token and one session for the whole
run. Bound the fan-out with ``--concurrency`` to stay polite to the server.

Requires ``Sites.Read.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from __future__ import annotations

import argparse
import asyncio
import os
import tempfile
import time

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


async def download_file(
    ctx: ClientContext,
    server_relative_url: str,
    output_dir: str,
    sem: asyncio.Semaphore,
) -> str:
    """Download one file on its own cloned context, retrying transient errors."""
    local_path = os.path.join(output_dir, os.path.basename(server_relative_url))
    async with sem:
        clone = ctx.clone(site_url)
        # A short local open; the blocking HTTP read runs off the loop inside download().
        with open(local_path, "wb") as stream:  # noqa: ASYNC230
            await (
                clone.web.get_file_by_server_relative_url(server_relative_url)
                .download(stream)
                .execute_query_async_retry(max_retry=5, timeout_secs=2)
            )
    return local_path


async def main() -> None:
    parser = argparse.ArgumentParser(description="Download a SharePoint library concurrently")
    parser.add_argument("--list-title", default="Documents", help="document library title")
    parser.add_argument("--output-dir", default=None, help="local output directory (default: temp)")
    parser.add_argument("--concurrency", type=int, default=6, help="max in-flight downloads (default: 6)")
    args = parser.parse_args()

    output_dir = args.output_dir or tempfile.mkdtemp()
    os.makedirs(output_dir, exist_ok=True)

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    # First page of the library; for large libraries collect paths with
    # ``.root_folder.files.get_all().execute_query()`` before downloading.
    files = await ctx.web.lists.get_by_title(args.list_title).root_folder.files.get().execute_query_async()
    urls = [f.server_relative_url for f in files if f.server_relative_url]
    if not urls:
        print(f"No files found in '{args.list_title}'.")
        return

    sem = asyncio.Semaphore(args.concurrency)
    tasks = [asyncio.ensure_future(download_file(ctx, url, output_dir, sem)) for url in urls]

    started = time.perf_counter()
    ok = 0
    for coro in asyncio.as_completed(tasks):
        try:
            local_path = await coro
            ok += 1
            print(f"[OK]   {local_path}")
        except Exception as e:  # noqa: BLE001 - keep downloading the rest
            print(f"[FAIL] {e}")

    elapsed = time.perf_counter() - started
    print(f"\nDownloaded {ok} of {len(urls)} files into {output_dir} ({elapsed:.1f}s)")


asyncio.run(main())
