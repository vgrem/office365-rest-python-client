"""
Search messages with custom search and filters.

Uses the Microsoft Search API with keyword query, pagination,
and filters.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/search-concept-messages
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

result = client.search.query_messages("Meet for lunch?", page_from=1, size=10).execute_query()
for item in result.value:
    for hit in item.hitsContainers[0].hits:
        subject = hit.resource.get_property("subject")
        sender = hit.resource.get_property("from")
        print(f"  {subject}  (from: {sender})")
