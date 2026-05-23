# Searching SharePoint

SharePoint search uses the **REST query API** to find sites, documents,
and list items across the tenant. Queries are written as simple text
or with property filters and sort orders.

This page groups examples by **what you want to do** — not by API endpoint.

---

## 🔍 Basic Search

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Simple keyword search
result = ctx.search.query("financial report").execute_query()
for item in result.value:
    print(item.Title, item.Path)
```

| What | File | Notes |
|------|------|-------|
| **Simple search** | [`search_simple.py`](./search_simple.py) | Keyword query across all content |
| **Search documents only** | [`search_documents.py`](./search_documents.py) | Scope to document libraries |
| **Search sites only** | [`search_site_only.py`](./search_site_only.py) | Scope to site collections |
| **Search with sorting** | [`search_sort_list.py`](./search_sort_list.py) | Sort by managed property |
| **Search all sites** | [`search_sites.py`](./search_sites.py) | Enumerate accessible sites |

## 📤 Export Search Results

| What | File | Notes |
|------|------|-------|
| **Export search reports** | [`export_reports.py`](./export_reports.py) | Save query results to file |

---

## Official docs

- [SharePoint search REST API overview](https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview)
