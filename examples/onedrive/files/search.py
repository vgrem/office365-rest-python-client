"""
Search files and folders in your OneDrive by keyword.

Requires delegated permission ``Files.Read``.

https://learn.microsoft.com/en-us/graph/api/driveitem-search
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

results = client.me.drive.search("report").execute_query()
print(f"Found {len(results)} items matching 'report':")
for item in results:
    print(f"  {item.name:40s}  {'📄' if item.is_file else '📁'}  {item.size or 0:,} bytes")
