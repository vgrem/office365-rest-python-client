"""
Add a customer to a booking business.

Requires delegated permission ``Bookings.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/bookingbusiness-post-customers
"""

import argparse
import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Add a customer to a booking business")
    parser.add_argument("--id", required=True, help="booking business id")
    parser.add_argument("--name", required=True, help="customer display name")
    parser.add_argument("--email", required=True, help="customer email address")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    businesses = client.solutions.booking_businesses.get().execute_query()
    biz = next((b for b in businesses if b.id == args.id), None)
    if biz is None:
        sys.exit(f"No booking business with id: {args.id}")

    customer = biz.customers.add(displayName=args.name, emailAddress=args.email).execute_query()
    print(f"✓ Customer added: {customer.id}")


if __name__ == "__main__":
    main()
