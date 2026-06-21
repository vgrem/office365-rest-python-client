"""
List all task lists with their task counts.

Requires delegated permission Tasks.Read.

https://learn.microsoft.com/en-us/graph/api/todotasklist-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

lists = client.me.todo.lists.get().execute_query()
for lst in lists:
    tasks = lst.tasks.get().execute_query()
    print(f"  {lst.display_name:40s}  ({len(tasks)} tasks)")
