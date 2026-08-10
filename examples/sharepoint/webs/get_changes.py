"""Recent site changes report.

Pulls the latest changes from the site's change log and summarizes them by
change type (added / updated / deleted), then lists the most recent item
changes with their item id and editor.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone

from office365.sharepoint.changes.item import ChangeItem
from office365.sharepoint.changes.query import ChangeQuery
from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def _aware(value: datetime) -> datetime:
    """Ensure a timestamp is timezone-aware for comparison."""
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def main():
    parser = argparse.ArgumentParser(description="Recent site changes report")
    parser.add_argument("--days", type=int, default=7, help="report changes within the last N days (default: 7)")
    parser.add_argument("--limit", type=int, default=10, help="number of recent changes to list (default: 10)")
    args = parser.parse_args()

    client = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    query = ChangeQuery(Item=True, Web=True, List=True, FetchLimit="200", LatestFirst=True)
    changes = client.web.get_changes(query).execute_query()

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    recent = [c for c in changes if _aware(c.time) >= cutoff]

    counts = Counter(c.change_type.name for c in recent)
    print(f"Changes in the last {args.days} day(s) ({len(recent)}):")
    for name, count in counts.most_common():
        print(f"  {name:15s} {count}")

    print(f"\nMost recent ({min(args.limit, len(recent))}):")
    for c in recent[: args.limit]:
        item = f"  item={c.item_id}" if isinstance(c, ChangeItem) and c.item_id else ""
        editor = f"  editor={c.editor_login_name}" if isinstance(c, ChangeItem) and c.editor_login_name else ""
        print(f"  {_aware(c.time):%Y-%m-%d %H:%M}  {c.change_type.name}{item}{editor}")


if __name__ == "__main__":
    main()
