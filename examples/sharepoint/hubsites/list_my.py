"""
Gets information about all hub sites that the current user can access.
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
hub_sites = ctx.hub_sites.get().execute_query()
for hub_site in hub_sites:
    print(hub_site)
