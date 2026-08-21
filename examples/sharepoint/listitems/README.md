# Working with List Items

A **list item** is a single row in a SharePoint list or library.
Items store data in fields (columns) and have a numeric ID unique
within their list.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** or **Member** role on the list | Required to create, update, and delete items. Read access for queries. | [SharePoint permissions](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Getting started

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

target_list = ctx.web.lists.get_by_title("Documents")

# Read all items
items = target_list.items.get().execute_query()
for item in items:
    print(f"  {item.id}: {item.properties.get('Title', '')}")

# Create an item
item = target_list.add_item({"Title": "New report"}).execute_query()
print(f"Created: {item.id}")
```

---

## Create, Update & Delete

| What | File | Notes |
|------|------|-------|
| **Create item** | [`create.py`](./create.py) | Single item with field values |
| **Create in bulk** | [`create_bulk.py`](./create_bulk.py) | Many items via a single `$batch` request |
| **Update item** | [`update.py`](./update.py) | Change one or more fields |
| **Update in bulk** | [`update_bulk.py`](./update_bulk.py) | Many updates in a single `$batch` request |
| **Delete item** | [`delete.py`](./delete.py) | Remove an item |
| **Delete in bulk** | [`delete_bulk.py`](./delete_bulk.py) | Remove many items in a single `$batch` request |

## Read & Query

| What | File | Notes |
|------|------|-------|
| **Read items** | [`read.py`](./read.py) | Get all items from a list |
| **Read with properties** | [`read_include_props.py`](./read_include_props.py) | Include specific fields via `$select` |
| **Filter items** | [`filter.py`](./filter.py) | OData `$filter` queries |
| **Filter by filename** | [`filter_by_filename.py`](./filter_by_filename.py) | Filter documents by name |
| **Export to CSV** | [`export_to_csv.py`](./export_to_csv.py) | Export list items to file |

## Lookup & Field Values

| What | File | Notes |
|------|------|-------|
| **Set date/time field** | [`set_datetime_field_value.py`](./set_datetime_field_value.py) | DateTime field types |
| **Set lookup field** | [`set_lookup_field_value.py`](./set_lookup_field_value.py) | Reference another list |
| **Get lookup field value** | [`get_lookup_field_value.py`](./get_lookup_field_value.py) | Read a lookup field |

## Attachments

| What | File | Notes |
|------|------|-------|
| **List attachments** | [`attachments/list.py`](./attachments/list.py) | Enumerate item attachments |
| **Upload attachment** | [`attachments/upload.py`](./attachments/upload.py) | Add a file attachment |
| **Download attachment** | [`attachments/download.py`](./attachments/download.py) | Save attachment to disk |
| **Delete attachment** | [`attachments/delete.py`](./attachments/delete.py) | Remove an attachment |

## Versions

| What | File | Notes |
|------|------|-------|
| **List versions** | [`versions/list.py`](./versions/list.py) | All versions of an item |

---

## API reference

- [Working with lists and list items — SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest)
