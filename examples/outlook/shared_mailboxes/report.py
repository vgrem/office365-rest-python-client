"""
Shared mailboxes: list, check quotas, and find without owners.

IT Pros need to track shared mailboxes for licensing and
governance.

Requires delegated permission ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

shared = client.users.filter("userType eq 'member' and userPrincipalName startsWith 'shared'").top(10).get().execute_query()
print(f"Shared mailboxes found: {len(shared)}")
for m in shared:
    print(f"  {m.display_name:30s}  {m.user_principal_name}  ({m.user_type or '?'})")
