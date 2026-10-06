"""
Show a booking business: hours, services, staff, and customers.

Requires delegated permission ``Bookings.Read.All``.

https://learn.microsoft.com/en-us/graph/api/bookingbusiness-get
"""

import argparse
import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def _get_business(client: GraphClient, business_id: str):
    biz = client.solutions.booking_businesses[business_id].get_or_none().execute_query()
    if not biz.is_loaded:
        sys.exit(f"No booking business with id: {business_id}")
    return biz


def main():
    parser = argparse.ArgumentParser(description="Show a booking business")
    parser.add_argument("--id", required=True, help="booking business id")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    biz = _get_business(client, args.id)
    print(f"Inspecting: {biz.display_name} ({biz.id})")

    print("  Business hours:")
    for wh in biz.business_hours:
        print(f"    {wh.day}  {wh.timeSlots}")

    services = biz.services.get().execute_query()
    print(f"\n  Services ({len(services)}):")
    for s in services:
        display = s.properties.get("displayName", "?")
        duration = s.properties.get("duration", "?")
        price = s.properties.get("defaultPrice", "?")
        print(f"    {display:35s}  duration={duration}  price={price}")

    staff = biz.staff_members.get().execute_query()
    print(f"\n  Staff members ({len(staff)}):")
    for s in staff:
        name = s.properties.get("displayName", "?")
        email = s.properties.get("emailAddress", "?")
        print(f"    {name:25s}  {email}")

    customers = biz.customers.get().execute_query()
    print(f"\n  Customers: {len(customers)}")


if __name__ == "__main__":
    main()
