"""
Archive lifecycle: find inactive teams, notify owners, and archive
(or later unarchive on demand).

Archived teams are read-only — no new messages, edits, or reactions.
They remain in the directory and can be restored at any time.
This is a common compliance workflow for reducing team sprawl.

The script operates in two modes:
  - **audit** (default): scan teams, report candidates for archiving.
  - **archive**: archive teams inactive for the given threshold.

Requires application permissions:
    Team.ReadBasic.All, TeamSettings.Read.All, TeamMember.Read.All
    Directory.Read.All               List all teams
    TeamSettings.ReadWrite.All       Archive / unarchive

https://learn.microsoft.com/en-us/graph/api/team-archive
https://learn.microsoft.com/en-us/graph/api/team-unarchive
"""

import sys
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

INACTIVITY_DAYS = 180  # Archive teams with no recent channel activity


def get_all_teams(client: GraphClient) -> list[dict]:
    """List every team in the tenant with basic metadata."""
    groups = (
        client.groups.get()
        .filter("resourceProvisioningOptions/Any(x:x eq 'Team')")
        .select(["id", "displayName", "description", "visibility"])
        .top(999)
        .execute_query()
    )
    teams = []
    for g in groups:
        team = client.teams[g.id].get().select(["isArchived", "createdDateTime"]).execute_query()
        teams.append(
            {
                "id": g.id,
                "name": g.display_name,
                "description": getattr(g, "description", ""),
                "visibility": getattr(g, "visibility", "?"),
                "is_archived": team.is_archived,
                "created": team.created_date_time,
            }
        )
    return teams


def last_activity_date(client: GraphClient, team_id: str) -> datetime | None:
    """Find the most recent message across any channel in the team.

    Returns None if the team has no messages at all.
    """
    latest = None
    channels = client.teams[team_id].channels.get().execute_query()
    for channel in channels:
        try:
            messages = client.teams[team_id].channels[channel.id].messages.top(1).get().execute_query()
            if messages:
                msg_date = getattr(messages[0], "created_date_time", None)
                if msg_date and (latest is None or msg_date > latest):
                    latest = msg_date
        except Exception:
            pass
    return latest


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "audit"

    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    cutoff = datetime.now(timezone.utc) - timedelta(days=INACTIVITY_DAYS)

    teams = get_all_teams(client)
    print(f"Found {len(teams)} teams in the tenant\n")

    candidates = []
    for t in teams:
        if t["is_archived"]:
            continue  # already archived
        last_msg = last_activity_date(client, t["id"])
        if last_msg is None or last_msg < cutoff:
            days = (datetime.now(timezone.utc) - last_msg).days if last_msg else float("inf")
            candidates.append({**t, "last_message": last_msg, "days_since": days})

    if not candidates:
        print("No inactive teams found (all have recent activity).")
        return

    print(f"Inactive teams ({INACTIVITY_DAYS}+ days): {len(candidates)}\n")
    print(f"{'Team':35s} {'Visibility':12s} {'Created':15s} {'Days inactive':>14s} {'Archived?'}")
    print("-" * 95)

    for c in sorted(candidates, key=lambda x: x["days_since"], reverse=True):
        last_str = f"{c['days_since']:.0f}d" if c["last_message"] else "∞ (no messages)"
        created_str = c["created"].strftime("%Y-%m-%d") if c["created"] else "?"
        print(
            f"{c['name'][:33]:35s} "
            f"{c['visibility']:12s} "
            f"{created_str:15s} "
            f"{last_str:>14s}  "
            f"{'→ will archive' if mode == 'archive' else 'candidate'}"
        )

    # — Archive mode —
    if mode == "archive":
        print(f"\nArchiving {len(candidates)} teams (set-readonly)...")
        archived_count = 0
        for c in candidates:
            try:
                # Set "shouldSetSpoSiteReadOnlyForMembers=False" to let
                # members still access SharePoint even though Teams is archived.
                client.teams[c["id"]].archive().execute_query()
                archived_count += 1
                print(f"  ✓ {c['name']}")
            except Exception as e:
                print(f"  ⚠ {c['name']}: {e}")
        print(f"\nDone. {archived_count} teams archived.")

    # — Provide a ready-to-paste unarchive snippet —
    print()
    print("To unarchive a specific team later:")
    print('  team = client.teams["<teamId>"].get().execute_query()')
    print('  team.unarchive().execute_query()')
    print('  print(f"Unarchived: {team.display_name}")')


if __name__ == "__main__":
    main()
