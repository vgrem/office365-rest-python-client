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
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

create_trial = False

if create_trial:
    # Create a trial container type (free, expires in 30 days)
    ct = client.storage.file_storage.container_types.add(
        "My Trial App",
        test_client_id,
        billing_classification="trial",
    ).execute_query()
    print(f"Created: {ct.name} (ID: {ct.id}, expires: {ct.expiration_datetime})")


# List all container types
types = client.storage.file_storage.container_types.get().execute_query()
print("\nRegistered container types:")
for t in types:
    print(f"  {t.name}  ({t.billing_classification})")
