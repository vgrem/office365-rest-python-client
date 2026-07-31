"""
Checks whether the tenant has an Intune license.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_admin_credentials, test_admin_site_url

admin_client = ClientContext(test_admin_site_url).with_username_and_password(test_admin_credentials)
result = admin_client.tenant.check_tenant_intune_license().execute_query()
print(f"Intune license: {'Yes' if result.value else 'No'}")
