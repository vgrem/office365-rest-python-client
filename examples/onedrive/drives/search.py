"""
Search the current user's drive for files matching a keyword.

Uses the drive search endpoint.

Requires delegated permission ``Files.Read``.

https://learn.microsoft.com/en-us/graph/api/driveitem-search
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

results = client.me.drive.search("Quarterly").execute_query()
print(f"Search results for 'Quarterly': {len(results)}")
for item in results:
    item_type = "📄" if item.is_file else "📁"
    print(f"  {item_type}  {item.name:40s}  {item.parent_reference.path or 'root'}")
