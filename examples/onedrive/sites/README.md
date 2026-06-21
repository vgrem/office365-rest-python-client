# OneDrive / SharePoint v2 — Sites

Examples for working with SharePoint sites via Microsoft Graph API.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Sites.Read.All` (delegated or app) | Read sites, storage, permissions, analytics | [Sites permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#sites-permissions) |
| `Sites.ReadWrite.All` (delegated or app) | Create, follow, and manage sites | [Sites permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#sites-permissions) |

---

## Patterns

| Scenario | File | Why it's useful |
|---|---|---|
| **Get sites** — root, by URL, followed | [`get_site.py`](./get_site.py) | Find sites in your tenant |
| **Search and follow** — keyword search, follow a site | [`search_and_follow.py`](./search_and_follow.py) | Discover and subscribe to sites |
| **List all sites** — paginate through the full site collection | [`list_all.py`](./list_all.py) | Inventory every site in the tenant |
| **Storage report** — used vs quota per site | [`storage_report.py`](./storage_report.py) | Find sites running out of storage |
| **External sharing audit** — detect guest access | [`external_sharing.py`](./external_sharing.py) | Security — find overshared sites |
| **Site permissions** — list users and groups with access | [`site_permissions.py`](./site_permissions.py) | Governance — who has access? |
| **Create a site** — modern team or communication site | [`create_site.py`](./create_site.py) | Provision new sites via API |
| **Site analytics** — views, visits, edits per site | [`analytics_report.py`](./analytics_report.py) | Adoption tracking — most active sites |

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
