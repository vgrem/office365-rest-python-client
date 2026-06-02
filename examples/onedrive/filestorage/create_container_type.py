"""
Create and list SharePoint Embedded container types (beta API).

Requires:
  - ``FileStorageContainerType.Manage.All`` delegated permission granted via
    admin consent.  See ``examples/onedrive/grant_permission.py`` to grant it.
  - ``SharePoint Embedded Administrator`` or ``Global Administrator`` role.

The owning app ID must belong to the same tenant.

https://learn.microsoft.com/en-us/graph/api/filestorage-post-containertypes?view=graph-rest-beta
"""

import sys

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
# client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)
if not has_role(client, "Global Administrator", "SharePoint Embedded Administrator"):
    print("❌ Need Global Administrator or SharePoint Embedded Administrator.")
    sys.exit(1)


# Create a trial container type (free, expires in 30 days).
# Only one trial is allowed per tenant.
try:
    ct = client.storage.file_storage.container_types.add(
        "My Trial App",
        test_client_id,
        billing_classification="trial",
    ).execute_query()
    print(f"Created: {ct.name} (ID: {ct.id}, expires: {ct.expiration_datetime})")
except ClientRequestException as e:
    if e.code == "speInvalidOperation":
        # Trial limit reached — find the existing one
        types = client.storage.file_storage.container_types.get().execute_query()
        ct = next(
            (t for t in types if t.owning_app_id == test_client_id and t.billing_classification == "trial"),
            None,
        )
        if ct is None:
            print("No existing container type found for this app.")
            raise
        print(f"Using existing: {ct.name} (ID: {ct.id})")
    else:
        raise


#registrations = client.storage.file_storage.container_type_registrations.get().execute_query()

# List all container types
types = client.storage.file_storage.container_types.get().execute_query()
print("\nRegistered container types:")
for t in types:
    print(f"  {t.id}  {t.name}  ({t.billing_classification})")

# Allow the user to delete a container type
container_id = input("\nContainer type ID to delete (or leave empty to skip): ").strip()
if container_id:
    ct_to_delete = client.storage.file_storage.container_types[container_id].get().execute_query()
    ct_to_delete.delete_object().execute_query()
    print(f"Deleted: {ct_to_delete.name} (ID: {ct_to_delete.id})")
