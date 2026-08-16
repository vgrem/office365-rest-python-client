"""
Gets the personal site (OneDrive) for the current user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)
my_site = ctx.web.current_user.get_personal_site().execute_query()
print(f"Personal site: {my_site.url}")
