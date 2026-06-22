"""
Find teams with no channels or no messages — cleanup candidates.

Teams with no channels are essentially empty. Teams with channels
but no messages may be abandoned provisioning attempts.

Requires application permission Team.ReadBasic.All,
Channel.ReadBasic.All, ChannelMessage.Read.All.

https://learn.microsoft.com/en-us/graph/api/channel-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

print(f"Checking {len(client.teams.get_all().execute_query())} teams...\n")
for team in client.teams.get_all().execute_query():
    channels = team.channels.get().execute_query()
    if not channels:
        print(f"  EMPTY  {team.display_name}  (no channels)")
        continue
    has_msgs = False
    for ch in channels:
        msgs = ch.messages.top(1).get().execute_query()
        if msgs:
            has_msgs = True
            break
    if not has_msgs:
        print(f"  STALE  {team.display_name}  (channels but no messages)")
