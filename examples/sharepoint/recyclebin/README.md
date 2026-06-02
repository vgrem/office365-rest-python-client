# Recycle Bin

List, restore, and manage deleted items in the site recycle bin.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Read access** to the site | Required to view recycle bin. **Site Owner** to restore items. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List items in recycle bin | [`list_recycle_bin.py`](./list_recycle_bin.py) | Read access | [Recycle bin REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **2** | Restore an item from recycle bin | [`restore_from_recycle_bin.py`](./restore_from_recycle_bin.py) | Site Owner | [Recycle bin REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

items = ctx.web.recycle_bin.get().execute_query()
for item in items:
    print(f"  {item.title}  (deleted: {item.deleted_date})")
```

---

## API reference

- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
