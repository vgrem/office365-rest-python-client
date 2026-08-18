"""
Report Microsoft 365 Copilot license adoption across the tenant.

Shows which Copilot-related SKUs are subscribed and how many licenses are
consumed vs enabled.

Requires delegated permission ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/subscribedsku-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

COPILOT_KEYWORDS = ("COPILOT", "M365COPILOT", "CHAT")


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    skus = client.subscribed_skus.get().execute_query()
    print("Copilot-related SKUs:\n")
    found = False
    for sku in skus:
        name = (sku.sku_part_number or "").upper()
        if any(keyword in name for keyword in COPILOT_KEYWORDS):
            found = True
            enabled = sku.prepaid_units.enabled if sku.prepaid_units else 0
            print(f"  {sku.sku_part_number:35s} consumed: {sku.consumed_units or 0} / enabled: {enabled}")
    if not found:
        print("  (no Copilot SKUs found)")


if __name__ == "__main__":
    main()
