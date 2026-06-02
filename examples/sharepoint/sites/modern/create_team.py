"""
Creates a modern team site (Microsoft 365 group-connected).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
site = ctx.create_team_site(alias="TeamSite", title="Team Site").execute_query()
print(f"Team site created: {site.url}")
