"""
Clone a team — copy its channels, apps, tabs, settings, and/or members.

The clone operation is async; ``execute_query_and_wait`` polls until
the operation completes.

Requires delegated permission Team.Create or Group.ReadWrite.All.
"""

from office365.graph_client import GraphClient
from office365.teams.clonableteamparts import ClonableTeamParts
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    teams = client.teams.get().top(1).execute_query()
    if not teams:
        print("No source team found.")
        return

    source_team = teams[0]
    print(f"Source team: {source_team.display_name}")

    print("Cloning...")
    source_team.clone(
        f"{source_team.display_name}_cloned",
        f"{source_team.display_name}_cloned",
        ClonableTeamParts.channels,
        source_team.visibility,
    ).execute_query_and_wait()
    print("Clone completed.")


if __name__ == "__main__":
    main()
