"""Demonstrates how to retrieve lookup field values from a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
list_tasks = ctx.web.lists.get_by_title("Company Tasks")
items = (
    list_tasks.items.get()
    .select(
        [
            "*",
            "AssignedTo/Id",
            "AssignedTo/Title",
            "Predecessors/Id",
            "Predecessors/Title",
        ]
    )
    .expand(["AssignedTo", "Predecessors"])
    .top(10)
    .execute_query()
)
for item in items:
    assigned_to = item.properties.get("AssignedTo", {}).get("Id", None)
    predecessors_ids = [v.get("Id", None) for k, v in item.properties.get("Predecessors", {}).items()]
    print("AssignedTo Id: {0}, Predecessors Ids: {1}".format(assigned_to, predecessors_ids))
