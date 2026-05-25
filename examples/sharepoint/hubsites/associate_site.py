"""
Associate a site with an existing hub site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/hubsites
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
hub_sites = ctx.hub_sites.get().execute_query()
if hub_sites:
    target = hub_sites[0]
    assert target.id is not None
    site = ctx.site
    site.join_hub_site(target.id).execute_query()
    print(f"Site associated to hub: {target.title}")
