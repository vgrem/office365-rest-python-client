"""
Export users to CSV using the deferred ``to_csv``.

Loads a page of users and writes them to a CSV file — columns follow ``.select()``.
The write happens after ``execute_query()`` completes the load.

https://learn.microsoft.com/en-us/graph/api/user-list
https://learn.microsoft.com/en-us/graph/api/resources/user

Requires delegated permission ``User.Read.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import cert_path, cert_thumbprint, client_id, tenant

COLUMNS = ["userPrincipalName", "displayName", "mail", "accountEnabled", "createdDateTime"]


def main():
    parser = argparse.ArgumentParser(description="Export users to CSV")
    parser.add_argument("--output", default="/tmp/users_export.csv", help="output CSV file")
    parser.add_argument("--top", type=int, default=10, help="number of users to export")
    args = parser.parse_args()

    with open(cert_path, "r", encoding="utf-8") as f:
        private_key = f.read()
    client = GraphClient(tenant=tenant).with_certificate(client_id, cert_thumbprint, private_key)

    users = client.users.top(args.top).select(COLUMNS).get()
    with open(args.output, "w", newline="") as f:
        users.to_csv(f).execute_query()

    print(f"✓ Exported users to {args.output}")


if __name__ == "__main__":
    main()
