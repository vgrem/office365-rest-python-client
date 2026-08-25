# Microsoft To-Do

Manage Microsoft To-Do tasks and task lists via the Graph API —
CRUD, due-date lookahead, and cleanup of completed tasks.

---

## Tasks & Task Lists

### [Manage tasks](manage.py)

Microsoft To-Do — manage task lists, tasks, and checklist items.

```python
# Task lists
lists = client.me.todo.lists.get().execute_query()

# Create a task list
task_list = client.me.todo.lists.add("Demo").execute_query()

# Add a task with a due date and importance
task = task_list.tasks.add(
    title="Write docs",
    due_date_time=datetime.now(timezone.utc) + timedelta(days=3),
    importance=Importance.high,
).execute_query()

# Mark it completed
task.status = TaskStatus.completed
task.update().execute_query()
```


### [List task lists](list_task_lists.py)

List all task lists with their task counts.

```python
lists = client.me.todo.lists.get().execute_query()
for lst in lists:
    tasks = lst.tasks.get().execute_query()
    print(f"{lst.display_name}  ({len(tasks)} tasks)")
```


### [Tasks due soon](tasks_due_soon.py)

Find tasks due within a specified number of days.

```python
cutoff = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

for lst in client.me.todo.lists.get().execute_query():
    for task in lst.tasks.filter(f"dueDateTime/dateTime le '{cutoff}'").get().execute_query():
        print(f"[{lst.display_name}]  {task.title}  due={task.due_date_time}")
```


### [Clean up completed tasks](cleanup_completed.py)

Delete completed tasks older than a specified number of days.

```python
cutoff = datetime.now(timezone.utc) - timedelta(days=30)

for lst in client.me.todo.lists.get().execute_query():
    for task in lst.tasks.get().execute_query():
        if task.status == TaskStatus.completed and task.last_modified_date_time < cutoff:
            print(f"[{lst.display_name}]  {task.title}")
            task.delete_object().execute_query()
```


---
