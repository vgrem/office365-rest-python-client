"""
List service principals in the tenant.

For delegated permissions see has_delegated_perms.py / list_delegated_perms.py.
For expiring secrets see password_expiry.py / certificate_expiry.py.

Requires delegated permission Application.Read.All.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

sps = client.service_principals.top(20).get().execute_query()
print(f"Service principals ({len(sps)}):")
for sp in sps:
    print(f"  {sp.display_name}  app_id={sp.app_id or '?'}")
