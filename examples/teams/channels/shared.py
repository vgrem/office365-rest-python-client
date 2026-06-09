"""
Create a shared channel, share it with another team, and manage
access.

Shared channels extend collaboration across teams — members of other
teams can be added directly without adding them as guests to the host
team.

This example:
  1. Creates a shared channel in Team A.
  2. Shares it with Team B.
  3. Adds a specific user from Team B as an allowed member.
  4. Checks whether a user has access.

Requires delegated permissions:
    Channel.Create                Create channels
    ChannelMember.ReadWrite.All   Manage channel members

https://learn.microsoft.com/en-us/graph/api/resources/channel?view=graph-rest-1.0#shared-channels
"""

import sys

from office365.graph_client import GraphClient
from office365.teams.members.aad_user_conversation import AadUserConversationMember
from tests import test_client_id, test_client_secret, test_tenant


def find_team_by_name(client: GraphClient, name_hint: str):
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


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    # — Step 1: resolve teams —
    host_id, host_name = find_team_by_name(client, "Marketing")
    guest_id, guest_name = find_team_by_name(client, "Engineering")

    if not host_id:
        sys.exit("Host team not found (name contains 'Marketing').")
    if not guest_id:
        sys.exit("Guest team not found (name contains 'Engineering').")

    print(f"Host team:  {host_name}")
    print(f"Guest team: {guest_name}\n")

    # — Step 2: create a shared channel in the host team —
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

    # — Step 3: share the channel with the guest team —
    # POST /teams/{host}/channels/{channel}/sharedWithTeams
    shared_info = client.teams[host_id].channels[channel.id].shared_with_teams
    shared_info.add(teamId=guest_id).execute_query()

    # Reload to confirm
    shared = client.teams[host_id].channels[channel.id].shared_with_teams.get().execute_query()
    print(f"Channel shared with: {', '.join(str(s.id) for s in shared)}")

    # — Step 4: add a user from the guest team as an allowed member —
    # The ConversationMemberCollection.add() helper uses a simple
    # ConversationMember, but shared channels need AadUserConversationMember
    # with the correct odata.type and user@odata.bind serialization.
    guest_user_email = "meganb@contoso.onmicrosoft.com"
    users = client.users.filter(f"mail eq '{guest_user_email}'").get().execute_query()
    if not users:
        sys.exit(f"User not found: {guest_user_email}")

    guest_user = users[0]
    print(f"User resolved: {guest_user.display_name}  (uid: {guest_user.id})")

    # Construct the member manually with the correct type binding
    member = AadUserConversationMember(client.context)
    member.set_property("userId", guest_user.id)
    member.roles.add("owner")
    client.teams[host_id].channels[channel.id].members.add_child(member)
    client.execute_query()
    print("Allowed member added (AadUserConversationMember).")

    # — Step 5: check whether the user has access —
    result = client.teams[host_id].channels[channel.id].does_user_have_access(user_id=guest_user.id).execute_query()
    has_access = result.value
    print(f"User has access to shared channel: {has_access}")


if __name__ == "__main__":
    main()
