"""
Import users from a CSV file via the streaming data pipeline (``from_csv``).

Each row becomes a user-create request; the file is streamed in chunks, so
memory stays bounded no matter how many rows it holds. Failures (for example a
UPN that already exists) are collected instead of aborting the run.

The sample file lives in ``examples/data/users.csv``; pass ``--path`` to import
your own. ``--domain`` sets the UPN domain for the ``userName`` column.

The whole CSV-to-payload correspondence is one function: ``map=`` receives a
chunk's records -- plain dicts, whatever the format -- and returns the records to
create. It builds the UPN and the mail nickname, enables the account, and nests
the password under ``passwordProfile``. A column ``map`` does not build is not
sent, so ``userName`` (which builds the UPN) never reaches the payload. Typing a
column is a different job: ``converters={column: spec}`` states it, declaratively.

The record-at-a-time counterpart is ``import.py``.

Requires delegated permission ``User.ReadWrite.All``.
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from office365.runtime.progress import progress_bar
from tests.settings import client_id, password, tenant, username

SAMPLE_CSV = Path(__file__).resolve().parents[2] / "data" / "users.csv"

#: Columns copied as-is when the file carries them: the rest is built above.
PROFILE = ("givenName", "surname", "displayName", "department", "jobTitle", "officeLocation", "city", "country")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk-provision users from a CSV file")
    parser.add_argument("--path", default=str(SAMPLE_CSV), help="CSV file (default: examples/data/users.csv)")
    parser.add_argument("--domain", default=tenant, help="UPN domain appended to each `userName` value")
    parser.add_argument("--chunk", type=int, default=50, help="rows per commit")
    parser.add_argument("--apply", action="store_true", help="create the users (default: preview only)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    def payload(rows: list[dict]) -> list[dict]:
        """Turn a chunk of CSV records into user-create records."""
        return [
            {
                "userPrincipalName": f"{row['userName']}@{args.domain}",
                "mailNickname": row["userName"],
                "accountEnabled": True,
                "passwordProfile/password": row["password"],
                **{name: row[name] for name in PROFILE if row.get(name)},
            }
            for row in rows
        ]

    result = client.users.from_csv(
        args.path,
        chunksize=args.chunk,
        map=payload,
        on_error="collect",
        dry_run=not args.apply,
        progress=progress_bar("Importing users"),
    ).execute_query()

    print(result.value.summary())
    for failure in result.checkpoint.failures:
        print(f"  {failure.get('error', failure)}")


if __name__ == "__main__":
    main()
