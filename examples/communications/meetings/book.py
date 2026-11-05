"""
Book online meetings idempotently — one from flags, many from a CSV.

Every booking is keyed on *your* ``externalId``: a re-run, a retried job, or two workers
racing on the same booking get the meeting that already exists instead of a second one.
That is the difference between this and a plain create call, and it is what makes a
booking sync safe to schedule.

CSV mode reads ``external_id,subject,start,minutes`` per row through the library's record
reader (the same one ``from_csv`` uses); ``start`` is ISO 8601 in UTC
(``2026-01-05T09:00``), and a row without ``minutes`` gets 30.

Requires the delegated permission ``OnlineMeetings.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onlinemeeting-createorget
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from office365.runtime.converters.csv_reader import read_csv_records
from tests.settings import client_id, password, tenant, username


def parse_start(value: str) -> datetime:
    """An ISO 8601 instant read as UTC when it carries no offset of its own."""
    moment = datetime.fromisoformat(value)
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def book(client: GraphClient, external_id: str, subject: str, start: datetime, minutes: int):
    """Create the meeting keyed on ``external_id``, or return the one that already has it."""
    return client.me.online_meetings.create_or_get(
        external_id=external_id,
        subject=subject,
        start_datetime=start,
        end_datetime=start + timedelta(minutes=minutes),
    ).execute_query()


def main() -> None:
    parser = argparse.ArgumentParser(description="Book online meetings idempotently")
    parser.add_argument("--csv", help="a file of bookings: external_id,subject,start,minutes")
    parser.add_argument("--external-id", help="your stable id for this meeting (default: derived from the start)")
    parser.add_argument("--subject", default="Customer demo")
    parser.add_argument("--start", help="ISO 8601 start in UTC (default: tomorrow at 09:00)")
    parser.add_argument("--minutes", type=int, default=30)
    args = parser.parse_args()

    if args.csv:
        with open(args.csv, newline="", encoding="utf-8-sig") as handle:
            bookings = [
                (
                    row["external_id"],
                    row.get("subject") or args.subject,
                    parse_start(row["start"]),
                    int(row.get("minutes") or 30),
                )
                for row in read_csv_records(handle)
            ]
    else:
        if args.start:
            start = parse_start(args.start)
        else:
            start = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
        bookings = [(args.external_id or f"booking-{start:%Y%m%d%H%M}", args.subject, start, args.minutes)]

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    for external_id, subject, start, minutes in bookings:
        meeting = book(client, external_id, subject, start, minutes)
        print(f"{external_id}\t{start:%Y-%m-%d %H:%M}\t{meeting.join_web_url}")


if __name__ == "__main__":
    main()
