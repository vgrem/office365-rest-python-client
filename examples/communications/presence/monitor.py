"""
Presence monitoring — the "routing desk" pattern.

Poll a set of agents with ``getPresencesByUserId`` (one request per cycle),
remember the previous state, and act only on transitions. The action takes user
*object ids*, so addresses are resolved once up front. The helpers below
also show the business rules: who is reachable, and how to drive an agent's
own presence session when their shift starts or ends.

Requires the delegated permissions ``Presence.Read.All`` and, with ``--apply``,
``Presence.ReadWrite``.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from time import sleep

from office365.communications.presences.presence import Presence
from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, password, tenant, username

BUSY_ACTIVITIES = {"InACall", "InAConferenceCall", "InAMeeting", "Presenting", "OffWork", "OutOfOffice"}
UNREACHABLE_AVAILABILITY = {"DoNotDisturb", "Offline", "PresenceUnknown"}


def is_available(presence: Presence) -> bool:
    """Reachable = not explicitly unavailable and not stuck in an activity that blocks the desk."""
    if not presence.availability or not presence.activity:
        return False
    return presence.availability not in UNREACHABLE_AVAILABILITY and presence.activity not in BUSY_ACTIVITIES


def describe(presence: Presence) -> str:
    return f"availability={presence.availability}, activity={presence.activity}"


def route_call(client: GraphClient, agents: list[str], labels: dict[str, str]) -> None:
    """Pick the first reachable agent using a single bulk presence request."""
    presences = client.communications.get_presences_by_user_id(agents).execute_query()
    available = next((p for p in presences if is_available(p)), None)
    answer = f"call {labels.get(available.id, available.id)}" if available else "no agent available — queue the call"
    print(f"Routing: {answer}")


def set_shift(client: GraphClient, on_duty: bool) -> None:
    """Drive *your own* presence session when a shift starts or ends.

    The preferred presence expires on its own after 9 hours. Note that Graph
    refuses to set **another** user's presence with delegated credentials
    ("Cannot set the presence of another user") — that needs an application
    permission such as ``Presence.ReadWrite.All``.
    """
    presence = client.me.presence
    expires = datetime.now(timezone.utc) + timedelta(hours=9)
    if on_duty:
        presence.set_user_preferred_presence("Available", "Available", "PT9H").execute_query()
    else:
        presence.set_user_preferred_presence("Offline", "OffWork", "PT9H").execute_query()
    presence.set_status_message("Online and ready" if on_duty else "Shift ended", expires).execute_query()
    print(f"You are now {'on duty' if on_duty else 'off duty'}")


def monitor(client: GraphClient, agents: list[str], cycles: int, interval: int, labels: dict[str, str]) -> None:
    print(f"Watching {len(agents)} agent(s), {cycles} cycle(s) every {interval}s\n")
    previous: dict[str, str] = {}
    for cycle in range(1, cycles + 1):
        for presence in client.communications.get_presences_by_user_id(agents).execute_query():
            state = describe(presence)
            change = "" if previous.get(presence.id) in (None, state) else f"  (was {previous[presence.id]})"
            print(f"  [{cycle}/{cycles}] {labels.get(presence.id, presence.id)}: {state}{change}")
            previous[presence.id] = state
        if cycle < cycles:
            sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Monitor agent presence and route calls")
    parser.add_argument("--agents", nargs="+", default=[admin_username], help="UPNs or object ids to watch")
    parser.add_argument("--cycles", type=int, default=3, help="number of polls")
    parser.add_argument("--interval", type=int, default=15, help="seconds between polls")
    parser.add_argument(
        "--apply",
        choices=["on-duty", "off-duty"],
        help="also start/end your own shift (sets a preferred presence that expires in 9h)",
    )
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    # ``getPresencesByUserId`` takes user *object ids*: an address here answers PresenceUnknown
    # for everyone, so addresses are resolved first and kept as labels for the output.
    ids = [client.users[agent].get().execute_query().id if "@" in agent else agent for agent in args.agents]
    labels = dict(zip(ids, args.agents))

    monitor(client, ids, args.cycles, args.interval, labels)
    route_call(client, ids, labels)
    if args.apply:
        set_shift(client, on_duty=args.apply == "on-duty")


if __name__ == "__main__":
    main()
