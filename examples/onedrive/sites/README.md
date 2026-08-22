# OneDrive / SharePoint v2 — Sites

Examples for working with SharePoint sites via Microsoft Graph API.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Sites.Read.All` (delegated or app) | Read sites, storage, permissions, analytics | [Sites permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#sites-permissions) |
| `Sites.ReadWrite.All` (delegated or app) | Create, follow, manage sites, manage admins | [Sites permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#sites-permissions) |

---

## Discovery & Reporting

| Scenario | File | Why it's useful |
|---|---|---|
| **Get sites** — root, by URL, followed | [`get_site.py`](./get_site.py) | Find sites in your tenant |
| **Get site by path** — server-relative path, no URL needed | [`get_site_by_path.py`](./get_site_by_path.py) | Address a site by relative path |
| **Search and follow** — keyword search, follow a site | [`search_and_follow.py`](./search_and_follow.py) | Discover and subscribe to sites |
| **List all sites** — paginate through the full site collection | [`list_all.py`](./list_all.py) | Inventory every site in the tenant |
| **List subsites** — sites under a site collection | [`subsites.py`](./subsites.py) | Site-collection administration |
| **Storage report** — used vs quota per site | [`storage_report.py`](./storage_report.py) | Find sites running out of storage |
| **Site analytics** — views, visits, edits per site | [`analytics_report.py`](./analytics_report.py) | Adoption tracking — most active sites |
| **Site activities** — daily views/edits over a window | [`site_activities.py`](./site_activities.py) | Adoption over time |
| **Find stale sites** — sites with no activity | [`find_stale.py`](./find_stale.py) | Identify cleanup candidates |

## Security & Governance

| Scenario | File | Why it's useful |
|---|---|---|
| **Site permissions** — list users and groups with access | [`site_permissions.py`](./site_permissions.py) | Governance — who has access? |
| **Grant access** — grant read/write to a user | [`grant_permission.py`](./grant_permission.py) | Share a site with a specific user |
| **Revoke access** — remove a specific permission | [`revoke_permission.py`](./revoke_permission.py) | Clean up access |
| **Sharing link** — anonymous view/edit link for a site | [`share_site_link.py`](./share_site_link.py) | Create a link to share the site |
| **Content types & columns** — site-level inventory | [`site_governance.py`](./site_governance.py) | Governance — what's defined at site level |
| **External sharing audit** — detect guest access | [`external_sharing.py`](./external_sharing.py) | Security — find overshared sites |

## Administration

| Scenario | File | Why it's useful |
|---|---|---|
| **Stale site lifecycle** — find, report, resolve owners, delete | [`stale_lifecycle.py`](./stale_lifecycle.py) | Full stale site cleanup workflow |
| **Add site admin** | [`add_admin.py`](./add_admin.py) | Grant owner access to a user |
| **Remove site admin** | [`remove_admin.py`](./remove_admin.py) | Revoke a user's access |
| **Unfollow a site** | [`unfollow_site.py`](./unfollow_site.py) | Stop following a site |

> **Note:** Microsoft Graph v1.0 does not support creating, deleting, or renaming SharePoint
> sites (site lifecycle is managed via the SharePoint REST/tenant admin APIs). Use the
> [`examples/sharepoint/sites`](../../sharepoint/sites) examples (`create_team_site.py`, `create_comm_site.py`,
> `delete_site.py`, `site_lifecycle.py`) for those operations.

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

site = client.sites.root.get().execute_query()
print(f"Root site: {site.display_name}")
```

---

## Official docs

- [Site API overview](https://learn.microsoft.com/en-us/graph/api/resources/site)
- [List sites](https://learn.microsoft.com/en-us/graph/api/site-list)
- [Create site](https://learn.microsoft.com/en-us/graph/api/site-create)
- [Site permissions](https://learn.microsoft.com/en-us/graph/api/site-list-permissions)
- [Item analytics](https://learn.microsoft.com/en-us/graph/api/itemanalytics-get)
