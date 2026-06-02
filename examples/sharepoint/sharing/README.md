# Sharing

Share files, folders, and sites with specific people, the whole organization,
or anonymous users via sharing links.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Contribute** or higher on the item being shared | Required to create sharing links. Site Owner to change site-level sharing policy. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## How sharing works

Every sharing operation creates a **sharing link** that encodes the access
level and audience. SharePoint supports these link types:

| Link kind | Access level | Scope |
|---|---|---|
| **Anonymous view** | Anyone with the link can view | External (no sign-in) |
| **Anonymous edit** | Anyone with the link can edit | External (no sign-in) |
| **Organization view** | Everyone in your org can view | Internal |
| **Organization edit** | Everyone in your org can edit | Internal |
| **Specific people** | Only named users can access | Internal or external |
| **Direct** | Canonical URL (no sharing link) | Inherits permissions |

Sharing is also controlled at the **site level** — admins can restrict or
disable external sharing entirely.

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Get site sharing capability | [`get_site_sharing.py`](./get_site_sharing.py) | Site Owner | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **2** | Set site sharing capability | [`set_site_sharing.py`](./set_site_sharing.py) | Site Owner | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **3** | Share a file with specific people | [`share_file.py`](./share_file.py) | Contribute on file | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **4** | Share a file (org-wide link) | [`share_file_organizational.py`](./share_file_organizational.py) | Contribute on file | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **5** | Share a file with password | [`share_file_with_password.py`](./share_file_with_password.py) | Contribute on file | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **6** | Share a folder with specific people | [`share_folder.py`](./share_folder.py) | Contribute on folder | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **7** | Share a folder (org-wide link) | [`share_folder_organizational.py`](./share_folder_organizational.py) | Contribute on folder | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **8** | Share a folder (anonymous link) | [`share_folder_anonymous.py`](./share_folder_anonymous.py) | Contribute on folder | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **9** | Share a site | [`share_web.py`](./share_web.py) | Site Owner | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **10** | Create anonymous link | [`create_anonymous_link.py`](./create_anonymous_link.py) | Contribute on file | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **11** | Update sharing link (expiration) | [`update_sharing_link.py`](./update_sharing_link.py) | Contribute on item | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **12** | Remove sharing link | [`remove_sharing_link.py`](./remove_sharing_link.py) | Contribute on item | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **13** | Get file sharing info | [`get_file_sharing_info.py`](./get_file_sharing_info.py) | Read access | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| **14** | Get folder sharing info | [`get_folder_sharing_info.py`](./get_folder_sharing_info.py) | Read access | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Share a file with specific people
file = ctx.web.get_file_by_server_relative_url("/sites/team/Shared Documents/report.docx")
file.share("user@contoso.com", read_only=True).execute_query()

# Create an anonymous view link
from office365.sharepoint.sharing.links.kind import SharingLinkKind
link = file.share_link(SharingLinkKind.AnonymousView).execute_query()
print(f"Link: {link.value}")
```

---

## API reference

- [SharePoint sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api)
