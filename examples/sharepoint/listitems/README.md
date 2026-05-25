# Working with List Items in SharePoint

A **list item** is a single row in a SharePoint list or library.
Items store data in **fields** (columns) like Title, Author, or custom fields.
Every item has a numeric **ID** unique within its list.

All examples use the same auth pattern:

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("{site_url}").with_username_and_password(
    tenant="{tenant}",
    client_id="{client_id}",
    username="{username}",
    password="{password}",
)
target_list = ctx.web.lists.get_by_title("Documents")
```

## ✏️ Create, Update & Delete

| What | File | Notes |
|------|------|-------|
| **Create item** | [`create.py`](./create.py) | Single item with field values |
| **Create in bulk** | [`create_bulk.py`](./create_bulk.py) | Many items in a single request |
| **Update item** | [`update.py`](./update.py) | Change one or more fields |
| **Update in bulk** | [`update_bulk.py`](./update_bulk.py) | Many updates in a single request |
| **System update** | [`system_update.py`](./system_update.py) | Skip version creation on update |
| **Delete item** | [`delete.py`](./delete.py) | Remove an item |
| **Delete in bulk** | [`delete_bulk.py`](./delete_bulk.py) | Remove many items |
| **Copy items** | [`copy_items.py`](./copy_items.py) | Copy between lists |

## 🔍 Read & Query

| What | File | Notes |
|------|------|-------|
| **Read items** | [`read.py`](./read.py) | Get all items from a list |
| **Read with properties** | [`read_include_props.py`](./read_include_props.py) | Include specific fields |
| **Read with user info** | [`read_include_user.py`](./read_include_user.py) | Expand user/author fields |
| **Filter items** | [`filter.py`](./filter.py) | OData `$filter` queries |
| **Filter by filename** | [`filter_by_filename.py`](./filter_by_filename.py) | Filter documents by name |
| **Filter by folder** | [`filter_by_folder.py`](./filter_by_folder.py) | Filter items in a folder |
| **Get grouped items** | [`get_grouped.py`](./get_grouped.py) | Group by a field value |
| **Get deleted items** | [`get_deleted.py`](./get_deleted.py) | Retrieve items from recycle bin |
| **Query throttling** | [`query_throttle.py`](./query_throttle.py) | Handle 5000+ row threshold |
| **Export to CSV** | [`export_to_csv.py`](./export_to_csv.py) | Export list items to file |

## 🔗 Lookup & Field Values

| What | File | Notes |
|------|------|-------|
| **Set date/time field** | [`set_datetime_field_value.py`](./set_datetime_field_value.py) | DateTime field types |
| **Set lookup field** | [`set_lookup_field_value.py`](./set_lookup_field_value.py) | Reference another list |
| **Set image field** | [`set_image_field_value.py`](./set_image_field_value.py) | Image/Hyperlink fields |
| **Get lookup field value** | [`get_lookup_field_value.py`](./get_lookup_field_value.py) | Read a lookup field |

## 📎 Attachments

| What | File | Notes |
|------|------|-------|
| **List attachments** | [`attachments/list.py`](./attachments/list.py) | Enumerate item attachments |
| **Upload attachment** | [`attachments/upload.py`](./attachments/upload.py) | Add a file attachment |
| **Download attachment** | [`attachments/download.py`](./attachments/download.py) | Save attachment to disk |
| **Delete attachment** | [`attachments/delete.py`](./attachments/delete.py) | Remove an attachment |

## 📋 Versions

| What | File | Notes |
|------|------|-------|
| **List versions** | [`versions/list.py`](./versions/list.py) | All versions of an item |

---

## Official docs

- [Working with lists and list items — SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest)
