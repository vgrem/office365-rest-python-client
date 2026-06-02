"""
Create and list SharePoint Embedded container types (beta API).

Requires:
  - ``FileStorageContainerType.Manage.All`` delegated permission granted via
    admin consent.  See ``examples/onedrive/grant_permission.py`` to grant it.
  - ``SharePoint Embedded Administrator`` or ``Global Administrator`` role.

The owning app ID must belong to the same tenant.

https://learn.microsoft.com/en-us/graph/api/filestorage-post-containertypes?view=graph-rest-beta
"""

from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)

# Get or create a trial container type
types = client.storage.file_storage.container_types.get().execute_query()
if len(types) == 0:
    ct = client.storage.file_storage.container_types.add(
        "My Trial App",
        test_client_id,
        billing_classification="trial",
    ).execute_query()
    print(f"Created: {ct.name} (ID: {ct.id})")
else:
    ct = types[0]
    print(f"Using existing: {ct.name} (ID: {ct.id})")
