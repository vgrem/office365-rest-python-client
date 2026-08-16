# Sharing

Share files, folders, and sites with specific people, the whole organization,
or anonymous users via sharing links and direct permission grants.

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
disable external sharing entirely, and **specific users** can be granted
access via role assignments on the item.

---

## Examples

### Sharing links

| Operation | File | Required role | API reference |
|---|---|---|---|
| Share a file (anonymous link lifecycle) | [`share_file.py`](./share_file.py) | Contribute on file | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Share a file (org-wide link) | [`share_file_organizational.py`](./share_file_organizational.py) | Contribute on file | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Share a file with a password | [`share_file_with_password.py`](./share_file_with_password.py) | Contribute on file | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Share a folder (tokenized link + guest URL) | [`share_folder.py`](./share_folder.py) | Contribute on folder | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Share a folder (org-wide link) | [`share_folder_organizational.py`](./share_folder_organizational.py) | Contribute on folder | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Update a sharing link (expiration) | [`update_sharing_link.py`](./update_sharing_link.py) | Contribute on item | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Remove a sharing link | [`remove_sharing_link.py`](./remove_sharing_link.py) | Contribute on item | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Get file sharing info | [`get_file_sharing_info.py`](./get_file_sharing_info.py) | Read access | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Get folder sharing info | [`get_folder_sharing_info.py`](./get_folder_sharing_info.py) | Read access | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |

### Permissions & site policy

| Operation | File | Required role | API reference |
|---|---|---|---|
| Grant a user a role on a file (break inheritance, list assignments, reset) | [`permissions.py`](./permissions.py) | Contribute on item | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Share a site with a user (by group) | [`share_web.py`](./share_web.py) | Site Owner | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Get site external sharing capability | [`get_site_sharing.py`](./get_site_sharing.py) | Site Owner | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |
| Set site external sharing capability | [`set_site_sharing.py`](./set_site_sharing.py) | Site Owner | [Sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Create an anonymous view link for a file
from office365.sharepoint.sharing.links.kind import SharingLinkKind

file = ctx.web.get_file_by_server_relative_url("Shared Documents/report.docx")
result = file.share_link(SharingLinkKind.AnonymousView).execute_query()
print(f"Share link: {result.value.sharingLinkInfo.Url}")
```

---

## API reference

- [SharePoint sharing REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api)
