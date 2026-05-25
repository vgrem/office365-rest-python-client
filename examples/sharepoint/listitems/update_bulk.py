"""Demonstrates how to update multiple list items in batch mode

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from random import randint

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_tenant, test_username, test_team_site_url

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

# 1. Load existing list items
list_tasks = ctx.web.lists.get_by_title("Tasks")
items = list_tasks.items.get().top(10).execute_query()

# 2. Update list items via batch mode
for _, item in enumerate(items):
    task_prefix = str(randint(0, 10000))
    item.set_property("Title", "Task 123 {task_prefix}".format(task_prefix=task_prefix)).update()
ctx.execute_batch()
print("{0} items has been updated".format(len(items)))
