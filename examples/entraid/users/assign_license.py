"""
Assign a license to a user.

Demonstrates how to assign a Microsoft 365 license (SKU) to a user.
First retrieves available SKUs, then assigns one by SKU ID.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense

https://learn.microsoft.com/en-us/graph/api/resources/user

Requires delegated permission ``User.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

# find the first available license SKU (e.g. "Microsoft 365 E5")
skus = client.subscribed_skus.get().execute_query()
if not skus:
    print("No license SKUs found.")
    exit(1)

sku = skus[0]
print(f"Assigning license: {sku.sku_part_number} ({sku.sku_id})")

user = client.users.get_by_principal_name("user@contoso.onmicrosoft.com")
user.assign_license([sku.sku_id]).execute_query()
print(f"License assigned to {user.user_principal_name}")
