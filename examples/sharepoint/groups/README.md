# Groups

Manage SharePoint site groups — create, list, find, set owner, and add or
remove members.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** role | Required to create, delete, and manage group membership. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Operation | File | Required role |
|---|---|---|
| List all site groups | [`list_groups.py`](./list_groups.py) | Read access |
| Get a group by name | [`get_by_name.py`](./get_by_name.py) | Read access |
| Create a group | [`add_remove.py`](./add_remove.py) | Site Owner |
| Add a user to a group | [`add_user_to_group.py`](./add_user_to_group.py) | Site Owner |
| Remove a user from a group | [`remove_user_from_group.py`](./remove_user_from_group.py) | Site Owner |
| Set the group owner | [`set_owner.py`](./set_owner.py) | Site Owner |
| Expand the Members group to principals | [`expand_to_principals.py`](./expand_to_principals.py) | Read access |

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

# Create a group
group = ctx.web.site_groups.add("Project Contributors").execute_query()
```

---

## API reference

- [SharePoint group REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group)
