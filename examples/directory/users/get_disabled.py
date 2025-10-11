"""
Retrieve and display disabled Azure AD users using Microsoft Graph API.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

disabled_users = (
    client.users.select(["id", "userPrincipalName", "displayName", "accountEnabled"])
    .get()
    .filter("accountEnabled eq false")
    .execute_query()
)

for user in disabled_users:
    print(f"- {user.user_principal_name} ({user.display_name})")
