"""
Create a Microsoft Bookings business in the tenant.

Requires delegated permission ``Bookings.ReadWrite.All`` (or
``Bookings.Manage.All``).

https://learn.microsoft.com/en-us/graph/api/bookingbusiness-post
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a booking business")
    parser.add_argument("--name", default="SDK Demo Consulting", help="business display name")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    business = client.solutions.booking_businesses.add(args.name).execute_query()
    print(f"✓ Created business: {business.display_name} ({business.id})")


if __name__ == "__main__":
    main()
