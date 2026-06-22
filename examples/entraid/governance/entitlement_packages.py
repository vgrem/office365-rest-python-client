"""
List entitlement management access packages and their assignments.

Requires delegated permission ``EntitlementManagement.Read.All``.

https://learn.microsoft.com/en-us/graph/api/entitlementmanagement-list-accesspackages
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

response = client.execute_request_get(
    "/identityGovernance/entitlementManagement/accessPackages?$select=id,displayName,description&$top=20"
)
for p in response.json().get("value", []):
    assignments = client.execute_request_get(
        f"/identityGovernance/entitlementManagement/accessPackages/{p['id']}/accessPackageAssignmentApprovals"
    )
    count = len(assignments.json().get("value", []))
    print(f"  {p['displayName']:40s}  assignments={count}")
