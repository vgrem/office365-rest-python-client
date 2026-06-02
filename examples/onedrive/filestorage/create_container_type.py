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
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# Get or create a trial container type
types = client.storage.file_storage.container_types.get().execute_query()
ct = next(
    (t for t in types if t.owning_app_id == test_client_id and t.billing_classification == "trial"),
    None,
)
if ct is None:
    ct = client.storage.file_storage.container_types.add(
        "My Trial App", test_client_id, billing_classification="trial",
    ).execute_query()
    print(f"Created: {ct.name} (ID: {ct.id})")
else:
    print(f"Using existing: {ct.name} (ID: {ct.id})")

# List all container types
print("\nContainer types:")
for t in client.storage.file_storage.container_types.get().execute_query():
    print(f"  {t.name}  ({t.billing_classification})")
