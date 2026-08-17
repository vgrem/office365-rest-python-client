"""
Since for new tenants, apps using an ACS app-only access token is disabled by default,
you can change the behavior using the below script.

NOTE: ACS app-only authentication is deprecated — use Microsoft Entra app-only
(client certificate or client secret) instead.

https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, tenant

admin_client = ClientContext(admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
if admin_client.tenant.get_property("DisableCustomAppAuthentication"):
    print("Enabling ACS app-only access token auth on tenant...")
    admin_client.tenant.set_property("DisableCustomAppAuthentication", False).update().execute_query()
    print("Done")
else:
    print("ACS app-only access token auth has been already enabled on tenant")
