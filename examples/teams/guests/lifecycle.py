"""
List guest users in the tenant.

Requires delegated permission ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

guests = client.users.filter("userType eq 'Guest'").get().execute_query()
print(f"Guest users: {len(guests)}\n")
for g in guests:
    user_type = "#EXT#" if "#EXT#" in (g.user_principal_name or "") else "native guest"
    print(f"  {g.display_name or '(no name)':30s}  {g.user_principal_name:40s}  {user_type}")
