"""
Diagnose SharePoint Online performance via the SPRequestDuration response header.

Runs a configurable workload a number of times and reports both the
server-side processing time (SPRequestDuration header) and the client wall
time, with a min/max/avg summary. Results can optionally be exported to CSV.

https://learn.microsoft.com/en-us/microsoft-365/enterprise/
diagnosing-performance-issues-with-sharepoint-online?view=o365-worldwide
"""

import argparse
import csv
import statistics
import time

from office365.sharepoint.client_context import ClientContext
from requests import Response
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

SP_REQUEST_DURATION = "SPRequestDuration"


def _run_once(ctx: ClientContext, workload: str, list_title: str, headers: list) -> float:
    """Run the workload once, capture the SPRequestDuration header, return wall time in ms."""

    def _capture(resp: Response) -> None:
        headers.append(resp.headers.get(SP_REQUEST_DURATION))

    started = time.monotonic()
    if workload == "web":
        ctx.web.get().after_execute(_capture, include_response=True).execute_query()
    elif workload == "lists":
        ctx.web.lists.get().after_execute(_capture, include_response=True).execute_query()
    elif workload == "items":
        ctx.web.lists.get_by_title(list_title).items.top(100).select(["Id"]).get().after_execute(
            _capture, include_response=True
        ).execute_query()
    else:  # search
        ctx.search.query("IsDocument:1", row_limit=10).after_execute(_capture, include_response=True).execute_query()
    return (time.monotonic() - started) * 1000


def _summary(values: list) -> dict:
    values = [v for v in values if v is not None]
    if not values:
        return {"min": 0.0, "max": 0.0, "avg": 0.0, "total": 0.0}
    return {
        "min": min(values),
        "max": max(values),
        "avg": statistics.mean(values),
        "total": sum(values),
    }


def main():
    parser = argparse.ArgumentParser(description="Measure SharePoint request performance (SPRequestDuration)")
    parser.add_argument("--workload", choices=["web", "lists", "items", "search"], default="web")
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--list-title", default="Documents", help="List to load for the 'items' workload")
    parser.add_argument("--output", help="Optional CSV output path")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    server_ms: list = []
    wall_ms: list = []
    print(f"Workload '{args.workload}' — {args.iterations} iterations:\n")
    for i in range(args.iterations):
        headers: list = []
        wall = _run_once(ctx, args.workload, args.list_title, headers)
        server = int(headers[0]) if headers and headers[0] else None
        server_ms.append(server)
        wall_ms.append(wall)
        print(f"  #{i + 1:2d}  server: {server if server else 0:6} ms   wall: {wall:7.0f} ms")

    server = _summary(server_ms)
    wall = _summary(wall_ms)
    print("\nSummary (server-side SPRequestDuration, ms):")
    print(
        f"  min {server['min']:6.0f}  max {server['max']:6.0f}  avg {server['avg']:6.1f}  total {server['total']:8.0f}"
    )
    print("Summary (client wall time, ms):")
    print(f"  min {wall['min']:6.0f}  max {wall['max']:6.0f}  avg {wall['avg']:6.1f}  total {wall['total']:8.0f}")

    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["iteration", "server_ms", "wall_ms"])
            for i, (server_val, wall_val) in enumerate(zip(server_ms, wall_ms), 1):
                writer.writerow([i, server_val or "", round(wall_val, 1)])
        print(f"\nResults exported to {args.output}")


if __name__ == "__main__":
    main()
