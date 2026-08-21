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

---

## Examples

### Create

| Operation | File | Required role |
|---|---|---|
| Create a modern Team site | [`create_team_site.py`](./create_team_site.py) | SharePoint Admin |
| Create a modern Communication site | [`create_comm_site.py`](./create_comm_site.py) | SharePoint Admin |
| Create a classic site | [`create_classic_site.py`](./create_classic_site.py) | SharePoint Admin |

### Read, update, manage

| Operation | File | Required role |
|---|---|---|
| Get site properties | [`get_site_props.py`](./get_site_props.py) | Read access |
| Set site properties | [`update_site.py`](./update_site.py) | Site Owner |
| List site admins | [`get_site_admins.py`](./get_site_admins.py) | SharePoint Admin |
| Get personal site (OneDrive) | [`get_my_site.py`](./get_my_site.py) | User context |
| Delete a site | [`delete_site.py`](./delete_site.py) | SharePoint Admin |
| Full lifecycle (create → update → delete) | [`site_lifecycle.py`](./site_lifecycle.py) | SharePoint Admin + `Sites.FullControl.All` |

> Note: the SDK supports listing site collection administrators but not the
> add/remove write operations — grant owner access via the Members group or
> the SharePoint admin center.

### Site lifecycle & compliance

| Operation | File | Required role |
|---|---|---|
| Find inactive/obsolete sites | [`find_inactive_sites.py`](./find_inactive_sites.py) | SharePoint Admin + `Sites.Read.All` |
| Assign a sensitivity label to a site | [`assign_sensitivity_label.py`](./assign_sensitivity_label.py) | SharePoint Admin + Purview read |
| Check retention policy coverage | [`check_retention_policy.py`](./check_retention_policy.py) | SharePoint Admin + `RecordsManagement.Read.All` |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Get site properties
web = ctx.web.get().execute_query()
print(f"{web.title}  {web.url}  ({web.web_template})")
```

---

## API reference

- [Site creation REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest)
- [Site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations)
