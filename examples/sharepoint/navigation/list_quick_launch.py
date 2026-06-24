"""
Print the Quick Launch navigation of a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant

ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
nav = ctx.web.navigation.quick_launch.get().execute_query()
for item in nav:
    print(f"{item.title}  ({item.url})")
