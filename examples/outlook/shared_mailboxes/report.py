"""
Shared mailboxes: list shared mailboxes in the tenant.

Requires delegated permission User.Read.All.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

shared = (
    client.users.filter("userType eq 'Member' and startswith(userPrincipalName, 'shared')").top(10).get().execute_query()
)
print(f"Shared mailboxes: {len(shared)}")
for m in shared:
    print(f"  {m.user_principal_name}")
