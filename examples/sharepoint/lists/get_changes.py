"""Demonstrates how to retrieve changes from a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.changes.query import ChangeQuery
from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

client = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
query = ChangeQuery(
    Item=True,
    Add=False,
    Update=False,
    SystemUpdate=False,
    DeleteObject=True,
    RoleAssignmentAdd=False,
    RoleAssignmentDelete=False,
)

list_title = "Documents"
result = client.web.lists.get_by_title(list_title).get_changes(query).execute_query()
for change in result:
    print(change)
