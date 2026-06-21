"""
Delete completed tasks older than a specified number of days.

Requires delegated permission Tasks.ReadWrite.

https://learn.microsoft.com/en-us/graph/api/todotask-delete
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from office365.intune.print.taskstatus import TaskStatus
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

days = int(input("Delete completed tasks older than (days): ") or "30")
cutoff = datetime.now(timezone.utc) - timedelta(days=days)

deleted = 0
for lst in client.me.todo.lists.get().execute_query():
    for task in lst.tasks.get().execute_query():
        if (
            task.status == TaskStatus.completed
            and task.last_modified_date_time
            and task.last_modified_date_time < cutoff
        ):
            task.delete_object().execute_query()
            deleted += 1

print(f"Deleted {deleted} completed tasks older than {days} days")
