# Event Receivers

Event receivers attach custom logic (remote endpoints or code) to list
events — item added, updated, deleted, and more.

| What | File | Notes |
|------|------|-------|
| **Add receiver** | [`add_receiver.py`](./add_receiver.py) | Attach a remote event receiver to a list |
| **List receivers** | [`list_receivers.py`](./list_receivers.py) | Enumerate event receivers on a list |
| **Remove receiver** | [`remove_receiver.py`](./remove_receiver.py) | Delete an event receiver by ID |

---

## Event types

| Value | Event |
|-------|-------|
| 1 | ItemAdding |
| 2 | **ItemAdded** |
| 3 | ItemUpdating |
| 4 | ItemUpdated |
| 5 | ItemDeleting |
| 6 | ItemDeleted |
| 7–22 | Check-in/out, attachment, move, version events |

## Official docs

- [Event receiver REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver)
