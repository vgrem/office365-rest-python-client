"""Demonstrates how to create a list item in a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_user_principal_name, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
tasks_list = ctx.web.lists.get_by_title("Company Tasks")
manager = ctx.web.site_users.get_by_principal_name(test_user_principal_name)

item = tasks_list.add_item(
    {
        "Title": "New Task",
        # "Manager": FieldUserValue.from_user(manager),
    }
).execute_query()
print("Item has been created")
