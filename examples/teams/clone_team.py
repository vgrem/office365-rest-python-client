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

from office365.graph_client import GraphClient
from office365.teams.clonableteamparts import ClonableTeamParts
from office365.teams.team import Team
from tests import test_client_id, test_password, test_tenant, test_username


def poll_clone_completion(team: Team, max_wait_sec: int = 120) -> bool:
    """Poll the team's operations list waiting for a clone to succeed/fail."""
    for attempt in range(1, (max_wait_sec // 10) + 1):
        time.sleep(10)
        ops = team.operations.get().execute_query()
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
    teams = client.teams.get().top(1).execute_query()
    if len(teams) == 0:
        sys.exit("No source team found.")

    source_team = teams[0]
    print(f"Source team: {source_team.display_name}")

    print("Cloning (this may take 60+ seconds)...\n")
    target_team = source_team.clone(
        f"{source_team.display_name}_cloned",
        f"{source_team.display_name}_cloned",
        ClonableTeamParts.channels,
        source_team.visibility,
    ).execute_query_and_wait()


if __name__ == "__main__":
    main()
