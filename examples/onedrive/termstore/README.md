# Term Store (Managed Metadata)

Work with the term store — the managed metadata service for consistent tagging
across SharePoint and OneDrive: create taxonomy, export/import it, search, and
clean up.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Sites.ReadWrite.All` (delegated) | Create/search/delete terms | [Sites permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#sites-permissions) |
| `TermStore.Read.All` / `TermStore.ReadWrite.All` (app) | Export / import the store | [TermStore permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#term-store-permissions) |

---

## Examples

| Operation | File | API |
|---|---|---|
| Create groups, sets, terms | [`create_terms.py`](./create_terms.py) | [termStore group create](https://learn.microsoft.com/en-us/graph/api/termstore-group-post) |
| Search the store by term label | [`search_term.py`](./search_term.py) | [store search](https://learn.microsoft.com/en-us/graph/api/termstore-store-search) |
| Export the full hierarchy to CSV/JSON | [`export_store.py`](./export_store.py) | [group list](https://learn.microsoft.com/en-us/graph/api/termstore-store-list-groups) |
| Import a hierarchy from JSON | [`import_store.py`](./import_store.py) | [set create](https://learn.microsoft.com/en-us/graph/api/termstore-set-post) |
| Delete groups (clean up taxonomy) | [`clear_store.py`](./clear_store.py) | [group delete](https://learn.microsoft.com/en-us/graph/api/termstore-group-delete) |

---

## API reference

- [Term store](https://learn.microsoft.com/en-us/graph/api/resources/termstore-store)
- [Term](https://learn.microsoft.com/en-us/graph/api/resources/termstore-term)
