# Working with Fields in SharePoint

A **field** (also called a column) defines a data type in a list or library —
text, number, date, choice, lookup, taxonomy, calculated, and more.
Fields can be created at the **web level** (available everywhere) or
at the **list level** (scoped to a single list).

## ✏️ Create Fields

| What | File | Notes |
|------|------|-------|
| **Text field** | [`create_text_field.py`](./create_text_field.py) | Single line of text |
| **Number field** | [`create_number_field.py`](./create_number_field.py) | Numeric value |
| **Date field** | [`create_date.py`](./create_date.py) | Date/time column |
| **Choice field** | [`create_choice.py`](./create_choice.py) | Single or multi-value dropdown |
| **Lookup field** | [`create_lookup.py`](./create_lookup.py) | Reference another list |
| **User field** | [`create_user_field.py`](./create_user_field.py) | Person/Group picker |
| **Calculated field** | [`create_calculated.py`](./create_calculated.py) | Formula-based value |
| **Taxonomy field** | [`create_taxonomy.py`](./create_taxonomy.py) | Managed metadata term set |

## 🔍 Read Fields

| What | File | Notes |
|------|------|-------|
| **Get fields from list** | [`get_fields_from_list.py`](./get_fields_from_list.py) | All columns scoped to a list |
| **Get fields from web** | [`get_fields_from_web.py`](./get_fields_from_web.py) | Site columns available globally |

## ✏️ Update Fields

| What | File | Notes |
|------|------|-------|
| **Update field** | [`update_field.py`](./update_field.py) | Change title, required, or other properties |

## 🗑️ Delete Fields

| What | File | Notes |
|------|------|-------|
| **Delete field** | [`delete_field.py`](./delete_field.py) | Remove a field from a list |

## ↔️ Copy Fields

| What | File | Notes |
|------|------|-------|
| **Copy field between sites** | [`copy_field.py`](./copy_field.py) | Duplicate field via schema XML |

---

## Official docs

- [Working with lists and list items — SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest)
