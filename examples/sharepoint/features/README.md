# Working with Features in SharePoint

A **feature** is a set of SharePoint functionality that can be activated
or deactivated at the **site** or **web** level. Features are identified
by a GUID (feature ID) and have a display name and scope.

---

## ⚙️ Activate & Ensure

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Activate a site feature
ctx.web.activate_feature("00bfea71-1c5e-4a24-b310-ba51c3eb7a57").execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Activate a site feature** | [`activate_site.py`](./activate_site.py) | Activate by feature ID |
| **Ensure feature is activated** | [`ensure_activated.py`](./ensure_activated.py) | Activate only if not already active |

---

## Official docs

- [SharePoint features REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
