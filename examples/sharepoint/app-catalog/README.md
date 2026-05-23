# App Catalog (ALM)

Manage the lifecycle of SharePoint Framework (SPFx) solutions and SharePoint
Add-ins through the tenant or site collection app catalog.

All operations target the **tenant app catalog** (`admin.web.tenant_app_catalog`).
Install/uninstall also affect a **target site**.

| What | File | Notes |
|------|------|-------|
| **Upload** | [`upload_app.py`](./upload_app.py) | Add `.sppkg` to the app catalog |
| **List** | [`list_apps.py`](./list_apps.py) | Enumerate apps in the catalog |
| **Inspect** | [`inspect_app.py`](./inspect_app.py) | Get app metadata and upgrade info |
| **Deploy** | [`deploy_app.py`](./deploy_app.py) | Enable an app for installation |
| **Install** | [`install_app.py`](./install_app.py) | Install app on a target site |
| **Upgrade** | [`upgrade_app.py`](./upgrade_app.py) | Deploy + install newer version |
| **Uninstall** | [`uninstall_app.py`](./uninstall_app.py) | Remove app from a target site |
| **Remove** | [`remove_app.py`](./remove_app.py) | Delete app from the catalog |

---

## Official docs

- [ALM API for SPFx add-ins](https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins)
