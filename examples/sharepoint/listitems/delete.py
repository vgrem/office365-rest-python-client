"""Demonstrates how to delete a list item from a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_tenant, test_username, test_team_site_url

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
tasks_list = ctx.web.lists.get_by_title("Company Tasks")
items = tasks_list.items.get().execute_query()

print("Option 1: remove a list item (with an option to restore from a recycle bin)...")
items[0].recycle().execute_query()

print("Option 2: Permanently remove a list item...")
items[1].delete_object().execute_query()
