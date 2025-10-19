"""
Retrieves sites in tenant
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_admin_site_url, test_client_id, test_password, test_tenant, test_username

admin_client = ClientContext(test_admin_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
result = admin_client.tenant.get_site_properties_from_sharepoint_by_filters("").execute_query()
i = 0
for siteProps in result:
    print(f"({i} of {len(result)}) {siteProps.url}")
    i += 1
