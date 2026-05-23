# Working with Permissions in SharePoint

Permissions are managed through **role assignments** — a user or group is
assigned a **role definition** (Full Control, Edit, Read) on a **securable
object** (site, list, folder, or file).

## 🔐 Get Permissions

| What | File | Notes |
|------|------|-------|
| **Effective permissions (site)** | [`get_for_site.py`](./get_for_site.py) | Current user's permissions on the web |
| **Effective permissions (list)** | [`get_for_list.py`](./get_for_list.py) | Current user's permissions on a list |
| **Effective permissions (file)** | [`get_for_file.py`](./get_for_file.py) | Current user's permissions on a file |
| **Role definitions** | [`get_role_definitions.py`](./get_role_definitions.py) | All permission levels available on the site |

## ✏️ Grant & Revoke

| What | File | Notes |
|------|------|-------|
| **Grant to site** | [`grant_to_web.py`](./grant_to_web.py) | Add a user/group role on a web |
| **Revoke from site** | [`revoke_from_web.py`](./revoke_from_web.py) | Remove a user/group role on a web |
| **Grant to list** | [`grant_to_list.py`](./grant_to_list.py) | Add a user/group role on a list |
| **Revoke from list** | [`revoke_from_list.py`](./revoke_from_list.py) | Remove a user/group role on a list |

## 🔓 Inheritance

| What | File | Notes |
|------|------|-------|
| **Break inheritance** | [`break_inheritance.py`](./break_inheritance.py) | Create unique permissions on a list |
| **Reset inheritance** | [`reset_inheritance.py`](./reset_inheritance.py) | Revert to parent permissions |

---

## Official docs

- [SharePoint permissions REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
