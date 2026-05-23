"""
Add a custom action that injects JavaScript (ScriptLink) on every page.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action
"""

from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.usercustomactions.action import UserCustomAction
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
action = UserCustomAction(ctx)
action.set_property("Title", "Custom script")
action.set_property("Location", "ScriptLink")
action.set_property("ScriptBlock", "console.log('Loaded from custom action');")
action.set_property("Sequence", 100)
qry = CreateEntityQuery(ctx.web.user_custom_actions, action)
ctx.add_query(qry)
ctx.execute_query()
print(f"Script link added: {action.properties.get('Id')}")
