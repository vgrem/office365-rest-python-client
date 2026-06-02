# Modern (Site) Pages

> **⚠️ Classic page types are legacy.** Wiki pages and web part pages belong to
> the classic SharePoint experience. Use **modern Site Pages** for new work.
>
> For wiki page creation, see
> [`../files/create_wiki.py`](../files/create_wiki.py).
> For building custom page components, use
> [SPFx client-side web parts](https://learn.microsoft.com/en-us/sharepoint/dev/spfx/web-parts/get-started/build-a-hello-world-web-part).

Create, read, update, publish, and manage modern SharePoint pages.
Modern pages use a canvas layout with web parts and can be promoted to news.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** or **Member** role | Required to create, update, and delete pages. Read access for browsing. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List — enumerate all site pages | [`list.py`](./list.py) | Read access | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **2** | Get — retrieve a page by filename | [`get_by_name.py`](./get_by_name.py) | Read access | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **3** | Get content — read canvas and layout | [`get_content.py`](./get_content.py) | Read access | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **4** | Create — add a new modern page | [`create.py`](./create.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **5** | Create and publish — add + publish in one flow | [`create_and_publish.py`](./create_and_publish.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **6** | Promote to news — promote or demote as news | [`promote_to_news.py`](./promote_to_news.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **7** | Update — change title or properties | [`update.py`](./update.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **8** | Delete — remove a page | [`delete.py`](./delete.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |

---

## Quick start

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

## API reference

- [Site pages REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference)
- [Create and use modern pages](https://support.microsoft.com/en-gb/office/create-and-use-modern-pages-on-a-sharepoint-site-b3d46deb-27a6-4b1e-87b8-df851e503dec)
