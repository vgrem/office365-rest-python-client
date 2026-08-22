"""
Get staff availability for a booking business over the next N days.

Requires delegated permission ``Bookings.Read.All``.

https://learn.microsoft.com/en-us/graph/api/bookingbusiness-post-getstaffavailability
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

AVAILABILITY_STATUS = {
    "0": "available",
    "1": "busy",
    "2": "slots available",
    "3": "out of office",
    "-1": "none",
}


def main():
    parser = argparse.ArgumentParser(description="Get staff availability for a booking business")
    parser.add_argument("--id", required=True, help="booking business id")
    parser.add_argument("--days", type=int, default=7, help="number of days to look ahead (default 7)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    businesses = client.solutions.booking_businesses.get().execute_query()
    biz = next((b for b in businesses if b.id == args.id), None)
    if biz is None:
        sys.exit(f"No booking business with id: {args.id}")

    staff = biz.staff_members.get().execute_query()
    if not staff:
        print("No staff members found.")
        return

    now = datetime.now(timezone.utc)
    result = biz.get_staff_availability(
        staff_ids=[s.id for s in staff if s.id],
        start_datetime=now,
        end_datetime=now + timedelta(days=args.days),
    ).execute_query()

    for item in result.value:
        name = next((s.properties.get("displayName", "?") for s in staff if s.id == item.staffId), item.staffId)
        print(f"\n  {name}:")
        for slot in item.availabilityItems:
            status = AVAILABILITY_STATUS.get(str(slot.status.value), str(slot.status.value))
            print(f"    {status:15s} {slot.startDateTime} -> {slot.endDateTime}")


if __name__ == "__main__":
    main()
