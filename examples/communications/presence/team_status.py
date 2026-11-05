"""
The whole team's presence as one table — a single bulk request, exported as CSV.

``getPresencesByUserId`` answers up to 650 users per call, so a board of 200 people is one
request instead of 200. It takes user *object ids*, which is why this script resolves the
UPNs or mail addresses you type into ids first: a list of colleagues is written as
addresses, not GUIDs.

The rows leave through the same export pipeline a SharePoint list uses (``export_to``), so
the columns are the presence type's declared ones and ``--out team.csv`` opens directly in
Excel or pandas. They are keyed by the object id the action answers, not by the address you
typed — keep your input list beside the file when you need the addresses back.

Requires the delegated permission ``Presence.Read.All``.

https://learn.microsoft.com/en-us/graph/api/cloudcommunications-getpresencesbyuserid
"""

from __future__ import annotations

import argparse
import sys

from office365.graph_client import GraphClient
from office365.runtime.converters.csv_reader import read_csv_records
from tests.settings import client_id, password, tenant, username


def resolve(client: GraphClient, values: list[str]) -> list[str]:
    """The user object ids behind the identifiers given — an address is looked up, an id is kept."""
    return [client.users[value].get().execute_query().id if "@" in value else value for value in values]


def main() -> None:
    parser = argparse.ArgumentParser(description="Presence board for a list of users")
    parser.add_argument("--users", nargs="+", default=[], help="UPNs, mail addresses or user object ids")
    parser.add_argument("--csv", help="a file whose 'user' column lists them instead")
    parser.add_argument("--out", help="write the table to a CSV file instead of stdout")
    args = parser.parse_args()

    identifiers = list(args.users)
    if args.csv:
        with open(args.csv, newline="", encoding="utf-8-sig") as handle:
            identifiers += [row["user"] for row in read_csv_records(handle)]
    if not identifiers:
        parser.error("give --users or --csv")

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    presences = client.communications.get_presences_by_user_id(resolve(client, identifiers))
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as handle:
            presences.export_to(handle, format="csv").execute_query()
        print(f"{len(identifiers)} users written to {args.out}")
    else:
        presences.export_to(sys.stdout, format="csv").execute_query()


if __name__ == "__main__":
    main()
