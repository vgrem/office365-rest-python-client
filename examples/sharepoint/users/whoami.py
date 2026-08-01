"""
Retrieves the current user details.

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
whoami = ctx.web.current_user.get().execute_query()
print(whoami)
