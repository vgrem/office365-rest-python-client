"""Demonstrates how to set a lookup field value on a list item

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.lookup_value import FieldLookupValue
from tests import test_client_id, test_password, test_tenant, test_username, test_team_site_url

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

list_tasks = ctx.web.lists.get_by_title("Company Tasks")
min_items = 2
items = list_tasks.items.get().top(min_items).execute_query()
if len(items) != min_items:
    sys.exit("Not enough items were found")

task_id = items[0].get_property("Id")
assert isinstance(task_id, int)
lookup_field_value = FieldLookupValue(task_id)
items[1].set_property("ParentTask", lookup_field_value).update().execute_query()

# me = ctx.web.current_user
# items[0].set_property("AssignedTo", FieldUserValue(me.id)).update().execute_query()
# items[0].set_property("AssignedTo", FieldUserValue.from_user(me)).update().execute_query()
print("Item has been updated")
