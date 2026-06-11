"""
Teams presence and telephony status monitor — practical real-world example.

A call center / helpdesk scenario: monitor agent availability across a team,
detect state changes, bulk-query presence, and respond programmatically.

Covers:
  - Getting a single user's presence
  - Getting presence for multiple users at once (bulk)
  - Setting and clearing preferred presence
  - Setting a status message with expiry
  - Polling for state changes
  - Mapping presence states to business rules

Required permissions:
  - Presence.Read (delegated)        — read own presence
  - Presence.Read.All (application)  — read any user's presence
  - Presence.ReadWrite (delegated)   — set own presence + status message

See https://learn.microsoft.com/en-us/graph/api/resources/presence
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from time import sleep
from typing import Dict, List, Optional

from office365.graph_client import GraphClient


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SUPPORTED_AGENTS = [
    "alice@company.com",
    "bob@company.com",
    "carol@company.com",
]

POLL_INTERVAL_SECONDS = 30
BUSY_ACTIVITIES = {"InACall", "InAConferenceCall", "InAMeeting", "Presenting"}


# ---------------------------------------------------------------------------
# Business logic helpers
# ---------------------------------------------------------------------------

def is_available(presence) -> bool:
    """Determine if a user is considered 'available' for routing."""
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
    """Human-readable summary of an agent's current state."""
    availability = presence.get_property("availability") or "Unknown"
    activity = presence.get_property("activity") or "Unknown"
    return f"availability={availability}, activity={activity}"


# ---------------------------------------------------------------------------
# Core operations
# ---------------------------------------------------------------------------

def get_presence_for_user(client: GraphClient, user_id: str):
    """Get presence for a single user by ID or UPN."""
    return client.communications.presences[user_id].get().execute_query()


def get_presences_for_team(client: GraphClient, user_ids: List[str]):
    """Get presence for multiple users in a single API call (bulk)."""
    return client.communications.get_presences_by_user_id(user_ids).execute_query()


def take_agent_offline(client: GraphClient, user_id: str):
    """Mark an agent as DoNotDisturb + set an end-of-day status message."""
    expires = datetime.now(timezone.utc) + timedelta(hours=9)

    client.communications.presences[user_id].set_user_preferred_presence(
        availability="DoNotDisturb",
        activity="OffWork",
        expiration_duration="PT9H",
    ).execute_query()

    client.communications.presences[user_id].set_status_message(
        message="Shift ended — back tomorrow",
        expiry=expires,
    ).execute_query()


def set_agent_available(client: GraphClient, user_id: str):
    """Return an agent to available state after break."""
    client.communications.presences[user_id].set_user_preferred_presence(
        availability="Available",
        activity="Available",
        expiration_duration="PT8H",
    ).execute_query()


# ---------------------------------------------------------------------------
# Scenario 1: snapshot — check current team status
# ---------------------------------------------------------------------------

def snapshot_team_status(client: GraphClient, agents: List[str]):
    """One-shot display of every agent's current presence."""
    print("=== Team presence snapshot ===")
    presences = get_presences_for_team(client, agents)
    for entry in presences:
        print(f"  {entry.id:40s} {agent_status_summary(entry)}")
    print()


# ---------------------------------------------------------------------------
# Scenario 2: monitor — poll for state changes
# ---------------------------------------------------------------------------

def monitor_team_status(client: GraphClient, agents: List[str], cycles: int = 5):
    """Poll presence for a team and report state changes."""
    print(f"=== Monitoring {len(agents)} agents (poll every {POLL_INTERVAL_SECONDS}s) ===")

    previous: Dict[str, str] = {}

    for cycle in range(1, cycles + 1):
        print(f"\n--- Cycle {cycle}/{cycles} [{datetime.now(timezone.utc).isoformat()}] ---")
        presences = get_presences_for_team(client, agents)

        for entry in presences:
            user_id = entry.id
            state = agent_status_summary(entry)
            old_state = previous.get(user_id)

            if old_state is None:
                print(f"  INIT  {user_id:35s} {state}")
            elif state != old_state:
                print(f"  >>> {user_id:35s} {old_state} -> {state}")
                if is_available(entry) and not is_available.__doc__:
                    print(f"       Agent {user_id} is now available for routing")
            else:
                print(f"  .     {user_id:35s} {state}")

            previous[user_id] = state

        if cycle < cycles:
            sleep(POLL_INTERVAL_SECONDS)

    print()


# ---------------------------------------------------------------------------
# Scenario 3: round-robin availability check for routing
# ---------------------------------------------------------------------------

def find_available_agent(client: GraphClient, agents: List[str]) -> Optional[str]:
    """Return the first available agent (useful for automatic call routing)."""
    presences = get_presences_for_team(client, agents)
    for entry in presences:
        if is_available(entry):
            return entry.id
    return None


# ---------------------------------------------------------------------------
# Scenario 4: set status message on shift start
# ---------------------------------------------------------------------------

def start_shift(client: GraphClient, user_id: str, agent_name: str):
    """Begin shift: set available presence with a status message."""
    expires = datetime.now(timezone.utc) + timedelta(hours=9)
    client.communications.presences[user_id].set_user_preferred_presence(
        availability="Available",
        activity="Available",
        expiration_duration="PT9H",
    ).execute_query()

    client.communications.presences[user_id].set_status_message(
        message=f"{agent_name} is online — ready to take calls",
        expiry=expires,
    ).execute_query()


# ---------------------------------------------------------------------------
# Main — run all scenarios
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Connect (choose one auth method)
    #
    # Option A: certificate
    # client = GraphClient(tenant).with_client_certificate(client_id, thumbprint, key)
    #
    # Option B: client secret
    # client = GraphClient(tenant).with_client_secret(client_id, client_secret)
    #
    # Option C: device code (interactive, works with MFA)
    client = GraphClient(tenant).with_device_flow(client_id="your_client_id")
    # (For brevity replace with real credentials above)

    # ------------------------------------------------------------------
    # Scenario 1 — read-only snapshot
    # ------------------------------------------------------------------
    snapshot_team_status(client, SUPPORTED_AGENTS)

    # ------------------------------------------------------------------
    # Scenario 2 — find someone to route a call to
    # ------------------------------------------------------------------
    available = find_available_agent(client, SUPPORTED_AGENTS)
    if available:
        print(f"Routing call to: {available}")
    else:
        print("No agents available — queuing call")

    # ------------------------------------------------------------------
    # Scenario 3 — monitor for state changes (run 3 cycles)
    # ------------------------------------------------------------------
    monitor_team_status(client, SUPPORTED_AGENTS, cycles=3)

    # ------------------------------------------------------------------
    # Scenario 4 — mark agent as off (end of shift)
    # ------------------------------------------------------------------
    take_agent_offline(client, SUPPORTED_AGENTS[0])
    print(f"Agent {SUPPORTED_AGENTS[0]} marked as offline")
