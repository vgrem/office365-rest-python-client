"""
How to grant delegated (OAuth2) permissions for an app using Microsoft Graph.

This script checks whether a delegated permission is already granted, and
if not, prompts an admin to grant it via interactive consent.

Usage:
    python -m examples.directory.applications.grant_delegated_perms

Requires an administrative role that can grant delegated permissions
(e.g. Global Administrator). See Azure Portal > App registrations > API permissions.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph
"""

from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

client = (
    GraphClient(tenant=test_tenant)
    .with_token_interactive(test_client_id, test_admin_principal_name)
    .require_role("Global Administrator", "Privileged Role Administrator")
)

scope = input("Permission scope: ")

if client.has_delegated_permission(scope, test_client_id):
    print(f"Permission '{scope}' is already granted.")
else:
    print(f"Permission '{scope}' is not granted.")
    client.grant_delegated_permissions(test_client_id, scope).execute_query()
    print(f"Permission '{scope}' granted.")
