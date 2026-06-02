# Navigation

Manage the site navigation structure — top navigation bar, Quick Launch,
and hierarchical menu nodes.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** or **Designer** role | Required to add, update, or delete navigation nodes. Read access for browsing. | [SharePoint permissions](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Getting started

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Read top navigation
nav = ctx.web.navigation.top_navigation_bar.get().execute_query()
for node in nav:
    print(f"  {node.title}  → {node.url}")

# Read Quick Launch
ql = ctx.web.navigation.quick_launch.get().execute_query()
for node in ql:
    print(f"  {node.title}  → {node.url}")
```

---

## Read

| What | File | Notes |
|------|------|-------|
| **Top navigation bar** | [`list_top_nav.py`](./list_top_nav.py) | All nodes in the top nav |
| **Quick Launch** | [`list_quick_launch.py`](./list_quick_launch.py) | All nodes in the Quick Launch |

## Create

| What | File | Notes |
|------|------|-------|
| **Add node** | [`add_node.py`](./add_node.py) | Add a top-level node to Quick Launch or top nav |
| **Add child node** | [`add_child_node.py`](./add_child_node.py) | Add a sub-menu under an existing node |

## Update & Delete

| What | File | Notes |
|------|------|-------|
| **Update node** | [`update_node.py`](./update_node.py) | Rename or change URL |
| **Delete node** | [`delete_node.py`](./delete_node.py) | Remove a node by ID |

---

## API reference

- [SharePoint navigation API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference)
