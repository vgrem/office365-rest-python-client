"""
Creates a modern team site (Microsoft 365 group-connected).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)
site = ctx.create_team_site(alias="TeamSite", title="Team Site").execute_query()
print(f"Team site created: {site.url}")
