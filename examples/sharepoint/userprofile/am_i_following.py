"""Check if the current user is following a specific user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_user_principal_name, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
user = ctx.web.ensure_user(test_user_principal_name).execute_query()
assert user.login_name is not None
result = ctx.people_manager.am_i_following(user.login_name).execute_query()
print(f"Following {user.login_name}: {result.value}")
