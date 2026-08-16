"""
List all role definitions (permission levels) available on a site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

roles = ctx.web.role_definitions.get().execute_query()
for role in roles:
    print(f"  {role.name}  (ID: {role.id}, Order: {role.properties.get('Order')})")
