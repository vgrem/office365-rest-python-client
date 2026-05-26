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

from office365.directory.permissions.guard import has_delegated_permission, has_role
from office365.directory.permissions.resource_name import ResourceName
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from tests import test_admin_principal_name, test_client_id, test_tenant

scope = input("Permission scope: ")

client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)

if not has_role(client, "Global Administrator", "Privileged Role Administrator"):
    print("❌ Need Global Administrator or Privileged Role Administrator role to grant permissions.")
    exit(1)

if has_delegated_permission(client, scope, test_client_id):
    print(f"✅ Permission '{scope}' is already granted.")
else:
    print(f"❌ Permission '{scope}' is not granted.")
    answer = input("Grant it now via admin consent? (y/N): ")
    if answer.lower() == "y":
        resource = client.service_principals.get_by_name(ResourceName.Graph)
        try:
            resource.grant_delegated_permissions(test_client_id, None, scope).execute_query()
            print(f"✅ Permission '{scope}' granted.")
        except ClientRequestException as e:
            if "409" in str(e):
                print(f"✅ Permission '{scope}' was already granted.")
            else:
                raise
    else:
        print("Skipped.")
