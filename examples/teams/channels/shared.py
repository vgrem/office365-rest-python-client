"""
Create a shared channel, share it with another team, and manage
access.

Shared channels extend collaboration across teams — members of other
teams can be added directly without adding them as guests to the host
team.

Requires delegated permissions:
    Channel.Create                Create channels
    ChannelMember.ReadWrite.All   Manage channel members

https://learn.microsoft.com/en-us/graph/api/resources/channel?view=graph-rest-1.0#shared-channels
"""

import sys

from office365.graph_client import GraphClient
from office365.teams.members.aad_user_conversation import AadUserConversationMember
from tests.settings import client_id, client_secret, tenant


def find_team_by_name(client: GraphClient, name_hint: str):
    teams = client.teams.get_all().select(["id", "displayName"]).execute_query()
    for t in teams:
        if name_hint.lower() in (t.display_name or "").lower():
            return t.id, t.display_name
    return None, None


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    host_id, host_name = find_team_by_name(client, "Marketing")
    guest_id, guest_name = find_team_by_name(client, "Engineering")

    if not host_id:
        sys.exit("Host team not found (name contains 'Marketing').")
    if not guest_id:
        sys.exit("Guest team not found (name contains 'Engineering').")

    print(f"Host team:  {host_name}")
    print(f"Guest team: {guest_name}\n")

    channel = (
        client.teams[host_id]
        .channels.add(
            displayName="Cross-team Project Alpha",
            description="Shared channel — Engineering collaboration",
            membershipType="shared",
        )
        .execute_query()
    )
    print(f"Shared channel created: {channel.display_name}  (id: {channel.id})")

    shared_info = client.teams[host_id].channels[channel.id].shared_with_teams
    shared_info.add(teamId=guest_id).execute_query()

    shared = client.teams[host_id].channels[channel.id].shared_with_teams.get().execute_query()
    print(f"Channel shared with: {', '.join(str(s.id) for s in shared)}")

    guest_user_email = "meganb@contoso.onmicrosoft.com"
    users = client.users.filter(f"mail eq '{guest_user_email}'").get().execute_query()
    if not users:
        sys.exit(f"User not found: {guest_user_email}")

    guest_user = users[0]
    print(f"User resolved: {guest_user.display_name}  (uid: {guest_user.id})")

    member = AadUserConversationMember(client.context)
    member.set_property("userId", guest_user.id)
    member.roles.add("owner")
    client.teams[host_id].channels[channel.id].members.add_child(member)
    client.execute_query()
    print("Allowed member added.")

    result = client.teams[host_id].channels[channel.id].does_user_have_access(user_id=guest_user.id).execute_query()
    print(f"User has access to shared channel: {result.value}")


if __name__ == "__main__":
    main()
