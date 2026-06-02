# Users

Manage users in SharePoint: who has access to a site, current user info,
tenant-wide search, and OneDrive details.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Read access** to the site | Required to list users. **Site Owner** to add users. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

### Current user

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Get current user | [`whoami.py`](./whoami.py) | Any authenticated user | [Users REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **2** | Get my personal site | [`get_my_site.py`](./get_my_site.py) | Any authenticated user | [Users REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

### List and search

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **3** | List site users | [`list_site_users.py`](./list_site_users.py) | Read access | [Users REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **4** | Search tenant users | [`search_tenant_users.py`](./search_tenant_users.py) | Read access | [Users REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **5** | Get users for a site | [`get_for_site.py`](./get_for_site.py) | Read access | [Users REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

### Manage and OneDrive

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **6** | Add user to web | [`add_to_web.py`](./add_to_web.py) | Site Owner | [Users REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **7** | Get OneDrive quota | [`get_onedrive_quota_max.py`](./get_onedrive_quota_max.py) | Read access | [Users REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Get current user
me = ctx.web.current_user.get().execute_query()
print(f"Hello, {me.title}  ({me.login_name})")

# List all site users
users = ctx.web.site_users.get().execute_query()
for u in users:
    print(f"  {u.title}  ({u.login_name})")
```

---

## API reference

- [SharePoint users and groups REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
