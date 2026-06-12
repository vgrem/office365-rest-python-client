"""
Teams presence and telephony status monitor.

Covers: single/bulk presence queries, preferred presence, status messages,
polling for state changes, and business-rules routing logic.

Required permissions: Presence.Read, Presence.Read.All, Presence.ReadWrite.
"""

from datetime import datetime, timedelta, timezone
from time import sleep
from typing import Optional

from office365.graph_client import GraphClient

POLL_INTERVAL = 30
BUSY_ACTIVITIES = {"InACall", "InAConferenceCall", "InAMeeting", "Presenting"}


def is_available(presence) -> bool:
    availability = presence.get_property("availability")
    activity = presence.get_property("activity")
    if not availability or not activity:
        return False
    if availability in ("DoNotDisturb", "Offline", "PresenceUnknown"):
        return False
    if activity in BUSY_ACTIVITIES | {"OffWork", "OutOfOffice"}:
        return False
    return True


def agent_status_summary(presence) -> str:
    a = presence.get_property("availability") or "Unknown"
    b = presence.get_property("activity") or "Unknown"
    return f"availability={a}, activity={b}"


def take_agent_offline(client: GraphClient, user_id: str):
    expires = datetime.now(timezone.utc) + timedelta(hours=9)
    client.communications.presences[user_id].set_user_preferred_presence(
        availability="DoNotDisturb", activity="OffWork", expiration_duration="PT9H",
    ).execute_query()
    client.communications.presences[user_id].set_status_message(
        message="Shift ended", expiry=expires,
    ).execute_query()


def start_shift(client: GraphClient, user_id: str):
    expires = datetime.now(timezone.utc) + timedelta(hours=9)
    client.communications.presences[user_id].set_user_preferred_presence(
        availability="Available", activity="Available", expiration_duration="PT9H",
    ).execute_query()
    client.communications.presences[user_id].set_status_message(
        message="Online and ready", expiry=expires,
    ).execute_query()


def find_available_agent(client: GraphClient, agents: list[str]) -> Optional[str]:
    presences = client.communications.get_presences_by_user_id(agents).execute_query()
    for e in presences:
        if is_available(e):
            return e.id
    return None


def monitor_presence(client: GraphClient, agents: list[str], cycles: int = 3):
    print(f"Monitoring {len(agents)} agents (poll every {POLL_INTERVAL}s)")
    previous = {}
    for cycle in range(1, cycles + 1):
        presences = client.communications.get_presences_by_user_id(agents).execute_query()
        for e in presences:
            state = agent_status_summary(e)
            old = previous.get(e.id)
            if old is None:
                print(f"  INIT  {e.id}: {state}")
            elif state != old:
                print(f"  CHG   {e.id}: {old} -> {state}")
            previous[e.id] = state
        if cycle < cycles:
            sleep(POLL_INTERVAL)


def main():
    client = GraphClient().with_device_flow(client_id="your_client_id")
    agents = ["alice@company.com", "bob@company.com", "carol@company.com"]

    presences = client.communications.get_presences_by_user_id(agents).execute_query()
    print("Team presence:")
    for e in presences:
        print(f"  {e.id}: {agent_status_summary(e)}")

    available = find_available_agent(client, agents)
    print(f"\nRouting: {'call to ' + available if available else 'no agents — queue'}")

    monitor_presence(client, agents, cycles=3)

    take_agent_offline(client, agents[0])
    print(f"\n{agents[0]} marked offline")


if __name__ == "__main__":
    main()
