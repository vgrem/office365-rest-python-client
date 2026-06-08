"""
Assign a license to a user and switch between service plans.

Shows how to add, remove, and switch licenses using SKU IDs.

Requires delegated permission ``User.ReadWrite.All``,
``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense
"""

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_client_secret,
    test_tenant,
    test_user_principal_name,
)

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# Find the first available license SKU
skus = client.subscribed_skus.get().execute_query()
if len(skus) == 0:
    exit("No license SKUs found")

sku = skus[0]
print(f"Using SKU: {sku.sku_part_number}  (id: {sku.sku_id})")

# Assign license to a user
user = client.users.get_by_principal_name(test_user_principal_name)

try:
    result = user.assign_license(
        add_licenses=[AssignedLicense(sku_id=sku.sku_id)],
        remove_licenses=[],
    ).execute_query()
    print(f"License assigned to {user.display_name}")
except Exception as e:
    print(f"License assignment skipped (may already be licensed): {e}")
