# Sites

Create, read, update, and delete SharePoint sites (site collections).

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **SharePoint Administrator** or **Global Administrator** role | Required to create, update, and delete sites. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Classic vs modern sites

SharePoint has two site models:

| Type | Template | Group-connected | Use case |
|---|---|---|---|
| **Modern Team site** | `GROUP#0` | Yes (M365 group) | Team collaboration, document sharing |
| **Modern Communication site** | `SITEPAGEPUBLISHING#0` | No | Intranet, news, broad announcements |
| **Classic site** | Various (STS#0, etc.) | No | Legacy workflows, on-prem migration |

Modern sites are the default for new provisioning. Classic sites are still
supported but Microsoft recommends modern for new work.

```
Modern Team Site         Modern Comm Site          Classic Site
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ M365 Group      │    │ No group        │    │ No group        │
│ Planner, Teams, │    │ Publishing      │    │ Legacy features │
│ Outlook, etc.   │    │ layout          │    │ STS template    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Examples

### Create

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Create a modern Team site | [`create_team.py`](./create_team.py) | SharePoint Admin | [Site creation API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest) |
| **2** | Create a modern Communication site | [`create_comm.py`](./create_comm.py) | SharePoint Admin | [Site creation API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest) |
| **3** | Create a classic site | [`create_classic.py`](./create_classic.py) | SharePoint Admin | [Site creation API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest) |

### Read & Manage

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **4** | Get site properties | [`get_basic_props.py`](./get_basic_props.py) | Read access | [Site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations) |
| **5** | Get site admins | [`get_admins.py`](./get_admins.py) | Read access | [Site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations) |
| **6** | Get personal site (OneDrive) | [`get_my_site.py`](./get_my_site.py) | User context | [Site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations) |
| **7** | Set site properties | [`set_site_props.py`](./set_site_props.py) | Site Owner | [Site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations) |
| **8** | Add site admin | [`add_admin.py`](./add_admin.py) | Site Owner | [Site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations) |
| **9** | Remove site admin | [`remove_admin.py`](./remove_admin.py) | Site Owner | [Site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations) |
| **10** | Delete site | [`delete_site.py`](./delete_site.py) | SharePoint Admin | [Site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Get site properties
site = ctx.web.get().execute_query()
print(f"Title: {site.title}, URL: {site.url}, Template: {site.get_web_template()}")
```

---

## API reference

- [SharePoint site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations)
- [Modern site creation REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest)
