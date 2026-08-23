"""
File analytics — view activity stats and access patterns for a file.

Shows the aggregated all-time and last-7-days counters plus a day-by-day
activity timeline over the last 30 days.

Requires delegated permissions ``Files.Read`` and ``Analytics.Read``.

https://learn.microsoft.com/en-us/graph/api/driveitem-get-analytics
https://learn.microsoft.com/en-us/graph/api/driveitem-list-activity
"""

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Show analytics and activity for a file")
    parser.add_argument("--name", required=True, help="name of the file to analyze (in your OneDrive root)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    item = client.me.drive.root.get_by_path(args.name).get().execute_query()
    print(f"File: {item.name}")

    # -- Step 1: aggregated analytics --
    analytics = item.analytics.select(["allTime", "lastSevenDays"]).get().execute_query()
    if analytics.all_time:
        a = analytics.all_time
        print(f"  All time:  {a.access.actionCount or 0} accesses by {a.access.actorCount or 0} actors")
    if analytics.last_seven_days:
        l7 = analytics.last_seven_days
        print(f"  Last 7d:   {l7.access.actionCount or 0} accesses by {l7.access.actorCount or 0} actors")

    # -- Step 2: day-by-day activity timeline --
    activities = item.get_activities_by_interval(
        start_dt=datetime.now(timezone.utc) - timedelta(days=30),
        end_dt=datetime.now(timezone.utc),
        interval="day",
    ).execute_query()
    print(f"\nActivity over the last 30 days ({len(activities)} days with activity):")
    for act in activities:
        print(f"  {act.start_date_time.date()}  accesses={act.access.actionCount or 0}")


if __name__ == "__main__":
    main()
