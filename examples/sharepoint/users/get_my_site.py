"""
Gets the personal site for a user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
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
print(my_site.url)
