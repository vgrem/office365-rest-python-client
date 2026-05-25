# Modern (Site) Pages

Create, read, update, publish, and manage modern SharePoint pages.

| What | PnP equivalent | File | Notes |
|------|---------------|------|-------|
| **Create page** | `Add-PnPPage` | [`create.py`](./create.py) | Create a modern page |
| **Create and publish** | `Add-PnPPage` + `Publish-PnPPage` | [`create_and_publish.py`](./create_and_publish.py) | Create + publish in one flow |
| **List pages** | `Get-PnPPage` | [`list.py`](./list.py) | Enumerate all site pages |
| **Get page** | `Get-PnPPage -Identity` | [`get_by_name.py`](./get_by_name.py) | Get a specific page by filename |
| **Get page content** | `Get-PnPPage` | [`get_content.py`](./get_content.py) | Read canvas and layout content |
| **Update page** | `Set-PnPPage` | [`update.py`](./update.py) | Change title or properties |
| **Delete page** | `Remove-PnPPage` | [`delete.py`](./delete.py) | Remove a page |
| **Promote to news** | — | [`promote_to_news.py`](./promote_to_news.py) | Promote or demote as news |

> For **wiki pages**, see [`examples/sharepoint/files/create_wiki.py`](../files/create_wiki.py).

---

## Official docs

- [SharePoint pages overview](https://support.microsoft.com/en-gb/office/create-and-use-modern-pages-on-a-sharepoint-site-b3d46deb-27a6-4b1e-87b8-df851e503dec)
- [Site pages REST API reference](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference)
- [PnP PowerShell page cmdlets](https://pnp.github.io/powershell/cmdlets/Add-PnPPage.html)
