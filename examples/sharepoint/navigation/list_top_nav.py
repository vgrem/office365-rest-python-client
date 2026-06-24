"""
Print the top navigation bar of a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, site_url, tenant, cert_thumbprint, cert_path

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
nav = ctx.web.navigation.top_navigation_bar.get().execute_query()
for item in nav:
    print(f"{item.title}  ({item.url})")
