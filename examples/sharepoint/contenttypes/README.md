# Working with Content Types in SharePoint

A **content type** defines the schema (columns), workflow, and behavior
for a category of items in a list or library. Common examples include
"Document", "Task", "Event", and custom content types you define.

---

## ✏️ Create & Manage

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Add a content type to a list
target_list = ctx.web.lists.get_by_title("Documents")
ct = ctx.web.content_types.get_by_name("Document")
target_list.content_types.add_existing(ct).execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Create a content type** | [`create.py`](./create.py) | Add to a list with fields |
| **Delete a content type** | [`delete.py`](./delete.py) | Remove from a list |

## 🔍 Browse

| What | File | Notes |
|------|------|-------|
| **Get content type by name** | [`get_by_name.py`](./get_by_name.py) | Look up content type details |

---

## Official docs

- [SharePoint content types REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
