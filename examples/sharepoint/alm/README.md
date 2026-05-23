# Application Lifecycle Management (ALM) API

ALM APIs provide simple APIs to manage deployment of your SharePoint Framework
solutions and add-ins across your tenant. Supported operations:

1. **Upload**     — Add SharePoint Framework solution or SharePoint Add-in to
                   tenant or site collection app catalog.
                   → `catalog.app_from_path("app.sppkg", True)`

2. **List**       — List all and get details about SharePoint Framework solutions
                   or SharePoint Add-ins in the tenant or site collection app catalog.
                   → `catalog.available_apps.get()`

3. **Inspect**    — Get metadata and check upgrade availability for a specific app.
                   → `catalog.get_by_title("App")` + `catalog.is_app_upgrade_available(id)`

4. **Deploy**     — Enable SharePoint Framework solution or SharePoint Add-in to be
                   available for installation in tenant or site collection app catalog.
                   → `app.deploy(skip_feature_deployment=False)`

5. **Install**    — Install SharePoint Framework solution or SharePoint Add-in from
                   tenant or site collection app catalog to a site.
                   → `app.install()`

6. **Upgrade**    — Upgrade SharePoint Framework solution or SharePoint Add-in to a
                   site, which has a newer version available in the tenant or site
                   collection app catalog.
                   → `app.deploy()` then `app.install()`

7. **Uninstall**  — Uninstall SharePoint Framework solution or SharePoint Add-in
                   from the site.
                   → `app.uninstall()`

8. **Remove**     — Remove SharePoint Framework solution or SharePoint Add-in from
                   tenant or site collection app catalog.
                   → `app.remove()`

## Example

[common.py](common.py) — walks through all 8 operations end-to-end with app-only.

## Getting started

```python
from office365.sharepoint.client_context import ClientContext

admin = ClientContext("https://tenant-admin.sharepoint.com").with_client_credentials(
    client_id="xxx", client_secret="xxx"
)
catalog = admin.web.tenant_app_catalog  # app catalog entry point
app = catalog.available_apps.get_by_title("My App").execute_query()
```

## Official docs

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
