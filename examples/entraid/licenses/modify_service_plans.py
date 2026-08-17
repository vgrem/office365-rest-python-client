"""
Manage service plan states: enable or disable specific plans within a license.

For example, disable Exchange Online in an E3 license while keeping SharePoint.
The Graph API requires reassigning the entire license with a disabledPlans list.

Requires delegated permission ``User.ReadWrite.All``, ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense
"""

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant, test_user_principal_name

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

# 1. Find target SKU by part number (e.g. "SPE_E3", "SPE_E5", "ENTERPRISEPACK")
sku_part = input("SKU part number (e.g. SPE_E5): ").strip()
skus = client.subscribed_skus.get().execute_query()
sku = next((s for s in skus if s.sku_part_number == sku_part), None)
if not sku:
    raise SystemExit(f"SKU '{sku_part}' not found in tenant.")

print(f"\nAvailable service plans in {sku.sku_part_number}:")
for p in sku.service_plans:
    print(f"  [{p.servicePlanName:45s}]  {p.servicePlanId}")

# 2. Choose which plans to disable
plan_name = input("\nService plan name to disable (e.g. EXCHANGE_S_ENTERPRISE): ").strip()
disabled = [p for p in sku.service_plans if p.servicePlanId == plan_name]
if not disabled:
    raise SystemExit(f"Service plan '{plan_name}' not found in SKU.")

# 3. Reassign the license with the plan disabled
user = client.users.get_by_principal_name(test_user_principal_name)
user.assign_license(
    add_licenses=[AssignedLicense(skuId=sku.sku_id, disabledPlans=[plan.servicePlanId for plan in disabled])],
    remove_licenses=[],
).execute_query()
print(f"\nLicense '{sku.sku_part_number}' updated for {test_user_principal_name}")
print(f"Disabled plan: {plan_name}")
