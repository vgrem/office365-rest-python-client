# Content Types

Manage SharePoint content types — create, update, delete, add fields, and associate with lists.

| What | PnP equivalent | File | Notes |
|------|---------------|------|-------|
| **Create content type** | `Add-PnPContentType` | [`create.py`](./create.py) | Add a new content type to a site |
| **Get content type** | `Get-PnPContentType` | [`get_by_name.py`](./get_by_name.py) | Retrieve by name |
| **Update content type** | `Set-PnPContentType` | [`update.py`](./update.py) | Change description or properties |
| **Delete content type** | `Remove-PnPContentType` | [`delete.py`](./delete.py) | Remove from a site |
| **Add field to content type** | `Add-PnPFieldToContentType` | [`add_field.py`](./add_field.py) | Add a site column |
| **Add to list** | `Add-PnPContentTypeToList` | [`add_to_list.py`](./add_to_list.py) | Associate with a list |
| **Set default for list** | `Set-PnPDefaultContentTypeToList` | [`set_default.py`](./set_default.py) | Make default in a list |

---

## Official docs

- [Content type REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype)
