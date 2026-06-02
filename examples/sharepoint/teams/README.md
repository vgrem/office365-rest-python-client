# Teams (SharePoint)

List Microsoft Teams and channels that the current user has access to.
These examples use the **SharePoint REST API**.

> **Note:** The SharePoint REST API provides limited team operations.
> For full Teams management (create channels, send messages, install apps,
> manage members), use the
> [Microsoft Graph Teams API](https://learn.microsoft.com/en-us/graph/api/resources/teams-api-overview?view=graph-rest-1.0).

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **User context** (delegated auth) | Required to list teams the current user belongs to. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Get my joined teams | [`list_my.py`](./list_my.py) | User context (delegated) | [Team operations REST](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations) |
| **2** | Get recent and joined teams | [`get_recent_and_joined_teams.py`](./get_recent_and_joined_teams.py) | User context (delegated) | [Team operations REST](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations) |
| **3** | Get team channels | [`get_team_channels.py`](./get_team_channels.py) | User context (delegated) | [Team operations REST](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations) |
| **4** | Ensure team for group | [`ensure_team_for_group.py`](./ensure_team_for_group.py) | User context (delegated) | [Team operations REST](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations) |

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
- [Microsoft Graph Teams API](https://learn.microsoft.com/en-us/graph/api/resources/teams-api-overview?view=graph-rest-1.0) (full coverage)
