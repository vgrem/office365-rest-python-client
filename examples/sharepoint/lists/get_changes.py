"""Demonstrates how to retrieve changes from a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.changes.query import ChangeQuery
from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

client = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
query = ChangeQuery(
    item=True,
    add=False,
    update=False,
    system_update=False,
    delete_object=True,
    role_assignment_add=False,
    role_assignment_delete=False,
)

list_title = "Documents"
result = client.web.lists.get_by_title(list_title).get_changes(query).execute_query()
for change in result:
    print(change.properties)
