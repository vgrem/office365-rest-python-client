"""Demonstrates how to create multiple list items in batch mode

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from typing import List

from office365.runtime.client_object import ClientObject
from office365.runtime.client_result import ClientResult
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from tests import create_unique_name, test_client_id, test_password, test_team_site_url, test_tenant, test_username


def print_progress(return_types: List[ClientObject | ClientResult]) -> None:
    items_count = len([t for t in return_types if isinstance(t, ListItem)])
    print("{0} list items has been created".format(items_count))


ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
tasks_list = ctx.web.lists.get_by_title("Company Tasks")

num_of_items = 512
item_props = {"Title": create_unique_name("Task")}
task_items = [tasks_list.add_item(item_props) for idx in range(num_of_items)]
ctx.execute_batch(success_callback=print_progress)
print("{0} task items created".format(len(task_items)))
