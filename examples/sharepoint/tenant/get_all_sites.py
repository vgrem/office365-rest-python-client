"""
Retrieves all SharePoint sites from a tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_password, test_tenant, test_username

admin_client = ClientContext(test_admin_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)

tenant = Tenant(admin_client)
result = tenant.get_site_properties_from_sharepoint_by_filters("").execute_query()
i = 0
for siteProps in result:
    print(f"({i} of {len(result)}) {siteProps.url}")
    i += 1
