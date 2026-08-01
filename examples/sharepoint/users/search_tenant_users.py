"""
Searches for tenant users by search term.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, tenant

ctx = ClientContext(admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
result = ctx.search_user("SharePoint Service Administrator").execute_query()
print(result.value)
