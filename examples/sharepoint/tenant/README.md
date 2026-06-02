# Tenant Administration

Manage SharePoint tenant settings, sites, admins, sharing, and licensing.
These examples use the **tenant admin** API via the **tenant admin site**
(`https://contoso-admin.sharepoint.com`).

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **SharePoint Administrator** or **Global Administrator** role | Required for all tenant-level operations. Connection to the tenant admin site (`-admin.sharepoint.com`). | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

A `Tenant` object is the entry point for all tenant-level operations.

---

## Examples

### Configure settings

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **1** | Allow or block custom script on sites | [`allow_custom_script.py`](./allow_custom_script.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **2** | Change tenant sharing capability | [`change_sharing_capability.py`](./change_sharing_capability.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **3** | Enable app-only authentication (legacy) | [`enable_app_only_authentication.py`](./enable_app_only_authentication.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **4** | Check if legacy auth is enabled | [`is_legacy_auth_enabled.py`](./is_legacy_auth_enabled.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

### Browse and discover

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **5** | List all site collections | [`get_all_sites.py`](./get_all_sites.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **6** | List my sites | [`get_my_sites.py`](./get_my_sites.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **7** | Get a site by URL | [`get_site.py`](./get_site.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **8** | List home sites | [`get_home_sites.py`](./get_home_sites.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **9** | Find sites without a Microsoft 365 group | [`sites_without_a_group.py`](./sites_without_a_group.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

### Manage admins

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **10** | Get site collection admin | [`get_site_admin.py`](./get_site_admin.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **11** | Set site collection admin | [`set_site_admin.py`](./set_site_admin.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **12** | Delete site collections | [`delete_sites.py`](./delete_sites.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

### Reports and settings

| Step | Operation | File | Required role | API reference |
|---|---|---|---|---|
| **13** | Check user license assignments | [`check_licenses.py`](./check_licenses.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **14** | Export all tenant settings to file | [`export_tenant_settings.py`](./export_tenant_settings.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |
| **15** | Print tenant settings | [`print_tenant_settings.py`](./print_tenant_settings.py) | SharePoint Admin | [Tenant REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api) |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant

ctx = ClientContext("https://contoso-admin.sharepoint.com").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

tenant = Tenant(ctx)
sites = tenant.get_site_properties_from_sharepoint().execute_query()
for site in sites:
    print(f"  {site.Url}  ({site.Title})")
```

---

## API reference

- [SharePoint tenant administration REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
