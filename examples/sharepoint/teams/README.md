# Teams (SharePoint)

List Microsoft Teams that the current user is a direct member of.
These examples use the **SharePoint REST API** (not the Microsoft Graph).

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **User context** (delegated auth) | Required to list teams the current user belongs to. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Get my joined teams | [`list_my.py`](./list_my.py) | User context (delegated) | [Team operations REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

import json
result = ctx.group_site_manager.get_current_user_joined_teams().execute_query()
data = json.loads(result.value)
for team in data["value"]:
    print(f"  {team['displayName']}  (ID: {team['id']})")
```

---

## API reference

- [SharePoint team operations REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations)
