"""
Retrieves detailed properties for a specific SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, team_site_url, tenant

client = ClientContext(admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
site_props = client.tenant.get_site_properties_by_url(team_site_url, True).execute_query()
print(site_props)
