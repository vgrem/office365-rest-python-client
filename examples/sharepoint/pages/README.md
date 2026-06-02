# Modern (Site) Pages

> **⚠️ Classic page types are legacy.** SharePoint has two page families:
>
> | Classic pages (legacy) | Modern pages (current) |
> |---|---|
> | Wiki pages, web part pages, blog pages, publishing pages | Site Pages |
> | Classic UI, no mobile responsive | Canvas layout with responsive web parts |
> | Created in Site Pages library with classic experience | Created in Site Pages library with modern experience |
> | Not supported on modern team/communication sites | Default on modern sites |
>
> Use **modern Site Pages** for new work. For building custom page components,
> use [SPFx client-side web parts](https://learn.microsoft.com/en-us/sharepoint/dev/spfx/web-parts/get-started/build-a-hello-world-web-part).
>
> - [SharePoint classic and modern experiences overview](https://support.microsoft.com/en-us/office/sharepoint-classic-and-modern-experiences-5725c103-505d-4a6e-9350-300d3ec7d73f)
> - [Transform classic pages to modern pages](https://learn.microsoft.com/en-us/sharepoint/dev/transform/modernize-userinterface-site-pages)
> - [Create and edit classic SharePoint pages](https://support.microsoft.com/en-us/office/create-and-edit-classic-sharepoint-pages-ee50e579-a092-4c32-b797-20c6e569608b)

Create, read, update, publish, and manage modern SharePoint pages.
Modern pages use a canvas layout with web parts and can be promoted to news posts.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** or **Member** role | Required to create, update, and delete pages. Read access for browsing. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List: enumerate all site pages | [`list.py`](./list.py) | Read access | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **2** | Get: retrieve a page by filename | [`get_by_name.py`](./get_by_name.py) | Read access | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **3** | Get content: read canvas and layout | [`get_content.py`](./get_content.py) | Read access | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **4** | Create: add a new modern page | [`create.py`](./create.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **5** | Create and publish: add + publish in one flow | [`create_and_publish.py`](./create_and_publish.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **6** | Promote to news: promote or demote as news post | [`promote_to_news.py`](./promote_to_news.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **7** | Update: change title or properties | [`update.py`](./update.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |
| **8** | Delete: remove a page | [`delete.py`](./delete.py) | Member on site | [Site pages API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference) |

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
    print(f"  {page.file_name}  : {page.title}")
```

---

## API reference

- [Site pages REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference)
- [Create and use modern pages](https://support.microsoft.com/en-us/office/create-and-use-modern-pages-on-a-sharepoint-site-b3d46deb-27a6-4b1e-87b8-df851e503dec)
- [Create and edit classic SharePoint pages](https://support.microsoft.com/en-us/office/create-and-edit-classic-sharepoint-pages-ee50e579-a092-4c32-b797-20c6e569608b)
