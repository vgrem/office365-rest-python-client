"""
Create a tag and assign members in a team.

Tags let users @mention a group (e.g. "Designers", "On-call") without
typing every name. This example creates a tag and populates it with
team members resolved by email.

Requires delegated permission ``TeamworkTag.ReadWrite`` or
``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/teamworktag-post
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

TAG_NAME = "Designer"
TAG_DESCRIPTION = "Design team members for @mentions"
MEMBER_EMAILS = ["meganb@contoso.onmicrosoft.com", "diegos@contoso.onmicrosoft.com"]


def get_team_by_name(client: GraphClient, name: str):
    """Find the first team whose display name contains *name*."""
    groups = (
        client.groups.get()
        .filter("resourceProvisioningOptions/Any(x:x eq 'Team')")
        .select(["id", "displayName"])
        .top(999)
        .execute_query()
    )
    for g in groups:
        if name.lower() in g.display_name.lower():
            return client.teams[g.id].get().execute_query()
    return None


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    team = get_team_by_name(client, "Marketing")
    if team is None:
        sys.exit("No matching team found.")

    print(f"Team: {team.display_name}\n")

    # Step 1 — resolve member user IDs
    member_ids = []
    for email in MEMBER_EMAILS:
        users = client.users.filter(f"mail eq '{email}'").get().execute_query()
        if len(users) == 0:
            print(f"  ⚠ User not found: {email}")
            continue
        member_ids.append(users[0].id)
        print(f"  ✓ Resolved {email} → {users[0].id}")

    if not member_ids:
        sys.exit("No valid members to assign.")

    print()

    # Step 2 — create the tag with members
    tag = team.tags.add(
        displayName=TAG_NAME,
        description=TAG_DESCRIPTION,
        members=[{"userId": uid} for uid in member_ids],
    ).execute_query()

    print(f"Tag created: {tag.display_name}")
    print(f"  Members: {len(member_ids)}")


if __name__ == "__main__":
    main()
