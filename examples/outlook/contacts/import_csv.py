"""
Import contacts from a CSV file via the data pipeline (``from_records``).

Email addresses are nested ``EmailAddress`` values, so a small transform builds
them from plain strings before the creates are queued and committed in batches
(``execute_batch``) with a determinate progress bar.

Requires delegated permission ``Contacts.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-post-contacts
"""

from __future__ import annotations

import argparse
import csv

from office365.graph_client import GraphClient
from office365.outlook.calendar.email_address import EmailAddress
from office365.runtime.operations import Progress
from tests.settings import client_id, password, tenant, username


def build_records(path: str) -> list[dict]:
    """Read a CSV (displayName,givenName,surname,email;...) into import records."""
    records = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            record = {k: v for k, v in row.items() if k != "email" and v}
            emails = [e.strip() for e in (row.get("email") or "").split(";") if e.strip()]
            if emails:
                record["emailAddresses"] = [EmailAddress(address=e) for e in emails]
            records.append(record)
    return records


def progress_bar(description: str):
    """tqdm-backed hook — the library only needs a ``Callable[[Progress], None]``."""
    from tqdm import tqdm

    bar = tqdm(desc=description)

    def hook(p: Progress) -> None:
        if p.total is not None and bar.total is None:
            bar.total = p.total
        bar.update(p.done - bar.n)
        if p.total is not None and p.done >= p.total:
            bar.close()

    return hook


def main():
    parser = argparse.ArgumentParser(description="Import contacts from a CSV via the data pipeline")
    parser.add_argument("--path", required=True, help="CSV file with displayName,givenName,surname,email;...")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    records = build_records(args.path)

    client.me.contacts.from_records(records, progress=progress_bar("Importing contacts"))
    client.execute_batch(100)
    print(f"Imported {len(records)} contacts")


if __name__ == "__main__":
    main()
