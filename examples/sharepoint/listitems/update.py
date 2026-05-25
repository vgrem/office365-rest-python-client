"""Demonstrates how to update a list item

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import sys
from random import randint

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

list_tasks = ctx.web.lists.get_by_title("Tasks")
items = list_tasks.items.get().top(1).execute_query()
if len(items) == 0:
    sys.exit("No items found")

item_to_update = items[0]
task_prefix = str(randint(0, 10000))
# tax_field_value = TaxonomyFieldValue("Sweden", "f9a6dae9-633c-474b-b35e-b235cf2b9e73")
# item_to_update.set_property("Country", tax_field_value).update().execute_query()
item_to_update.set_property("Title", f"Task {task_prefix}").update().execute_query()
print("Item has been updated")
