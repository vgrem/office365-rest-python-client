"""
Controls app access on a specific SharePoint site collection.

https://developer.microsoft.com/en-us/office/blogs/controlling-app-access-on-specific-sharepoint-site-collections/
https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_client_secret,
    test_team_site_url,
    test_tenant,
)

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
site = client.sites.get_by_url(test_team_site_url)
app = client.applications.get_by_app_id(test_client_id)
roles = ["read", "write"]

print(f"Granting {roles} permissions for application {app}")
site.permissions.add(roles, app).execute_query()
result = site.permissions.get().execute_query()
for perm in result:
    print(f"Current permissions: {perm.granted_to_identities}")
