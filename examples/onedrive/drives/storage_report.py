"""Tenant-wide drive storage report.

Lists every drive (personal OneDrive and SharePoint document libraries) with
its owner, type, and quota usage, flagging drives near or over quota.

Requires application permissions ``Files.Read.All`` and ``Sites.Read.All``.

https://learn.microsoft.com/en-us/graph/api/drive-list
"""

from collections import Counter

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

WARN_PCT = 85
GIB = 1024**3

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Files.Read.All", "Sites.Read.All")
)

drives = client.drives.get().execute_query()
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
    flag = " <<<" if pct > WARN_PCT else ""
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
