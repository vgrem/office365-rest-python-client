"""
Book online meetings idempotently — one from flags, a whole file from CSV.

Every booking is keyed on *your* ``externalId``: a re-run, a retried job, or two workers
racing on the same booking get the meeting that already exists instead of a second one.
That is the difference between this and a plain create call, and it is what makes a
booking sync safe to schedule. A CSV import books nothing twice for the same reason — the
collection's import queues a ``createOrGet`` per row, not a create.

The CSV columns are the meeting's own — ``externalId,subject,startDateTime,endDateTime``
(ISO 8601 in UTC) — so the file needs no per-row code: the import maps each header onto
the model. A row without ``subject`` gets it from the flags; a row's times are its own.

Requires the delegated permission ``OnlineMeetings.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onlinemeeting-createorget
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def parse_start(value: str) -> datetime:
    """An ISO 8601 instant read as UTC when it carries no offset of its own."""
    moment = datetime.fromisoformat(value)
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Book online meetings idempotently")
    parser.add_argument("--csv", help="a file of bookings: externalId,subject,startDateTime,endDateTime")
    parser.add_argument("--external-id", help="your stable id for this meeting (default: derived from the start)")
    parser.add_argument("--subject", default="Customer demo")
    parser.add_argument("--start", help="ISO 8601 start in UTC (default: tomorrow at 09:00)")
    parser.add_argument("--minutes", type=int, default=30)
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    meetings = client.me.online_meetings

    if args.csv:
        stats = meetings.from_csv(args.csv).execute_query().value
        print(f"{stats.success} of {stats.total} booking(s) in place — keyed on externalId, so a re-run adds none")
        return

    start = (
        parse_start(args.start)
        if args.start
        else (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    )
    meeting = meetings.create_or_get(
        external_id=args.external_id or f"booking-{start:%Y%m%d%H%M}",
        subject=args.subject,
        start_datetime=start,
        end_datetime=start + timedelta(minutes=args.minutes),
    ).execute_query()
    print(f"{meeting.external_id}\t{start:%Y-%m-%d %H:%M}\t{meeting.join_web_url}")


if __name__ == "__main__":
    main()
