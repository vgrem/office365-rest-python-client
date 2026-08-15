"""
Retrieves all SharePoint sites from a tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url
from tests.settings import cert_path, cert_thumbprint, client_id, tenant

admin_client = ClientContext(test_admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
tenant = Tenant(admin_client)
result = tenant.get_site_properties_from_sharepoint_by_filters("").execute_query()
i = 0
for siteProps in result:
    print(f"({i} of {len(result)}) {siteProps.url}")
    i += 1
