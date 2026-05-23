"""Gets the people who are following the specified user.

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
user = ctx.site.root_web.site_users.get_by_email(test_user_principal_name)
result = ctx.people_manager.get_followers_for(user).execute_query()
for follower in result:
    print(follower.display_name)
