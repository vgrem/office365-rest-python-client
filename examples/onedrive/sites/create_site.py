"""
Create a modern SharePoint site — team or communication.

Requires delegated permission Sites.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/site-create
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Sites.ReadWrite.All")
)

name = input("Site name: ").strip()
alias = input("Site alias (e.g. project-alpha): ").strip() or name.lower().replace(" ", "-")
is_team = input("Team site (y/n)? ").strip().lower() == "y"

if is_team:
    site = client.sites.create_team(name=name, alias=alias).execute_query()
else:
    site = client.sites.create_comm(name=name, alias=alias).execute_query()

print(f"\nCreated: {site.display_name}")
print(f"  URL:    {site.web_url}")
print(f"  ID:     {site.id}")
