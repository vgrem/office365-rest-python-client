# Working with Users in SharePoint

Users in SharePoint are managed at the **site collection** level.
Every site has a list of users who have been granted access.
Users are represented by the `User` object, which contains
login name, email, display name, and group memberships.

---

## 👤 Get Current User

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

me = ctx.web.current_user.get().execute_query()
print(f"Hello, {me.title} ({me.login_name})")
```

| What | File | Notes |
|------|------|-------|
| **Get current user** | [`whoami.py`](./whoami.py) | Display name, login, email, groups |
| **Get my personal site** | [`get_my_site.py`](./get_my_site.py) | OneDrive for Business URL |

## 👥 List & Find Users

| What | File | Notes |
|------|------|-------|
| **List site users** | [`list_site_users.py`](./list_site_users.py) | All users with access to the site |
| **Search tenant users** | [`search_tenant_users.py`](./search_tenant_users.py) | Find users across the tenant |
| **Get users for a site** | [`get_for_site.py`](./get_for_site.py) | Users in a specific site collection |

## ➕ Manage Access

| What | File | Notes |
|------|------|-------|
| **Add user to web** | [`add_to_web.py`](./add_to_web.py) | Grant a user access to a site |

## 💾 OneDrive

| What | File | Notes |
|------|------|-------|
| **Get OneDrive quota** | [`get_onedrive_quota_max.py`](./get_onedrive_quota_max.py) | Storage limit for a user |

---

## Official docs

- [SharePoint users and groups REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
