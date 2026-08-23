"""
Site activity analytics — daily views and edits over a rolling window.

Requires delegated permission ``Sites.Read.All``.

https://learn.microsoft.com/en-us/graph/api/itemactivitystat-getactivitybyinterval
"""

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Site activity analytics — daily views and edits over a rolling window")
    parser.add_argument("--site-url", default=team_site_url, help="site URL to inspect")
    parser.add_argument("--days", type=int, default=30, help="rolling window length in days")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("Sites.Read.All")
    )

    site = client.sites.get_by_url(args.site_url).get().execute_query()

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=args.days)
    stats = site.get_activities_by_interval(start, end, "day").execute_query()
    print(f"Activity for {site.display_name} (last {args.days} days):")
    for s in stats:
        views = s.access.viewCount
        edits = s.edit.viewCount
        print(f"  {s.start_date_time:%Y-%m-%d}  views={views}  edits={edits}")


if __name__ == "__main__":
    main()
