"""
Microsoft To-Do — manage task lists, tasks, and checklist items.

Requires delegated permission Tasks.ReadWrite.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    lists = client.me.todo.lists.get().execute_query()
    print(f"Task lists: {len(lists)}\n")

    for lst in lists:
        print(f"  {lst.display_name}")

    target = next((t for t in lists if t.display_name == "SDK Demo Tasks"), None)
    if target is None:
        target = client.me.todo.lists.add(displayName="SDK Demo Tasks").execute_query()
        print(f"Created: {target.display_name}")
    else:
        print(f"Using: {target.display_name}")

    due = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    task = target.tasks.add(
        title="Review SDK documentation",
        dueDateTime={"dateTime": due, "timeZone": "UTC"},
        importance="high",
        body={"content": "Final review before release.", "contentType": "text"},
    ).execute_query()
    print(f"\nTask: {task.title}")
    print(f"  Due: {task.due_date_time}")
    print(f"  Importance: {task.properties.get('importance', '?')}")

    for item in [
        {"title": "Check all examples parse", "isChecked": False},
        {"title": "Verify Graph API permissions", "isChecked": False},
        {"title": "Test with client credentials", "isChecked": True},
    ]:
        cl = task.checklist_items.add(title=item["title"], isChecked=item["isChecked"]).execute_query()
        print(f"  {cl.title}: {'checked' if cl.is_checked else 'unchecked'}")

    all_tasks = target.tasks.get().execute_query()
    print(f"\nAll tasks ({len(all_tasks)}):")
    for t in all_tasks:
        print(f"  {t.properties.get('status', '?'):10s}  {t.title}")

    task.set_property("status", "completed")
    task.update().execute_query()
    print(f"\n{task.title} completed")


if __name__ == "__main__":
    main()
