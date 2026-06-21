"""
Grant an app (service principal) access to a specific SharePoint site.

The app must already have the ``Sites.Selected`` application permission
granted via admin consent. This API then grants that specific app
access to a target site.

Requires delegated permission ``Sites.ReadWrite.All`` and
SharePoint Administrator or Global Administrator role.

https://learn.microsoft.com/en-us/graph/api/site-post-permissions
"""

from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_team_site_url, test_tenant

privileged_client = (
    GraphClient(tenant=test_tenant)
    .with_token_interactive(test_client_id, test_admin_principal_name)
    .require_role("Global Administrator", "Privileged Role Administrator")
)

# Get the service principal for this app
sp = privileged_client.service_principals.get_by_app_id(test_client_id).get().execute_query()

# Get the target site
site = privileged_client.sites.get_by_url(test_team_site_url).get().execute_query()

# Grant write access using the service principal entity directly
permission = site.permissions.add(
    roles=["write"],
    identity=sp,
).execute_query()
print(f"Granted {permission.roles} to app {test_client_id} on site {test_team_site_url}")
