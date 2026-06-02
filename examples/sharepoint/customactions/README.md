# Custom Actions

> **⚠️ Legacy — prefer SPFx Extensions for modern sites.**
> Microsoft recommends migrating from UserCustomAction to SharePoint Framework
> (SPFx) Extensions. These examples target **classic** pages and lists only.
> [Migration guide](https://learn.microsoft.com/en-us/sharepoint/dev/spfx/extensions/guidance/migrate-from-usercustomactions-to-spfx-extensions)

Add custom functionality to classic SharePoint pages and lists — inject
JavaScript, add toolbar buttons, or extend the ribbon.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** role | Required to manage custom actions on a site or list. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

Custom actions can be created at two scopes:
- **Site scope** — ScriptLink injects JavaScript into every page
- **List scope** — adds toolbar buttons or ECB menu items to a specific list

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List — enumerate site and list custom actions | [`list_actions.py`](./list_actions.py) | Read access | [List](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action) |
| **2** | Add script link — inject JavaScript site-wide | [`add_script_link.py`](./add_script_link.py) | Site Owner | [Create](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action) |
| **3** | Add list action — add a toolbar button to a list | [`add_list_action.py`](./add_list_action.py) | Site Owner on target list | [Create](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action) |
| **4** | Remove — delete a custom action by ID | [`remove_action.py`](./remove_action.py) | Site Owner | [Delete](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# List all custom actions on the site
actions = ctx.web.user_custom_actions.get().execute_query()
for a in actions:
    print(f"  {a.properties.get('Title', '')}  (ID: {a.properties.get('Id', '')})")
```

---

## API reference

- [User custom action REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action)
- [Migrate from UserCustomAction to SPFx Extensions](https://learn.microsoft.com/en-us/sharepoint/dev/spfx/extensions/guidance/migrate-from-usercustomactions-to-spfx-extensions)
