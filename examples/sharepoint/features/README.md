# Features

> **⚠️ Classic — custom features are no longer deployed via the Feature Framework.**
> Built-in site/web features are still present and can be activated via REST,
> but custom features are now deployed through SPFx.
> [SPFx overview](https://learn.microsoft.com/en-us/sharepoint/dev/spfx/sharepoint-framework-overview)

Activate, deactivate, and list features on a SharePoint site or web.
Features are identified by a GUID and define bundled functionality.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** role | Required to activate or deactivate features at the site level. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | List — enumerate activated features on a site | [`list_features.py`](./list_features.py) | Read access | [List features](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features) |
| **2** | Activate — activate a feature by ID | [`activate_site.py`](./activate_site.py) | Site Owner | [Activate](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features) |
| **3** | Ensure activated — activate only if not already active | [`ensure_activated.py`](./ensure_activated.py) | Site Owner | [Activate](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features) |
| **4** | Deactivate — remove an activated feature | [`deactivate_feature.py`](./deactivate_feature.py) | Site Owner | [Deactivate](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Activate a feature
f = ctx.site.features.add(
    KnownFeaturesList.ContentTypeHub, False, FeatureDefinitionScope.Farm
).execute_query()
print(f"Activated: {f.display_name}")
```

---

## API reference

- [SharePoint features REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features)