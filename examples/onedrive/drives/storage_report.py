"""
Tenant-wide drive storage report.

Lists every drive (personal OneDrive and SharePoint document libraries) with
its owner, type, and quota usage, flagging drives near or over quota. A core
capacity-planning report for administrators.

Requires application permissions ``Files.Read.All`` and ``Sites.Read.All``.

https://learn.microsoft.com/en-us/graph/api/drive-list
"""

import argparse
from collections import Counter

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

WARN_PCT = 85
GIB = 1024**3


def main():
    parser = argparse.ArgumentParser(description="Report storage usage across all tenant drives")
    parser.add_argument("--warn-pct", type=float, default=WARN_PCT, help="quota warning threshold %% (default: 85)")
    parser.add_argument("--max-drives", type=int, default=0, help="max drives to scan, 0 = all (default: 0)")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("Files.Read.All", "Sites.Read.All")
    )

    drives = client.drives.get().execute_query()
    if args.max_drives > 0:
        drives = list(drives)[: args.max_drives]

    print(f"{'Name':45s} {'Type':14s} {'Owner':30s} {'Used':>8s} {'Quota':>8s} {'%':>6s}")
    print("-" * 120)

    near_quota = 0
    total_used = 0
    by_type = Counter()
    for drive in drives:
        quota = drive.quota
        used = quota.used or 0
        total = quota.total or 0
        pct = used / total * 100 if total else 0.0
        owner = drive.owner.user.displayName or "?"
        name = drive.properties.get("name") or drive.id or "?"
        flag = " <<<" if pct > args.warn_pct else ""
        if flag:
            near_quota += 1
        by_type[drive.drive_type or "?"] += 1
        total_used += used
        print(
            f"{name:45s} {(drive.drive_type or '?'):14s} {owner:30s} "
            f"{used / GIB:>7.1f}G {total / GIB:>7.1f}G {pct:>5.1f}%{flag}"
        )

    print(f"\n{len(drives)} drives, {near_quota} near/over quota, {total_used / GIB:.1f}G used in total")
    print("By type:", dict(by_type))


if __name__ == "__main__":
    main()
