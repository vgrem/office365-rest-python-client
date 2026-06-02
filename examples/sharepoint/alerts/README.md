# Alerts

Create, list, and remove alerts. Alerts send email notifications when items
are added, changed, or deleted in a list or library.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Read access** to the list | Required to create alerts on it. Alerts are user-specific. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List alerts for current user | [`list_alerts.py`](./list_alerts.py) | User context | [Alerts REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **2** | Add an alert on a list | [`add_alert.py`](./add_alert.py) | Read access on list | [Alerts REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **3** | Remove an alert | [`remove_alert.py`](./remove_alert.py) | User context | [Alerts REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

alerts = ctx.web.current_user.alerts.get().execute_query()
for a in alerts:
    print(f"  {a.title}  ({a.id})")
```

---

## API reference

- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
