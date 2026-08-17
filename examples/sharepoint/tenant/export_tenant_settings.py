"""
Exports tenant settings to a CSV file in the Style Library.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, tenant

admin_client = ClientContext(admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
result = admin_client.tenant.export_to_csv(view_xml="<View/>", list_name="Style Library").execute_query()
print("Sites details have been exported into {0}{1}".format(admin_site_url, result.value))
