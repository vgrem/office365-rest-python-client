# Working with Views in SharePoint

A **view** defines how a list or library is displayed — which columns
to show, the sort order, filters, and grouping. Every list has a
**default view** and can have many **custom views**.

---

## 🔍 Read Views

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Get the default view of a list
target_list = ctx.web.lists.get_by_title("Documents")
default_view = target_list.default_view.get().execute_query()
print(default_view.title, default_view.view_type)
```

| What | File | Notes |
|------|------|-------|
| **Read default view** | [`read_default.py`](./read_default.py) | Title, fields, order, type |
| **Read custom views** | [`read_custom.py`](./read_custom.py) | All non-default views |

## 📤 Export

| What | File | Notes |
|------|------|-------|
| **Export view definition** | [`export_view.py`](./export_view.py) | View schema as XML |
| **Export view items** | [`export_items.py`](./export_items.py) | Items as they appear in a view |

---

## Official docs

- [SharePoint views REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
