# Working with Lists in SharePoint

A **list** is a container for rows of data — like a database table.
A **document library** is a special kind of list that also stores files.
Every list has a **title** and a **unique ID** (GUID).

This page groups examples by **what you want to do** — not by API endpoint.

---

## ✏️ Create & Manage

```python
# Create a list
target_list = ctx.web.lists.add("My List", description="").execute_query()

# Delete a list
target_list.delete_object().execute_query()

# Save as template
target_list.save_as_template("MyTemplate.stp", "My Template", "").execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Create a list** | [`create.py`](./create.py) | With title and description |
| **Delete a list** | [`delete.py`](./delete.py) | Moves to recycle bin |
| **Save as template** | [`save_as_template.py`](./save_as_template.py) | Export as `.stp` file |
| **Clear all items** | [`clear.py`](./clear.py) | Removes every item |
| **Show / hide columns** | [`show_hide_columns.py`](./show_hide_columns.py) | Toggle column visibility in views |

## 🔍 Read & Browse

```python
# Read list properties
props = target_list.get().execute_query()
print(props.title, props.id)

# Read all items
items = target_list.items.get().execute_query()

# Read with paging
page = target_list.get_items_by_caml_query(caml_query).execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Read list properties** | [`read_properties.py`](./read_properties.py) | Title, ID, description, item count |
| **Read list schema** | [`read_schema.py`](./read_schema.py) | Fields, content types, settings |
| **Read all lists** | [`read_all.py`](./read_all.py) | All lists on a site |
| **Read with paging** | [`read_paged.py`](./read_paged.py) | Paginated item rows |
| **Get list size** | [`read_lib_size.py`](./read_lib_size.py) | Total storage used |
| **Get changes** | [`get_changes.py`](./get_changes.py) | Change log since a time stamp |
| **Get data as stream** | [`get_data_as_stream.py`](./get_data_as_stream.py) | Low-level data access |
| **Export list metadata** | [`export_list.py`](./export_list.py) | List definition as XML |

## 📥 Import

```python
# Import from CSV
ctx.web.lists.import_list(Path(csv_path), target_list.title, True).execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Import from CSV** | [`import_list.py`](./import_list.py) | Creates items from a `.csv` file |
| **Import from library** | [`import_lib.py`](./import_lib.py) | Import files into a library |

## 🔍 Filter & Query

```python
# Filter with OData
items = target_list.items.filter("Title eq 'Task1'").get().execute_query()

# Filter with CAML
items = target_list.get_items_by_caml_query(caml_xml).execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Filter with OData** | [`read_items_with_filter.py`](./read_items_with_filter.py) | `$filter` query syntax |
| **Filter with CAML** | [`read_items_with_caml_query.py`](./read_items_with_caml_query.py) | XML-based query language |
| **Filter list collection** | [`filter.py`](./filter.py) | Filter which lists are returned |

## 🛠️ Advanced

| File | What it does |
|------|-------------|
| [`assessment/broken_tax_field_value.py`](./assessment/broken_tax_field_value.py) | Diagnose and fix broken taxonomy field values |

---

## Getting started

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Get a reference to a list by title, then work with it
target_list = ctx.web.lists.get_by_title("Documents")
props = target_list.get().execute_query()
print(props.title)
```

## Official docs

- [Working with lists — SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest#retrieving-lists-and-list-properties-with-rest)
