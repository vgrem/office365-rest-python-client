# Working with Taxonomy (Managed Metadata)

Taxonomy is SharePoint's **managed metadata** system — hierarchical term
stores, term groups, term sets, and individual terms. It's used for
consistent tagging across sites.

The entry point is the **Term Store**, which you access via a dedicated
`TaxonomyService` context.

---

## 🔍 Explore the Term Store

```python
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.taxonomy.service import TaxonomyService

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Access the term store
tax_service = TaxonomyService(ctx)
store = tax_service.term_stores.get().execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Get term store info** | [`get_term_store_info.py`](./get_term_store_info.py) | Name, languages, default language |
| **Get a term group** | [`get_group_by_name.py`](./get_group_by_name.py) | Find a group by name |
| **Get a term set** | [`get_term_set.py`](./get_term_set.py) | Terms in a specific term set |
| **Get a term by ID** | [`get_term_by_id.py`](./get_term_by_id.py) | Look up a single term |
| **Search terms** | [`search_term.py`](./search_term.py) | Keyword search across term sets |
| **Export term store** | [`export_term_store.py`](./export_term_store.py) | Dump all terms to a file |

## ✏️ Taxonomy Fields

```python
# Create a taxonomy field on a list
field = target_list.fields.add_taxonomy_field("Department", term_set_id).execute_query()

# Read a taxonomy field value from an item
tax_value = item.properties.get("Department")
```

| What | File | Notes |
|------|------|-------|
| **Create taxonomy field** | [`create_field.py`](./create_field.py) | Add a managed metadata column |
| **Get taxonomy field value** | [`get_field_value.py`](./get_field_value.py) | Read from a list item |
| **Set taxonomy field value** | [`set_field_value.py`](./set_field_value.py) | Write to a list item |

---

## Official docs

- [SharePoint taxonomy REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
