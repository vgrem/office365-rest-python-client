"""
Microsoft To-Do — manage task lists, tasks, and checklist items.

To-Do is the personal task management service (different from
Planner, which is team-based). This example covers:
  - List task lists
  - Create a task with due date and details
  - Add checklist items
  - Mark a task as complete
  - Delete a task

Requires delegated permission ``Tasks.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/resources/todo-overview
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    # -- Step 1: list task lists --
    lists = client.me.todo.lists.get().execute_query()
    print(f"Task lists: {len(lists)}\n")

    for lst in lists:
        print(f"  {lst.display_name:40s}  id={lst.id[:15]}...")

    # -- Step 2: create or find a task list --
    target_list_name = "SDK Demo Tasks"
    task_list = next((lst for lst in lists if lst.display_name == target_list_name), None)

    if task_list is None:
        task_list = client.me.todo.lists.add(displayName=target_list_name).execute_query()
        print(f"Created task list: '{task_list.display_name}'")
    else:
        print(f"Using existing task list: '{task_list.display_name}'")

    # -- Step 3: create a task with due date --
    due = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    task = task_list.tasks.add(
        title="Review SDK documentation",
        dueDateTime={"dateTime": due, "timeZone": "UTC"},
        importance="high",
        body={"content": "Final review before release.", "contentType": "text"},
    ).execute_query()
    print(f"\nCreated task: '{task.title}'")
    print(f"  Due:       {task.due_date_time.strftime('%Y-%m-%d %H:%M') if task.due_date_time else '?'}")
    print(f"  Importance: {task.properties.get('importance', '?')}")

    # -- Step 4: add checklist items --
    checklist = [
        {"title": "Check all examples parse", "isChecked": False},
        {"title": "Verify Graph API permissions", "isChecked": False},
        {"title": "Test with client credentials", "isChecked": True},
    ]

    for item in checklist:
        cl_item = task.checklist_items.add(
            title=item["title"],
            isChecked=item["isChecked"],
        ).execute_query()
        print(f"  Checklist: {cl_item.title} {'✓' if cl_item.is_checked else '☐'}")

    # -- Step 5: list all tasks --
    all_tasks = task_list.tasks.get().execute_query()
    print(f"\nAll tasks in '{task_list.display_name}' ({len(all_tasks)}):")
    for t in all_tasks:
        title = t.title or "(untitled)"
        status = t.properties.get("status", "?")
        due_str = t.due_date_time.strftime("%Y-%m-%d") if t.due_date_time else ""
        print(f"  [{status:10s}] {title:40s}  {due_str}")

    # -- Step 6: complete the task --
    task.set_property("status", "completed")
    task.update().execute_query()
    print(f"\n✓ Task '{task.title}' marked as completed.")

    # -- Step 7: delete the task list (commented) --
    # task_list.delete_object().execute_query()
    # print(f"Deleted task list: '{task_list.display_name}'")


if __name__ == "__main__":
    main()
