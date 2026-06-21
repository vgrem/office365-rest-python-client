"""
Report on apps installed across all Microsoft Teams.

For detecting shadow IT and tracking app adoption.

Required delegated permissions:
    Team.ReadBasic.All              List all teams
    TeamsAppInstallation.Read.All   Read installed apps per team

https://learn.microsoft.com/en-us/graph/api/resources/teamsappinstallation
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

for team in client.teams.get_all().execute_query():
    try:
        apps = team.installed_apps.expand(["teamsAppDefinition"]).get().execute_query()
    except Exception:
        continue
    for app in apps:
        definition = app.teams_app_definition
        name = definition.properties.get("displayName", "Unknown")
        version = definition.properties.get("version", "")
        state = definition.properties.get("publishingState", "")
        print(f"  [{team.display_name}]  {name}  {version}  {state}")
