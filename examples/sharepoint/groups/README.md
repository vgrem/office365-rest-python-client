# Groups

Manage SharePoint site groups — create, list, find, add and remove members.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** role | Required to create, delete, and manage group membership. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List — enumerate all site groups | [`list_groups.py`](./list_groups.py) | Read access | [Group collection](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group) |
| **2** | Get by name — retrieve a group by its name | [`get_by_name.py`](./get_by_name.py) | Read access | [Get by name](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group) |
| **3** | Add — create a new site group | [`add_remove.py`](./add_remove.py) | Site Owner | [Create](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group) |
| **4** | Add user — add a member to a group | [`add_user_to_group.py`](./add_user_to_group.py) | Site Owner | [Add user](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group) |
| **5** | Remove user — remove a member from a group | [`remove_user_from_group.py`](./remove_user_from_group.py) | Site Owner | [Remove user](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group) |
| **6** | Expand — list group members with details | [`expand_to_principals.py`](./expand_to_principals.py) | Read access | [Expand to principals](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# List all site groups
groups = ctx.web.site_groups.get().execute_query()
for g in groups:
    print(f"  {g.title}  (ID: {g.id})")
```

---

## API reference

- [SharePoint group REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group)