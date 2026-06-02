# Event Receivers

> **⚠️ Legacy — prefer SharePoint Webhooks for modern sites.**
> Remote Event Receivers (RERs) are deprecated by Microsoft. They work on
> **classic** lists and pages but are not supported on modern lists.
> [Webhooks overview](https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks)

Attach custom logic (remote endpoints) to list events — item added, updated,
deleted, and more.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** role on the target list | Required to add and remove event receivers. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

Event receivers can be attached at the **web** or **list** scope. When an
event fires, SharePoint sends an HTTP request to the configured endpoint.

| Event type | Value | Fires when |
|---|---|---|
| ItemAdding | 1 | Before an item is added |
| **ItemAdded** | **2** | After an item is added |
| ItemUpdating | 3 | Before an item is updated |
| ItemUpdated | 4 | After an item is updated |
| ItemDeleting | 5 | Before an item is deleted |
| ItemDeleted | 6 | After an item is deleted |
| 7–22 | — | Attachment, move, version, check-in/out events |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List — enumerate event receivers on a list | [`list_receivers.py`](./list_receivers.py) | Read access | [List](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver) |
| **2** | Add — attach a remote event receiver to a list | [`add_receiver.py`](./add_receiver.py) | Site Owner on target list | [Create](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver) |
| **3** | Remove — delete an event receiver by ID | [`remove_receiver.py`](./remove_receiver.py) | Site Owner on target list | [Delete](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# List event receivers on a list
target_list = ctx.web.lists.get_by_title("Documents")
receivers = target_list.event_receivers.get().execute_query()
for r in receivers:
    print(f"  {r.properties.get('ReceiverName', '')}  (ID: {r.properties.get('ReceiverId', '')})")
```

---

## API reference

- [Event receiver REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver)
- [SharePoint webhooks overview](https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks) (modern replacement)