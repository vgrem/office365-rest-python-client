"""
Create a tag and assign members in a team.

Requires delegated permission TeamworkTag.ReadWrite.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

TAG_NAME = "Designer"
TAG_DESCRIPTION = "Design team members for @mentions"
MEMBER_EMAILS = ["meganb@contoso.onmicrosoft.com", "diegos@contoso.onmicrosoft.com"]


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    teams = client.teams.get_all().select(["id", "displayName"]).execute_query()
    team = next((t for t in teams if "Marketing" in (t.display_name or "")), None)
    if team is None:
        print("No matching team found.")
        return

    member_ids = []
    for email in MEMBER_EMAILS:
        users = client.users.filter(f"mail eq '{email}'").get().execute_query()
        if users:
            member_ids.append(users[0].id)

    if member_ids:
        tag = team.tags.add(
            displayName=TAG_NAME,
            description=TAG_DESCRIPTION,
            members=[{"userId": uid} for uid in member_ids],
        ).execute_query()
        print(f"Tag created: {tag.display_name}  ({len(member_ids)} members)")


if __name__ == "__main__":
    main()
