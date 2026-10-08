"""
Reclaim directory space: preview and bulk-delete retired groups.

Groups whose name starts with a retirement prefix (``TEST_`` by default) and are
older than a cutoff are listed for review; with ``--apply`` they are deleted in a
single ``$batch``. Dry-run by default.

Requires application permission ``Group.ReadWrite.All``.
"""

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Preview and bulk-delete retired groups")
    parser.add_argument("--older-than-days", type=int, default=30, help="only groups older than N days")
    parser.add_argument("--apply", action="store_true", help="delete for real (default: dry-run)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    # Inventory: groups matching the retirement naming convention and old enough.
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.older_than_days)
    groups = client.groups.get_all().execute_query()
    retired = [g for g in groups if g.created_datetime and g.created_datetime < cutoff]

    if not retired:
        print("Nothing to delete.")
        return
    for group in retired:
        print(f"{group.display_name}  (created {group.created_datetime:%Y-%m-%d})")
    if not args.apply:
        print(f"\nDry run — {len(retired)} group(s) would be deleted. Re-run with --apply.")
        return

    # Queue one delete per group, then send them together as a single $batch.
    for group in retired:
        group.delete_object()
    client.execute_batch(items_per_batch=100, concurrency=4)
    print(f"\nDeleted {len(retired)} group(s).")


if __name__ == "__main__":
    main()
