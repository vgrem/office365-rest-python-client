# Working with Sites in SharePoint

A **site** is a SharePoint web container — a team site, communication site,
or classic site. Each site has a **URL**, a **title**, and a unique **ID**.
Sites are managed via the `Site` and `Web` objects.

This page groups examples by **what you want to do** — not by API endpoint.

---

## 🏗️ Create Sites

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso-admin.sharepoint.com").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Create a modern team site
site = ctx.create_team_site("mysite", "My Team Site").execute_query()

# Create a modern communication site
site = ctx.create_communication_site("mysite", "My Comm Site").execute_query()

# Create a classic site collection
from office365.sharepoint.tenant.administration.tenant import Tenant
tenant = Tenant.from_url("https://contoso-admin.sharepoint.com").with_client_credentials(
    "your_client_id", "your_client_secret"
)
tenant.create_site_sync("https://contoso.sharepoint.com/sites/classic", "Classic Site").execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Create team site** (modern) | [`create_team.py`](./create_team.py) | Microsoft 365 group-connected |
| **Create comm. site** (modern) | [`create_comm.py`](./create_comm.py) | Communication site |
| **Create comm. site with owner** | [`create_comm_site_with_owner.py`](./create_comm_site_with_owner.py) | Specify site owner |
| **Create classic site** | [`create_classic.py`](./create_classic.py) | Classic site collection |

## 🔍 Get Site Info

```python
# Get basic properties
props = ctx.web.get().execute_query()
print(props.title, props.url)

# Get site status
status = ctx.tenant.get_site_status("https://contoso.sharepoint.com/sites/mysite").execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Get basic properties** | [`get_basic_props.py`](./get_basic_props.py) | Title, URL, ID, owner |
| **Get site status** | [`get_status.py`](./get_status.py) | Whether the site is created / ready |
| **Get my personal site** | [`get_my_site.py`](./get_my_site.py) | OneDrive for Business URL |
| **Get site admins** | [`get_admins.py`](./get_admins.py) | List site collection admins |

## 🖼️ Branding

| What | File | Notes |
|------|------|-------|
| **Download site logo** | [`download_logo.py`](./download_logo.py) | Save the current logo |

## 🔐 App Access

| File | What it does |
|------|-------------|
| [`grant_app_access.py`](./grant_app_access.py) | Grant app principal access to a site |

---

## Official docs

- [SharePoint site creation REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest)
