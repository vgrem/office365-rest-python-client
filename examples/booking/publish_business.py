"""
Publish a booking business's scheduling page.

Makes the scheduling page available to external customers and sets the
``publicUrl`` property.

Requires delegated permission ``Bookings.ReadWrite.All`` (or
``Bookings.Manage.All``).

https://learn.microsoft.com/en-us/graph/api/bookingbusiness-publish
"""

import argparse
import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Publish a booking business scheduling page")
    parser.add_argument("--id", required=True, help="booking business id")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    biz = client.solutions.booking_businesses[args.id].get_or_none().execute_query()
    if not biz.is_loaded:
        sys.exit(f"No booking business with id: {args.id}")

    biz.publish().execute_query()
    print(f"✓ Scheduling page published: {biz.properties.get('publicUrl', '?')}")


if __name__ == "__main__":
    main()
