"""
The whole team's presence as one table — one bulk request, exported as CSV.

``getPresencesByUserId`` answers up to 650 users per call, so a board of 200 people is one
request instead of 200. It takes user *object ids*, and answers ``PresenceUnknown`` for an
address it is handed — which reads as "offline". ``get_presences_by_principal_name`` closes
that gap: it reads the names from the directory, calls the action with the ids, and one
``execute_query()`` runs both.

The rows leave as CSV in the presence type's declared columns, so ``--out team.csv`` opens
directly in Excel or pandas. They are keyed by the object id the action answers, not by the
address you typed — keep your input list beside the file when you need the addresses back.

Requires the delegated permissions ``Presence.Read.All`` (the action) and ``User.Read.All``
(the directory read behind each name).

https://learn.microsoft.com/en-us/graph/api/cloudcommunications-getpresencesbyuserid
"""

from __future__ import annotations

import argparse
import sys

from office365.graph_client import GraphClient
from office365.runtime.converters.csv_reader import read_csv_records
from tests.settings import client_id, password, tenant, username


def main() -> None:
    parser = argparse.ArgumentParser(description="Presence board for a list of users")
    parser.add_argument("--users", nargs="+", default=[], help="user principal names, e.g. mdoe@contoso.com")
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

    presences = client.communications.get_presences_by_principal_name(identifiers)
    presences.execute_query()

    if args.out:
        presences.to_csv(args.out)
        print(f"{len(presences)} of {len(identifiers)} users written to {args.out}")
    else:
        presences.to_csv(sys.stdout)


if __name__ == "__main__":
    main()
