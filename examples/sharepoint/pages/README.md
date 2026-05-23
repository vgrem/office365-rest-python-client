# Working with Pages in SharePoint

A **page** is a special kind of file (`.aspx`) stored in the **Site Pages**
library. SharePoint supports both **wiki pages** (rich text + web parts)
and **modern (client-side) pages**. Pages have a unique name within a site.

---

## ✏️ Create & Publish

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Create a wiki page
page = ctx.web.add_wiki_page("MyPage").execute_query()

# Create and publish a modern page
from office365.sharepoint.pages.pages_service import SitePageService
svc = SitePageService(ctx)
svc.create_page("MyPage", "My Page Title").publish().execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Create a page** | [`create.py`](./create.py) | Wiki page in Site Pages library |
| **Create and publish** | [`create_and_publish.py`](./create_and_publish.py) | Modern page with publish step |

## 🔍 Browse Pages

| What | File | Notes |
|------|------|-------|
| **List all pages** | [`list.py`](./list.py) | All pages in a site |
| **Get page by name** | [`get_by_name.py`](./get_by_name.py) | Look up a single page |
| **Get page content** | [`get_content.py`](./get_content.py) | Read the HTML/wiki content |

---

## Official docs

- [SharePoint pages REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
