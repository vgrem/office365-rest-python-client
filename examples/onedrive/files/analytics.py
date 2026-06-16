"""
File analytics — view activity stats and access patterns.

Requires delegated permissions Files.Read and Analytics.Read.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    drive = client.sites.get_by_path("/sites/project").drive
    files = [i for i in drive.root.children.top(20).get().execute_query() if i.is_file]
    if not files:
        print("No files found.")
        return

    target = files[0]
    print(f"File: {target.name}")

    analytics = target.analytics.select(["allTime"]).get().execute_query()
    if analytics.all_time:
        a = analytics.all_time
        print(f"  All time: {a.accessCount or 0} accesses, {a.viewCount or 0} views, {a.shareCount or 0} shares")
    if analytics.last_seven_days:
        l7 = analytics.last_seven_days
        print(f"  Last 7d:  {l7.accessCount or 0} accesses, {l7.viewCount or 0} views")

    activities = target.get_activities_by_interval(
        start_dt=datetime.now(timezone.utc) - timedelta(days=30),
        end_dt=datetime.now(timezone.utc),
        interval="day",
    ).execute_query()
    print(f"\nActivity ({len(activities)} days with activity):")
    for act in activities:
        print(f"  {act.start_date_time.date()}  accesses={act.accessCount or 0}  views={act.viewCount or 0}")


if __name__ == "__main__":
    main()
