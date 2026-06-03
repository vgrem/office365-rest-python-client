"""
List all tabs in a channel.

Tabs are app-specific views (e.g. Planner, OneNote, Website) pinned to a
channel for easy access.

Requires delegated permission ``TeamsTab.Read.All`` or
``TeamsTab.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/channel-list-tabs?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

tabs = teams[0].primary_channel.tabs.get().execute_query()
print(f"Tabs in '{teams[0].display_name}' / General:")
for tab in tabs:
    print(f"  {tab.display_name}")
