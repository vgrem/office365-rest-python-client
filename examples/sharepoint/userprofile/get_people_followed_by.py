"""Gets the people who the specified user is following.

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
me = ctx.web.current_user
assert me.login_name is not None
followed = ctx.people_manager.get_people_followed_by(me.login_name).execute_query()
for person in followed:
    print(f"{person.display_name}  ({person.email})")
