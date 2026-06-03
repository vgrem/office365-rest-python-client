"""
Update team settings (messaging, member, guest).

Requires delegated permission ``TeamSettings.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-update?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
team.set_property("memberSettings", {"allowCreateUpdateChannels": True})
team.set_property("messagingSettings", {"allowUserEditMessages": True, "allowUserDeleteMessages": True})
team.set_property("guestSettings", {"allowCreateUpdateChannels": False})
team.update().execute_query()
print(f"Settings updated for '{team.display_name}'")
