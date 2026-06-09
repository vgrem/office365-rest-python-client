"""
Clone a team — copy its channels, apps, tabs, settings, and/or members.

Uses the ``ClonableTeamParts`` enum as a bitset so you can select
exactly what to copy.  The clone operation is async; this example
polls the source team's ``operations`` collection until it completes.

Typical provisioning pattern: bootstrap a new project from a template
team that already has the right channel structure and app setup.

Requires delegated permission ``Team.Create`` or ``Group.ReadWrite.All``.

Note: the SDK's ``team.clone()`` helper is a stub that doesn't pass
the required body parameters yet.  This example uses the underlying
``ServiceOperationQuery`` directly to send the proper payload.

https://learn.microsoft.com/en-us/graph/api/team-clone
"""

import sys
import time
from typing import Optional

from office365.graph_client import GraphClient
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.teams.clonableteamparts import ClonableTeamParts
from tests import create_unique_name, test_client_id, test_password, test_tenant, test_username

# Which parts to copy (combine with | for any subset)
CLONE_PARTS = [ClonableTeamParts.apps, ClonableTeamParts.tabs, ClonableTeamParts.settings, ClonableTeamParts.channels]


def find_source_team(client: GraphClient, name_hint: str) -> tuple[Optional[str], Optional[str]]:
    """Return (team_id, display_name) for the first team matching *name_hint*."""
    groups = (
        client.groups.get()
        .filter("resourceProvisioningOptions/Any(x:x eq 'Team')")
        .select(["id", "displayName"])
        .top(999)
        .execute_query()
    )
    for g in groups:
        if name_hint.lower() in g.display_name.lower():
            return g.id, g.display_name
    return None, None


def poll_clone_completion(client: GraphClient, team_id: str, max_wait_sec: int = 120) -> bool:
    """Poll the team's operations list waiting for a clone to succeed/fail."""
    for attempt in range(1, (max_wait_sec // 10) + 1):
        time.sleep(10)
        ops = client.teams[team_id].operations.get().execute_query()
        for op in ops:
            print(f"    [{attempt * 10}s] Operation status: {op.status}")
            if op.status == "succeeded":
                return True
            elif op.status == "failed":
                err = op.properties.get("error", {})
                print(f"    Error: {err.get('message', 'unknown')}")
                return False
    return False


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    # — Step 1: pick a source team —
    source_id, source_name = find_source_team(client, "Marketing")
    if source_id is None:
        sys.exit("No matching source team found.")

    print(f"Source team: {source_name}")

    # — Step 2: build the parts string (comma-separated, lowercase) —
    parts_names = [p.name for p in CLONE_PARTS]
    parts_str = ",".join(parts_names)
    print(f"  Cloning: {', '.join(parts_names)}")

    # — Step 3: construct the clone payload as a dict —
    new_name = create_unique_name(f"{source_name}-Clone")
    nickname = new_name.lower().replace(" ", "").replace("_", "")[:64] or "clonedteam"

    payload = {
        "displayName": new_name,
        "mailNickname": nickname,
        "visibility": "private",
        "parts": parts_str,
    }

    print(f"Cloning → '{new_name}' (this may take 60+ seconds)...\n")

    # The team.clone() helper doesn't pass body params yet, so we
    # use ServiceOperationQuery directly with the payload dict.
    team = client.teams[source_id]
    qry = ServiceOperationQuery(team, "clone", None, payload)
    client.context.add_query(qry)
    client.execute_query()

    # — Step 4: poll for completion via the source team's operations —
    succeeded = poll_clone_completion(client, source_id)

    if succeeded:
        print(f"\n✅ Clone succeeded — '{new_name}' is ready.")
        # The cloned team ID can be found in the targetResourceLocation
        # of the "succeeded" operation if needed.
    else:
        print(f"\n❌ Clone failed or timed out.")


if __name__ == "__main__":
    main()
