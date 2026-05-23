# Tenant Administration

These examples use the **tenant admin** API, which requires a connection
to the **tenant admin site** (`https://contoso-admin.sharepoint.com`)
with app-only or admin credentials.

A `Tenant` object is the entry point for all tenant-level operations.

---

## ⚙️ Configure Tenant Settings

```python
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant

ctx = ClientContext("https://contoso-admin.sharepoint.com").with_client_credentials(
    "your_client_id", "your_client_secret"
)
tenant = Tenant(ctx)
```

| What | File | Notes |
|------|------|-------|
| **Allow custom script** | [`allow_custom_script.py`](./allow_custom_script.py) | Enable / disable custom scripts on sites |
| **Change sharing capability** | [`change_sharing_capability.py`](./change_sharing_capability.py) | External sharing level for the tenant |
| **Enable app-only auth** | [`enable_app_only_authentication.py`](./enable_app_only_authentication.py) | Allow ACS app-only access (legacy) |
| **Is legacy auth enabled** | [`is_legacy_auth_enabled.py`](./is_legacy_auth_enabled.py) | Check if legacy auth protocols are allowed |

## 🔍 Browse & Discover

| What | File | Notes |
|------|------|-------|
| **List all site collections** | [`get_all_sites.py`](./get_all_sites.py) | All sites in the tenant |
| **List my sites** | [`get_my_sites.py`](./get_my_sites.py) | Sites the current user can access |
| **Get a site by URL** | [`get_site.py`](./get_site.py) | Details for a specific site |
| **List home sites** | [`get_home_sites.py`](./get_home_sites.py) | Sites marked as home / root |
| **Sites without a group** | [`sites_without_a_group.py`](./sites_without_a_group.py) | Sites not connected to M365 group |

## 👥 Manage Admins

| What | File | Notes |
|------|------|-------|
| **Get site admin** | [`get_site_admin.py`](./get_site_admin.py) | Who is the site collection admin |
| **Set site admin** | [`set_site_admin.py`](./set_site_admin.py) | Add / remove site admins |

## 🗑️ Delete & Clean Up

| What | File | Notes |
|------|------|-------|
| **Delete sites** | [`delete_sites.py`](./delete_sites.py) | Delete multiple site collections |

## 📋 Reports & Settings

| What | File | Notes |
|------|------|-------|
| **Check licenses** | [`check_licenses.py`](./check_licenses.py) | Verify user license assignments |
| **Export tenant settings** | [`export_tenant_settings.py`](./export_tenant_settings.py) | Dump all settings to a file |
| **Print tenant settings** | [`print_tenant_settings.py`](./print_tenant_settings.py) | Print settings to console |

---

## Official docs

- [SharePoint tenant administration REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
