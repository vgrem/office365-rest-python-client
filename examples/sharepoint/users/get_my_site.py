"""
Gets the personal site for a user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
my_site = ctx.web.current_user.get_personal_site().execute_query()
print(my_site.url)
