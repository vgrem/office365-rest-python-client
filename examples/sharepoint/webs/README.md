# Working with Webs in SharePoint

A **web** (also called a site) is a SharePoint container for lists, libraries,
and pages. Every site has one root web and optionally many subsites.
The current context always has a `web` property that represents the current site.

This page groups examples by **what you want to do** — not by API endpoint.

---

## 🔍 Get Web Info

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Get the current web
web = ctx.web.get().execute_query()
print(f"Title: {web.title}, URL: {web.url}")
```

| What | File | Notes |
|------|------|-------|
| **Get web properties** | [`get_props.py`](./get_props.py) | Title, description, URL, ID |
| **Get all webs in site** | [`get_all.py`](./get_all.py) | Subsites under the current site |
| **Get lists in a web** | [`get_lists.py`](./get_lists.py) | All lists and libraries |
| **Get roles** | [`get_roles.py`](./get_roles.py) | Permission role definitions |
| **Get regional settings** | [`get_regional_settings.py`](./get_regional_settings.py) | Locale, time zone, language |
| **Get changes** | [`get_changes.py`](./get_changes.py) | Change log (items, lists, webs) |
| **Get activities** | [`get_activities.py`](./get_activities.py) | Recent site activity feed |
| **Get from absolute URL** | [`get_from_abs_url.py`](./get_from_abs_url.py) | Resolve a full URL to a Web object |

## ⚙️ Configure

| What | File | Notes |
|------|------|-------|
| **Enable Document ID** | [`enable_doc_id.py`](./enable_doc_id.py) | Turn on the Document ID feature |
| **Clear a web** | [`clear_web.py`](./clear_web.py) | Remove all content (lists, pages, etc.) |

---

## Getting started

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Get the current web's properties
web = ctx.web.get().execute_query()
print(f"Title: {web.title}")
print(f"URL: {web.url}")
```

## Official docs

- [SharePoint REST API — working with sites and webs](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
