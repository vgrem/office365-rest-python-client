"""
Demonstrates how to retain the history for list items.
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

ctx = ClientContext(team_site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)
items = ctx.web.lists.get_by_title("Site Pages").items.expand(["Versions"]).get().top(10).execute_query()

for item in items:
    for version in item.versions:
        print(version)
