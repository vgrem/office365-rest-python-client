"""
Checks whether the tenant has an Intune license.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, tenant

admin_client = ClientContext(admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
result = admin_client.tenant.check_tenant_intune_license().execute_query()
print(f"Intune license: {'Yes' if result.value else 'No'}")
