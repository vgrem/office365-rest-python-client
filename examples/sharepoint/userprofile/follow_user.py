"""Follow or unfollow a user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username, test_user_principal_name

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
user = ctx.web.ensure_user(test_user_principal_name).execute_query()
assert user.login_name is not None

is_following = ctx.people_manager.am_i_following(user.login_name).execute_query()
if is_following.value:
    ctx.people_manager.stop_following(user.login_name).execute_query()
    print(f"Unfollowed: {user.login_name}")
else:
    ctx.people_manager.follow(user.login_name).execute_query()
    print(f"Following: {user.login_name}")
