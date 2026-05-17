"""Demonstrates how to retrieve lookup field values from a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
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
