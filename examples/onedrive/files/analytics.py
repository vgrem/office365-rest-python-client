"""
File analytics — view activity stats, get activities by time interval,
and check item views/modifications over time.

Shows who accessed a file, when, and how often. Useful for adoption
tracking, content governance, and understanding which files are
most actively used in a drive.

Requires delegated permission ``Files.Read`` and ``Analytics.Read``.

https://learn.microsoft.com/en-us/graph/api/itemanalytics-get
https://learn.microsoft.com/en-us/graph/api/driveitem-getactivitiesbyinterval
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    drive = client.me.drive

    # -- Step 1: pick a file to analyse (most recent) --
    items = drive.root.children.top(20).get().execute_query()
    files = [i for i in items if i.is_file]

    if not files:
        print("No files found in OneDrive root. Creating a test file...")
        drive.root.upload("analytics_test.txt", b"Analytics test content.").execute_query()
        files = drive.root.children.top(20).get().execute_query()
        files = [i for i in files if i.is_file]

    target = files[0]
    print(f"Analysing: {target.name}  (size: {target.size or 0} bytes)\n")

    # -- Step 2: get analytics for the item --
    try:
        analytics = target.analytics.get().execute_query()
        if analytics:
            print("Item analytics:")
            if hasattr(analytics, "all_time") and analytics.all_time:
                a = analytics.all_time
                print(f"  All time: {a.access_count or 0} accesses, {a.view_count or 0} views")
                print(f"            {a.share_count or 0} shares, {a.download_count or 0} downloads")
            if hasattr(analytics, "last_seven_days") and analytics.last_seven_days:
                l7 = analytics.last_seven_days
                print(f"  Last 7d : {l7.access_count or 0} accesses, {l7.view_count or 0} views")
        else:
            print("  (analytics returned no data — may need Analytics.Read permission)")
    except Exception as e:
        print(f"  (analytics not available: {e})")

    # -- Step 3: get activity by interval (last 30 days) --
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=30)
    end = now

    print("\nActivity by day for the last 30 days:")
    try:
        activities = target.get_activities_by_interval(
            start_dt=start,
            end_dt=end,
            interval="day",
        ).execute_query()

        print(f"  {len(activities)} days with activity")
        for act in activities:
            dt = act.start_date_time.strftime("%Y-%m-%d") if act.start_date_time else "?"
            access = act.access_count or 0
            act_view = act.view_count or 0
            act_down = act.download_count or 0
            act_share = act.share_count or 0
            print(f"  {dt}  accesses={access:>3}  views={act_view:>3}  downloads={act_down:>3}  shares={act_share:>2}")
    except Exception as e:
        print(f"  (activity by interval not available: {e})")

    # -- Step 4: item activity (who did what) --
    print("\nRecent activities on this file:")
    try:
        activities_v2 = target.get_activities_by_interval(
            start_dt=start,
            end_dt=end,
            interval="day",
        ).execute_query()
        if activities_v2:
            print("  (see activity timeline above — details available via activity insight resources)")
    except Exception as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
