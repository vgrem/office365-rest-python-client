# Microsoft To-Do

Examples for working with Microsoft To-Do tasks via the Graph API.

The To Do API operates on the signed-in user's mailbox, so the examples use
delegated auth (`with_username_and_password`) with the credentials in
`tests/settings.py`.

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

## `manage.py` — CLI

Run from the repo root:

```bash
python examples/todo/manage.py lists                                    # list task lists with counts
python examples/todo/manage.py tasks --list "Demo"                      # show tasks in a list
python examples/todo/manage.py add-list --name "Demo"                   # create a task list
python examples/todo/manage.py add-task --list "Demo" --title "Write docs" [--due-in 3] [--importance high] [--body "..."]
python examples/todo/manage.py checklist --list "Demo" --task <task_id> [--add "Subtasks"]
python examples/todo/manage.py complete --list "Demo" --task <task_id>
python examples/todo/manage.py delete-list --name "Demo"
```

## Other scripts

```bash
python examples/todo/list_task_lists.py [--name "Demo"]                 # task lists with counts
python examples/todo/tasks_due_soon.py [--days 7]                       # tasks due within N days
python examples/todo/cleanup_completed.py [--days 30] [--dry-run]       # delete old completed tasks
```

---

## Official docs

- [To-Do task API overview](https://learn.microsoft.com/en-us/graph/api/resources/todotask)
- [Task list API](https://learn.microsoft.com/en-us/graph/api/resources/todotasklist)
