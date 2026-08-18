"""
List sensitivity labels available in the tenant.

To actually apply a sensitivity label to a SharePoint file, see
``examples/sharepoint/sites/assign_sensitivity_label.py``.

Requires delegated permission ``InformationProtectionPolicy.Read.All``
and Global Administrator or Compliance Administrator role.

https://learn.microsoft.com/en-us/graph/api/informationprotectionpolicy-list-labels
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant


def main():
    parser = argparse.ArgumentParser(description="List sensitivity labels")
    parser.add_argument("--detail", action="store_true", help="Show priority and description")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant, scopes=["https://graph.microsoft.com/InformationProtectionPolicy.Read.All"])
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Compliance Administrator")
    )

    labels = client.security.data_security_and_governance.sensitivity_labels.get().execute_query()
    print(f"Sensitivity labels ({len(labels)}):\n")

    for label in labels:
        if args.detail:
            print(f"  {label.display_name:30s}  priority={label.priority}  {label.description}")
        else:
            print(f"  {label.display_name:30s}  id: {label.id}")


if __name__ == "__main__":
    main()
