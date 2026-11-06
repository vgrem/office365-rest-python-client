"""
Find, retitle, move or cancel an online meeting — printing the change before making it.

A meeting is named the way a ticket names it: by the ``joinWebUrl`` in the invite, or by
its id if your own system kept one. There is no "list my online meetings" — ``/me/onlineMeetings``
without a filter answers *InvalidArgument* — so those two lookups are the whole choice.

Writes need ``--apply``. Without it the script prints what it would send and stops, which
is the difference between reading a ticket and acting on it.

Requires the delegated permission ``OnlineMeetings.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onlinemeeting-update
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from office365.runtime.exceptions import ObjectNotFoundException
from tests.settings import client_id, password, tenant, username


def parse_start(value: str) -> datetime:
    """An ISO 8601 instant read as UTC when it carries no offset of its own."""
    moment = datetime.fromisoformat(value)
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def lookup(client: GraphClient, join_url: str | None, meeting_id: str | None):
    """The meetings matching the one name the caller has: an id, or the join link a filter can address."""
    if meeting_id:
        return [client.me.online_meetings[meeting_id].get().execute_query()]
    try:
        return list(client.me.online_meetings.filter(f"JoinWebUrl eq '{join_url}'").get().execute_query())
    except ObjectNotFoundException:
        # A join URL that matches nothing answers 404 ("Specified meeting is not found"), not
        # an empty page: Graph resolves this filter server-side, so a miss is not a short list.
        return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Find and change one online meeting")
    name = parser.add_mutually_exclusive_group(required=True)
    name.add_argument("--join-url", help="the joinWebUrl from the invite")
    name.add_argument("--meeting-id", help="the meeting id, if your own system kept one")
    parser.add_argument("--subject", help="retitle the meeting")
    parser.add_argument("--start", help="move the start (ISO 8601); keeps the duration")
    parser.add_argument("--minutes", type=int, help="duration of the moved meeting, with --start")
    parser.add_argument("--cancel", action="store_true", help="delete the meeting")
    parser.add_argument("--apply", action="store_true", help="send the change; without it nothing is written")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    meetings = lookup(client, args.join_url, args.meeting_id)
    if not meetings:
        raise SystemExit("No meeting matches — check the join URL.")
    for meeting in meetings:
        when = f"{meeting.start_datetime} → {meeting.end_datetime}"
        print(f"found: {meeting.subject or '(no subject)'} · {when} · {meeting.id}")

    changes = {}
    if args.subject:
        changes["subject"] = args.subject
    if args.start:
        start = parse_start(args.start)
        duration = meetings[0].end_datetime - meetings[0].start_datetime
        minutes = args.minutes or int(duration.total_seconds() // 60)
        changes["startDateTime"] = start
        changes["endDateTime"] = start + timedelta(minutes=minutes)

    for meeting in meetings:
        if args.cancel:
            print(f"{'cancelling' if args.apply else 'would cancel'}: {meeting.id}")
            if args.apply:
                meeting.delete_object().execute_query()
            continue
        if not changes:
            print("nothing to change — pass --subject, --start or --cancel")
            continue
        print(f"{'updating' if args.apply else 'would update'} {meeting.id}: {changes}")
        if args.apply:
            meeting.update_properties(**changes).execute_query()


if __name__ == "__main__":
    main()
