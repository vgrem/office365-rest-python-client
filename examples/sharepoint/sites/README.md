# Site Collections

Create, read, update, and delete SharePoint site collections.

## ✏️ Create

| What | PnP equivalent | File | Notes |
|------|---------------|------|-------|
| **Team site** (modern) | `New-PnPSite -Type Team` | [`create_team.py`](./create_team.py) | Microsoft 365 group-connected |
| **Communication site** (modern) | `New-PnPSite -Type Communication` | [`create_comm.py`](./create_comm.py) | Modern publishing site |
| **Classic site** | `New-PnPSite` | [`create_classic.py`](./create_classic.py) | Not group-connected |

## 🔍 Read

| What | PnP equivalent | File | Notes |
|------|---------------|------|-------|
| **Get properties** | `Get-PnPSite` | [`get_basic_props.py`](./get_basic_props.py) | Title, URL, template |
| **Get admins** | `Get-PnPSiteCollectionAdmin` | [`get_admins.py`](./get_admins.py) | Site collection administrators |
| **Get personal site** | `Get-PnPPersonalSite` | [`get_my_site.py`](./get_my_site.py) | OneDrive for current user |

## ✏️ Update

| What | PnP equivalent | File | Notes |
|------|---------------|------|-------|
| **Set properties** | `Set-PnPSite` | [`set_site_props.py`](./set_site_props.py) | Update title, description |
| **Add admin** | `Add-PnPSiteCollectionAdmin` | [`add_admin.py`](./add_admin.py) | Grant admin access |
| **Remove admin** | `Remove-PnPSiteCollectionAdmin` | [`remove_admin.py`](./remove_admin.py) | Revoke admin access |

## 🗑️ Delete

| What | PnP equivalent | File | Notes |
|------|---------------|------|-------|
| **Delete site** | `Remove-PnPSite` | [`delete_site.py`](./delete_site.py) | Remove site collection |

---

## Official docs

- [SharePoint site REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations)
- [Modern site creation REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest)
