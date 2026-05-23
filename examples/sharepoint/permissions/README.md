# Working with Permissions in SharePoint

Permissions in SharePoint are managed through **role assignments** —
a user or group is assigned a **role definition** (like Full Control,
Edit, Read) on a **securable object** (site, list, folder, or file).

---

## 🔐 Get Permissions

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Get permissions for a site
roles = ctx.web.role_assignments.get().execute_query()
for role in roles:
    print(f"{role.member.title}: {role.role_definition_bindings}")
```

| What | File | Notes |
|------|------|-------|
| **Get permissions for a site** | [`get_for_site.py`](./get_for_site.py) | Role assignments on the web |
| **Get permissions for a list** | [`get_for_list.py`](./get_for_list.py) | Role assignments on a list |
| **Get permissions for a file** | [`get_for_file.py`](./get_for_file.py) | Role assignments on a file |

## ✏️ Grant & Revoke

| What | File | Notes |
|------|------|-------|
| **Grant permissions** | [`grant_to_web.py`](./grant_to_web.py) | Add a user/group to a role |
| **Revoke permissions** | [`revoke_from_web.py`](./revoke_from_web.py) | Remove a user/group from a role |

---

## Official docs

- [SharePoint permissions REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
