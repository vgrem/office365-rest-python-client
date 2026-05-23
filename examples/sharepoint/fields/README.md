# Working with Fields in SharePoint

A **field** (also called a column) defines a data type in a list or library —
text, number, date, choice, lookup, taxonomy, calculated, and more.
Fields can be created at the **web level** (available everywhere) or
at the **list level** (scoped to a single list).

This page groups examples by **what you want to do** — not by API endpoint.

---

## ✏️ Create Fields

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Get a target list
target_list = ctx.web.lists.get_by_title("Documents")

# Create a choice field
field = target_list.fields.add_choice_field("Status", ["Not Started", "In Progress", "Completed"]).execute_query()

# Create a lookup field
field = target_list.fields.add_lookup_field("RelatedDoc", target_list.id, "Title").execute_query()

# Create a date/time field
field = target_list.fields.add_date_time_field("Deadline").execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Create choice field** | [`create_choice.py`](./create_choice.py) | Single or multi-value |
| **Create lookup field** | [`create_lookup.py`](./create_lookup.py) | Reference another list |
| **Create date/time field** | [`create_date.py`](./create_date.py) | Date only or date + time |
| **Create calculated field** | [`create_calculated.py`](./create_calculated.py) | Formula-based value |
| **Create taxonomy field** | [`create_taxonomy.py`](./create_taxonomy.py) | Managed metadata term set |

## 🔍 Get Fields

| What | File | Notes |
|------|------|-------|
| **Get fields from a list** | [`get_from_list.py`](./get_from_list.py) | All fields scoped to a list |
| **Get fields from web** | [`get_from_web.py`](./get_from_web.py) | Site columns available globally |

## ↔️ Copy Fields

| What | File | Notes |
|------|------|-------|
| **Copy field between lists** | [`copy_field.py`](./copy_field.py) | Duplicate field definition |

---

## Official docs

- [Working with lists and list items — SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest)
