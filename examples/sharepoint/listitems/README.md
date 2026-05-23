# Working with List Items in SharePoint

A **list item** is a single row in a SharePoint list or library.
Items store data in **fields** (columns) like Title, Author, or custom fields.
Every item has a numeric **ID** unique within its list.

This page groups examples by **what you want to do** — not by API endpoint.

---

## ✏️ Create, Update & Delete

```python
# Create
target_list.add_item({"Title": "Task1"}).execute_query()

# Update
item.set_property("Title", "New name").update().execute_query()

# Delete
item.delete_object().execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Create a list item** | [`create.py`](./create.py) | Set field values in a dict |
| **Create items in bulk** | [`create_bulk.py`](./create_bulk.py) | Many items, single request |
| **Update a list item** | [`update.py`](./update.py) | Change one or more fields |
| **Update items in bulk** | [`update_bulk.py`](./update_bulk.py) | Many updates, single request |
| **System update** (skip version) | [`system_update.py`](./system_update.py) | No new version created |
| **System update (alt)** | [`system_update_alt.py`](./system_update_alt.py) | Alternative API |
| **Delete a list item** | [`delete.py`](./delete.py) | Moves to recycle bin |
| **Delete items in bulk** | [`delete_bulk.py`](./delete_bulk.py) | Many deletes, single request |
| **Copy items between lists** | [`copy_items.py`](./copy_items.py) | |

## 🔍 Read & Query

```python
# Read all items
items = target_list.items.get().execute_query()

# Read with specific fields
items = target_list.items.include("Title", "Author").get().execute_query()

# Filter with CAML query
items = target_list.get_items_by_caml_query(query_xml).execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Read all items** | [`read.py`](./read.py) | Default fields |
| **Include specific properties** | [`read_include_props.py`](./read_include_props.py) | Only fetch what you need |
| **Include user details** | [`read_include_user.py`](./read_include_user.py) | Expand user/group fields |
| **Read with CAML query** | [`read_list_via_query_alt.py`](./read_list_via_query_alt.py) | Complex filters |
| **Read with properties (alt)** | [`read_with_props_alt.py`](./read_with_props_alt.py) | Alternative pattern |
| **Filter by field value** | [`filter.py`](./filter.py) | `$filter` OData query |
| **Filter by file name** | [`filter_by_filename.py`](./filter_by_filename.py) | Filter documents by name |
| **Filter by folder** | [`filter_by_folder.py`](./filter_by_folder.py) | Items in a specific folder |
| **Group by field** | [`get_grouped.py`](./get_grouped.py) | Group results by column |
| **Get deleted items** | [`get_deleted.py`](./get_deleted.py) | Items in the recycle bin |
| **Handle large queries** | [`query_throttle.py`](./query_throttle.py) | Throttling + retry |
| **Export to CSV** | [`export_to_csv.py`](./export_to_csv.py) | Save as a local file |

## 🔗 Lookup & Taxonomy Fields

```python
# Set a lookup field
value = FieldLookupValue(LookupId=task_id)
item.set_property("ParentTask", value).update().execute_query()

# Read a lookup field value
lookup_value = item.properties.get("ParentTask")
```

| What | File | Notes |
|------|------|-------|
| **Set lookup field value** | [`set_lookup_field_value.py`](./set_lookup_field_value.py) | Single and multi lookup |
| **Get lookup field value** | [`get_lookup_field_value.py`](./get_lookup_field_value.py) | Read and display |

## 📅 Special Field Types

| What | File | Notes |
|------|------|-------|
| **Set date/time field** | [`set_datetime_field_value.py`](./set_datetime_field_value.py) | ISO 8601 format |
| **Set image field** | [`set_image_field_value.py`](./set_image_field_value.py) | Upload + set image |

## 📎 Attachments

| File | What it does |
|------|-------------|
| [`attachments/list.py`](./attachments/list.py) | List all attachments on an item |
| [`attachments/upload.py`](./attachments/upload.py) | Attach a file to an item |
| [`attachments/download.py`](./attachments/download.py) | Download all attachments |
| [`attachments/download_per_attachment.py`](./attachments/download_per_attachment.py) | Download one attachment |
| [`attachments/delete.py`](./attachments/delete.py) | Remove an attachment |

## 📜 Version History

| File | What it does |
|------|-------------|
| [`versions/list.py`](./versions/list.py) | List all versions of an item |

---

## Getting started

All examples use the same pattern:

```python
from office365.sharepoint.client_context import ClientContext
from tests import test_team_site_url, test_client_id, test_client_secret

ctx = ClientContext(test_team_site_url).with_client_credentials(
    test_client_id, test_client_secret
)

# Get a reference to a list, then work with its items
target_list = ctx.web.lists.get_by_title("Documents")
items = target_list.items.get().execute_query()
for item in items:
    print(item.properties.get("Title"))
```

Replace the test imports with your own credentials when running outside the test suite.

## Official docs

- [Working with list items — SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest#working-with-list-items-by-using-rest)
