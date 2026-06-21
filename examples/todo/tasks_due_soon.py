"""
Find tasks due within a specified number of days.

Requires delegated permission Tasks.Read.

https://learn.microsoft.com/en-us/graph/api/todotask-list
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

days = int(input("Show tasks due within (days): ") or "7")
cutoff = datetime.now(timezone.utc) + timedelta(days=days)

for lst in client.me.todo.lists.get().execute_query():
    for task in lst.tasks.filter(f"dueDateTime/dateTime le '{cutoff.isoformat()}Z'").get().execute_query():
        print(f"  [{lst.display_name}]  {task.title:50s}  due={task.due_date_time}")
