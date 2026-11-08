"""The service plans inside a SKU, and turning one off for a user.

Graph has no "disable a plan" call: the whole licence is reassigned carrying the ids of the
plans to disable, so the operation is a read-modify-write of ``assignedLicenses``. Without
``--plan-off`` the script only reads.

    python plans.py --sku SPE_E5
    python plans.py --sku SPE_E5 --user ada@contoso.com --plan-off EXCHANGE_S_ENTERPRISE

Requires delegated ``User.ReadWrite.All`` and ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense
"""

import argparse

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.graph_client import GraphClient
from office365.runtime.types.collections import StringCollection
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description="List a SKU's service plans, or disable one for a user")
    parser.add_argument("--sku", required=True, help="SKU part number, e.g. SPE_E5")
    parser.add_argument("--user", help="User principal name to apply the change to")
    parser.add_argument("--plan-off", action="append", default=[], help="Service plan name to disable")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    sku = client.subscribed_skus.find_by_part_number(args.sku, required=True).execute_query()
    plans = {plan.servicePlanName: plan for plan in sku.service_plans}
    for name, plan in plans.items():
        print(f"{name} {plan.servicePlanId} {plan.provisioningStatus}")
    if not args.plan_off:
        return
    if not args.user:
        raise SystemExit("--plan-off needs --user")
    unknown = [name for name in args.plan_off if name not in plans]
    if unknown:
        raise SystemExit(f"{sku.sku_part_number} has no plan named {', '.join(unknown)}")
    disabled = StringCollection([plans[name].servicePlanId or "" for name in args.plan_off])
    client.users.get_by_principal_name(args.user).assign_license(
        add_licenses=[AssignedLicense(skuId=sku.sku_id, disabledPlans=disabled)], remove_licenses=[]
    ).execute_query()
    print(f"disabled {', '.join(args.plan_off)} on {sku.sku_part_number} for {args.user}")


if __name__ == "__main__":
    main()
