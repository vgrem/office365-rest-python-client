# Microsoft To-Do

Examples for working with Microsoft To-Do tasks via the Graph API.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Tasks.Read` (delegated) | Read tasks and task lists | [Tasks permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#tasks-permissions) |
| `Tasks.ReadWrite` (delegated) | Create, update, delete tasks | |

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| CRUD — task lists, tasks, checklist items | [`manage.py`](./manage.py) | `Tasks.ReadWrite` |
| List all task lists with counts | [`list_task_lists.py`](./list_task_lists.py) | `Tasks.Read` |
| Find tasks due soon | [`tasks_due_soon.py`](./tasks_due_soon.py) | `Tasks.Read` |
| Clean up completed tasks | [`cleanup_completed.py`](./cleanup_completed.py) | `Tasks.ReadWrite` |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_username_and_password(
    "client_id", "user@contoso.com", "password"
)

lists = client.me.todo.lists.get().execute_query()
for lst in lists:
    print(lst.display_name)
```

---

## Official docs

- [To-Do task API overview](https://learn.microsoft.com/en-us/graph/api/resources/todotask)
- [Task list API](https://learn.microsoft.com/en-us/graph/api/resources/todotasklist)
