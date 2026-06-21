"""
Microsoft To-Do — manage task lists, tasks, and checklist items.

Requires delegated permission Tasks.ReadWrite.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from office365.outlook.mail.importance import Importance
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    task_list = client.me.todo.lists.get_or_add("SDK Demo Tasks").execute_query()
    print(f"Task list: {task_list.display_name}\n")

    due = datetime.now(timezone.utc) + timedelta(days=3)
    task = task_list.tasks.add(
        title="Review SDK documentation",
        due_date_time=due,
        importance=Importance.high,
        body="Final review before release.",
    ).execute_query()
    print(f"Task: {task.title}  Due: {task.due_date_time}  Importance: {task.importance}")

    for item in [
        {"title": "Check all examples parse", "isChecked": False},
        {"title": "Verify Graph API permissions", "isChecked": False},
        {"title": "Test with client credentials", "isChecked": True},
    ]:
        cl = task.checklist_items.add(displayName=item["title"], isChecked=item["isChecked"]).execute_query()
        print(f"  {cl.display_name}: {'checked' if cl.is_checked else 'unchecked'}")

    all_tasks = task_list.tasks.get().execute_query()
    print(f"\nAll tasks ({len(all_tasks)}):")
    for t in all_tasks:
        print(f"  {t.status}  {t.title}")

    task.set_property("status", "completed").update().execute_query()
    print(f"\n{task.title} completed")


if __name__ == "__main__":
    main()
