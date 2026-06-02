"""
Delete a SharePoint Embedded container type (beta API).

Requires:
  - ``FileStorageContainerType.Manage.All`` delegated permission granted via
    admin consent. See ``examples/onedrive/grant_permission.py`` to grant it.
  - ``SharePoint Embedded Administrator`` or ``Global Administrator`` role.

https://learn.microsoft.com/en-us/graph/api/filestoragecontainertype-delete
"""

import sys

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

if not has_role(client, "Global Administrator", "SharePoint Embedded Administrator"):
    print("❌ Need Global Administrator or SharePoint Embedded Administrator.")
    sys.exit(1)

# List existing container types with their IDs
types = client.storage.file_storage.container_types.get().execute_query()
if not types:
    print("No container types found.")
    sys.exit(0)

print("Container types:")
for t in types:
    print(f"  {t.id}  {t.name}  ({t.billing_classification})")

container_id = input("\nContainer type ID to delete: ").strip()
if not container_id:
    print("No ID entered. Exiting.")
    sys.exit(0)

ct = client.storage.file_storage.container_types[container_id].get().execute_query()
ct.delete_object().execute_query()
print(f"Deleted: {ct.name} (ID: {ct.id})")
