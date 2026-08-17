"""
Prints all tenant settings.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from pprint import pprint

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, tenant

admin_client = ClientContext(admin_site_url).with_client_certificate(
    tenant,
    client_id=client_id,
    thumbprint=cert_thumbprint,
    cert_path=cert_path,
)
tenant_details = Tenant(admin_client).get().execute_query()
pprint(tenant_details.properties)
