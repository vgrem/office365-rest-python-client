"""
Download several Microsoft 365 usage reports concurrently.

``reports.download_report_async()`` streams each CSV through the async transport,
so independent reports overlap instead of running one after another. This is the
practical shape of a nightly compliance drop: gather the standard `*UserDetail`
reports into a dated folder and report the bytes written for each.

Requires application permission ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/resources/report
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from office365.graph_client import GraphClient
from office365.runtime.operations import Progress
from tests.settings import client_id, client_secret, tenant

REPORTS = (
    "getEmailActivityUserDetail",
    "getOneDriveActivityUserDetail",
    "getSharePointActivityUserDetail",
    "getTeamsUserActivityUserDetail",
)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


async def fetch(client: GraphClient, name: str, period: str, out_dir: Path) -> tuple[str, int]:
    def report_progress(progress: Progress) -> None:
        pct = f"{progress.percent:5.1f}%" if progress.total else "  ..."
        print(f"\r  {name}: {pct}", end="", flush=True)

    result = await client.reports.download_report_async(name, out_dir / f"{name}.csv", period, progress=report_progress)
    print(f"\r  {name}: {result.bytes_written:,} bytes -> {result.file_name}")
    return name, result.bytes_written


async def main() -> None:
    parser = argparse.ArgumentParser(description="Download several usage reports concurrently")
    parser.add_argument("--period", default="D30", help="D7/D30/D90/D180")
    parser.add_argument("--output-dir", default="usage_reports", help="destination folder")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    ensure_dir(out_dir)

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    async with client:
        results = await asyncio.gather(*(fetch(client, name, args.period, out_dir) for name in REPORTS))

    total = sum(size for _, size in results)
    print(f"\n{len(results)} reports, {total:,} bytes total in {out_dir}/")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(130)
