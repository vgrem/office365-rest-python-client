"""
List documents that are trending, recently used, or shared with the user.

The insights API surfaces relevant documents from OneDrive/SharePoint:
  - Trending: documents gaining popularity around the user
  - Used: documents the user has viewed or modified
  - Shared: documents shared with the user

Requires delegated permission Sites.Read.All.

https://learn.microsoft.com/en-us/graph/api/resources/insights
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

print("=== Trending ===")
for item in client.me.insights.trending.get().execute_query():
    print(f"  {item.resource_reference}")

print("\n=== Recently used ===")
for item in client.me.insights.used.get().execute_query():
    print(f"  {item.resource_reference}")

print("\n=== Shared with me ===")
for item in client.me.insights.shared.get().execute_query():
    print(f"  {item.resource_reference}")
