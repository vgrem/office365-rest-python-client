"""
Retrieves detailed properties for a specific SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_admin_site_url, test_client_id, test_password, test_team_site_url, test_tenant, test_username

client = ClientContext(test_admin_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
site_props = client.tenant.get_site_properties_by_url(test_team_site_url, True).execute_query()
print(site_props)
