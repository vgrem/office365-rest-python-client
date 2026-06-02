# Property Bag

Store and retrieve custom key-value pairs on a web (site) using
the property bag.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** role | Required to set property bag values. Read access to view. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Get property bag values | [`get_properties.py`](./get_properties.py) | Read access | [Property bag REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **2** | Set property bag value | [`set_properties.py`](./set_properties.py) | Site Owner | [Property bag REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

web = ctx.web.get().execute_query()
web.set_property("AllProperties", {"Custom_Config": "value"}).update().execute_query()
```

---

## API reference

- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
