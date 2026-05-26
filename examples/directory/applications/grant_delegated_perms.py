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
from office365.directory.permissions.guard import has_delegated_permission
from tests import test_client_id, test_client_secret, test_tenant

scope = input("Permission scope: ") or "FileStorageContainerType.Manage.All"

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

if has_delegated_permission(client, scope, test_client_id):
    print(f"Permission '{scope}' is already granted.")
else:
    print(f"Permission '{scope}' is not granted.")
    answer = input("Grant it now via admin consent? (y/N): ")
    if answer.lower() == "y":
        admin = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id)
        resource = admin.service_principals.get_by_name("Microsoft Graph")
        resource.grant_delegated_permissions(test_client_id, None, scope).execute_query()
        print(f"Permission '{scope}' granted.")
    else:
        print("Skipped.")
