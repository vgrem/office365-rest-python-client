# Searching SharePoint

SharePoint search uses the **REST query API** to find sites, documents,
and list items across the tenant. Queries are written as simple text
or with property filters, refiners, and sort orders.

This page groups examples by **what you want to do** — not by API endpoint.

---

## 🔍 Query

| What | File | Notes |
|------|------|-------|
| **Keyword search** | [`query_keyword.py`](./query_keyword.py) | Simple keyword query across all content |
| **Search documents** | [`query_documents.py`](./query_documents.py) | Scope to document libraries (`IsDocument:1`) |
| **Search sites** | [`query_sites.py`](./query_sites.py) | Enumerate accessible sites (`contentclass:STS_Site`) |
| **Search by site** | [`query_by_site.py`](./query_by_site.py) | Limit scope with `Path:` managed property |
| **Search by content type** | [`query_by_content_type.py`](./query_by_content_type.py) | Filter by `ContentType:` managed property |
| **Search with filters** | [`query_with_filter.py`](./query_with_filter.py) | Author / date-range KQL filters |
| **Search with sorting** | [`query_with_sort.py`](./query_with_sort.py) | Sort by managed property (`Sort`) |
| **Search with refinement** | [`query_with_refinement.py`](./query_with_refinement.py) | Faceted search — refiners and drill-down |
| **Search with pagination** | [`query_paged.py`](./query_paged.py) | Page through large result sets |

## 📤 Export

| What | File | Notes |
|------|------|-------|
| **Export search reports** | [`export_reports.py`](./export_reports.py) | Tenant-level search usage reports |

---

## Official docs

- [SharePoint search REST API overview](https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview)
