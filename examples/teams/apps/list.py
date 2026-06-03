"""
List all apps installed in a team.

Requires delegated permission ``TeamsAppInstallation.Read.All`` or
``TeamsAppInstallation.ReadWriteForTeam.All``.

https://learn.microsoft.com/en-us/graph/api/team-list-installedapps?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

team = teams[0]
apps = team.installed_apps.get().execute_query()
print(f"Apps installed in '{team.display_name}':")
for app in apps:
    print(f"  {app.id}")
