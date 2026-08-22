"""
List all Microsoft Bookings businesses in the tenant.

Requires delegated permission ``Bookings.Read.All``.

https://learn.microsoft.com/en-us/graph/api/bookingbusiness-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    argparse.ArgumentParser(description="List booking businesses").parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    businesses = client.solutions.booking_businesses.get().execute_query()
    print(f"Booking businesses: {len(businesses)}")
    for b in businesses:
        address = b.address
        city = address.city if address else "?"
        print(f"  {b.id:40s} {b.display_name or '(unnamed)':30s} city={city}")


if __name__ == "__main__":
    main()
