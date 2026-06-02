# Modern (Site) Pages

Create, read, update, publish, and manage modern SharePoint pages.

> **Classic page types are legacy.** Wiki pages and web part pages belong to
> the classic SharePoint experience. Use **modern Site Pages** for new work.
>
> For wiki page creation, see
> [`../files/create_wiki.py`](../files/create_wiki.py).
> For building custom page components, use
> [SPFx client-side web parts](https://learn.microsoft.com/en-us/sharepoint/dev/spfx/web-parts/get-started/build-a-hello-world-web-part).

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** or **Member** role | Required to create, update, and delete pages. Read access for browsing. | [SharePoint permissions](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Getting started

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# List all site pages
pages = ctx.web.site_pages.pages.get().execute_query()
for page in pages:
    print(f"  {page.file_name}  — {page.title}")
```

---

## Create & Publish

| What | File | Notes |
|------|------|-------|
| **Create page** | [`create.py`](./create.py) | Create a modern page |
| **Create and publish** | [`create_and_publish.py`](./create_and_publish.py) | Create + publish in one flow |
| **Promote to news** | [`promote_to_news.py`](./promote_to_news.py) | Promote or demote as news |

## Read & Browse

| What | File | Notes |
|------|------|-------|
| **List pages** | [`list.py`](./list.py) | Enumerate all site pages |
| **Get page by name** | [`get_by_name.py`](./get_by_name.py) | Get a specific page by filename |
| **Get page content** | [`get_content.py`](./get_content.py) | Read canvas and layout content |

## Update & Delete

| What | File | Notes |
|------|------|-------|
| **Update page** | [`update.py`](./update.py) | Change title or properties |
| **Delete page** | [`delete.py`](./delete.py) | Remove a page |

---

## API reference

- [Site pages REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference)
- [Create and use modern pages](https://support.microsoft.com/en-gb/office/create-and-use-modern-pages-on-a-sharepoint-site-b3d46deb-27a6-4b1e-87b8-df851e503dec)
