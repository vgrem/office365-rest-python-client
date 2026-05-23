"""
Remove a custom action by ID.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.usercustomactions.action import UserCustomAction
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
actions = ctx.web.user_custom_actions.get().execute_query()
if actions:
    target = actions[0]
    assert target.properties.get("Id") is not None
    action = UserCustomAction(ctx)
    action.set_property("Id", target.properties["Id"])
    action.delete_object().execute_query()
    print(f"Removed action ID: {target.properties['Id']}")
