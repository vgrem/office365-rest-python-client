"""
Install a Teams app in a team by app catalog ID.

Lists available apps from the Teams app catalog first.

Requires delegated permission ``TeamsAppInstallation.ReadWriteForTeam.All``
or ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/team-post-installedapps?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

teams = client.me.joined_teams.get().execute_query()
if len(teams) == 0:
    sys.exit("No teams found")

apps = client.teams.app_catalog.get().execute_query()
if len(apps) == 0:
    sys.exit("No apps found in catalog")

team = teams[0]
catalog_app = apps[0]
app = team.installed_apps.add(catalog_app).execute_query()
print(f"App '{catalog_app.display_name}' installed in '{team.display_name}'")
