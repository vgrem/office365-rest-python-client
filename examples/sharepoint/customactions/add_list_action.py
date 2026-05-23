"""
Add a custom action (toolbar button) to a SharePoint list.

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
target_list = ctx.web.lists.get_by_title("Documents")

action = UserCustomAction(ctx)
action.set_property("Title", "Open in App")
action.set_property("Location", "EditControlBlock")
action.set_property("Sequence", 100)
action.set_property("Url", "https://example.com/open?id={ItemId}")
qry = CreateEntityQuery(target_list.user_custom_actions, action)
ctx.add_query(qry)
ctx.execute_query()
print(f"List action added: {action.properties.get('Id')}")
