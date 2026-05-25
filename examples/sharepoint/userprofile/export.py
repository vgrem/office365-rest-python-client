"""Exports user profile data for users in a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
users = ctx.site.root_web.site_users.filter("IsHiddenInUI eq false").get().top(10).execute_query()

exported_data = {}
for user in users:
    assert user.login_name is not None
    exported_data[user.login_name] = ctx.people_manager.get_properties_for(user.login_name)
ctx.execute_batch()
print(exported_data)
