# SharePoint

The SharePoint REST API (v1) — lists, items, files, folders, search,
permissions, sites, and managed metadata — as minimal, copy-paste examples.

---

## Lists & list items

### [Lists](lists/)

A **list** is a container for rows of data, like a database table.

```python
# Read all lists on the site
all_lists = ctx.web.lists.get().execute_query()
for l in all_lists:
    print(f"  {l.title}  (ID: {l.id})")

# Get a specific list by title
target = ctx.web.lists.get_by_title("Documents").get().execute_query()
print(f"Items: {target.item_count}, Fields: {len(target.fields)}")
```


### [List Items](listitems/)

A **list item** is a single row in a SharePoint list or library.

```python
target_list = ctx.web.lists.get_by_title("Documents")

# Read all items
items = target_list.items.get().execute_query()
for item in items:
    print(f"  {item.id}: {item.properties.get('Title', '')}")

# Create an item
item = target_list.add_item({"Title": "New report"}).execute_query()
print(f"Created: {item.id}")
```


### [Fields](fields/)

Create, read, update, delete, copy, and export fields (columns) in SharePoint.

```python
# List all site columns (web scope)
fields = ctx.web.fields.get().execute_query()
for f in fields:
    print(f"  {f.title}  (Type: {f.properties.get('TypeDisplayName', '')})")

# Create a text field
field = ctx.web.fields.add_text_field("CustomerName").execute_query()
print(f"Created: {field.title}")
```


### [Content Types](contenttypes/)

Manage content types on a SharePoint site — create, update, delete, add and remove fields, reorder fields, and associate with lists.

```python
from office365.sharepoint.contenttypes.creation_information import ContentTypeCreationInformation


# List all content types
cts = ctx.web.content_types.get().execute_query()
for ct in cts:
    print(f"  {ct.name}  (ID: {ct.id})")

# Create a new content type
info = ContentTypeCreationInformation(Name="Project Document", Description="For Contoso projects")
ct = ctx.web.content_types.add(info).execute_query()
print(f"Created: {ct.name}")
```


### [Views](views/)

A **view** defines how a list or library is displayed: which columns to show, the sort order, filters, and grouping.

```python
target_list = ctx.web.lists.get_by_title("Documents")

# Get the default view
default_view = target_list.default_view.get().execute_query()
print(f"Default view: {default_view.title}  (type: {default_view.view_type})")

# List all views
views = target_list.views.get().execute_query()
for v in views:
    print(f"  {v.title}  {'[default]' if v.default_view else ''}")
```


---

## Files & folders

### [Files](files/)

Upload, download, copy, move, delete, share, and manage files in SharePoint document libraries.

```python
# Upload a small file
with open("./report.docx", "rb") as f:
    uploaded = ctx.web.default_document_library().root_folder.upload_file("report.docx", f.read()).execute_query()
print(f"Uploaded: {uploaded.serverRelativeUrl}")

# Download it back
downloaded = uploaded.get_content().execute_query()
print(f"Downloaded: {len(downloaded.content)} bytes")
```


### [Folders](folders/)

Create, copy, move, rename, download, delete, and share folders in SharePoint document libraries.

```python
# Create a folder
folder = ctx.web.folders.add("/sites/team/Shared Documents/Reports").execute_query()
print(f"Created: {folder.serverRelativeUrl}")

# List files inside
files = folder.files.get().execute_query()
for f in files:
    print(f"  {f.name}")
```


### [Recycle Bin](recyclebin/)

List, restore, recycle, and permanently delete items in the SharePoint recycle bin.

```python
# List first-stage recycle bin items
items = ctx.web.recycle_bin.get().execute_query()
for item in items:
    print(f"  {item.title}  (deleted: {item.deleted_date})")

# Restore the most recently deleted item
if len(items):
    items[0].restore().execute_query()
```


### [Compliance](compliance/)

Examples for managing **compliance tags** (retention labels) on SharePoint lists, libraries, and items via the SharePoint CSOM API.


---

## Sites & administration

### [Sites](sites/)

Create, read, update, and delete SharePoint sites (site collections).

```python
# Get site properties
web = ctx.web.get().execute_query()
print(f"{web.title}  {web.url}  ({web.web_template})")
```


### [Tenant](tenant/)

Manage SharePoint tenant settings, sites, admins, sharing, and licensing.

```python
from office365.sharepoint.tenant.administration.tenant import Tenant


tenant = Tenant(ctx)
sites = tenant.get_site_properties_from_sharepoint().execute_query()
for site in sites:
    print(f"  {site.Url}  ({site.Title})")
```


### [Groups](groups/)

Manage SharePoint site groups — create, list, find, set owner, and add or remove members.

```python
# List all site groups
groups = ctx.web.site_groups.get().execute_query()
for g in groups:
    print(f"  {g.title}  (ID: {g.id})")

# Create a group
group = ctx.web.site_groups.add("Project Contributors").execute_query()
```


### [Users](users/)

Manage users in SharePoint: who has access to a site, current user info, tenant-wide search, site groups, and OneDrive details.

```python
# Get current user
me = ctx.web.current_user.get().execute_query()
print(f"Hello, {me.title}  ({me.login_name})")

# List all site users
users = ctx.web.site_users.get().execute_query()
for u in users:
    print(f"  {u.title}  ({u.login_name})")
```


### [Features](features/)

Activate, deactivate, and list features on a SharePoint site or web.

```python
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList


# Activate a feature
f = ctx.site.features.add(
    KnownFeaturesList.ContentTypeHub, False, FeatureDefinitionScope.Farm
).execute_query()
print(f"Activated: {f.display_name}")
```


### [Webs](webs/)

A **web** (also called a site) is a SharePoint container for lists, libraries, and pages.

```python
# Get web properties
web = ctx.web.get().execute_query()
print(f"Title: {web.title}, URL: {web.url}, Template: {web.get_web_template()}")
```


### [Navigation](navigation/)

Manage the site navigation structure — top navigation bar, Quick Launch, and hierarchical menu nodes.

```python
# Read top navigation
nav = ctx.web.navigation.top_navigation_bar.get().execute_query()
for node in nav:
    print(f"  {node.title}  → {node.url}")

# Read Quick Launch
ql = ctx.web.navigation.quick_launch.get().execute_query()
for node in ql:
    print(f"  {node.title}  → {node.url}")
```


### [Pages](pages/)

Create, read, update, publish, and manage modern SharePoint pages.

```python
# List all site pages
pages = ctx.web.site_pages.pages.get().execute_query()
for page in pages:
    print(f"  {page.file_name}  : {page.title}")
```


### [Migration](migration/)

Assess a SharePoint site for migration readiness using the SharePoint Migration API.

```python
from office365.migration.assessor import MigrationAssessor

report = MigrationAssessor(ctx.web).include_permissions().include_versions().assess().execute_query()
print(report.value.summary())
```


---

## More areas

### [Alerts](alerts/)

Examples for managing SharePoint alerts — list, create, and remove alerts on lists and document libraries.


### [Audit](audit/)

Query audit logs from SharePoint sites and Microsoft Graph.

```python
# Read site audit settings
audit = ctx.web.audit.get().execute_query()
print(f"Audit entries trimmed: {audit.audit_log_trimming_retention}")
```


### [Webhooks](webhooks/)

Webhooks let your app receive HTTP callbacks when items change in a SharePoint list.

```python
target_list = ctx.web.lists.get_by_title("Documents")

# Subscribe
sub = target_list.subscriptions.add(
    "https://your-app.azurewebsites.net/webhook/notifications"
).execute_query()
print(f"Subscribed: {sub.id} (expires: {sub.expiration_datetime})")
```


### [Advanced](advanced/)

Configuration, performance, and low-level examples for custom scenarios.


### [App Catalog](app-catalog/)

Manage SharePoint Framework (SPFx) solutions and SharePoint Add-ins through the tenant or site collection app catalog.

```python
# List apps in the app catalog
apps = ctx.web.app_catalog.get().execute_query()
for app in apps:
    print(f"  {app.title}  (ID: {app.id})")
```


### [Custom Actions](customactions/)

Add custom functionality to classic SharePoint pages and lists — inject JavaScript, add toolbar buttons, or extend the ribbon.

```python
# List all custom actions on the site
actions = ctx.web.user_custom_actions.get().execute_query()
for a in actions:
    print(f"  {a.properties.get('Title', '')}  (ID: {a.properties.get('Id', '')})")

# Add a ScriptLink action that injects JavaScript site-wide
ctx.web.user_custom_actions.add(
    title="Custom script",
    location="ScriptLink",
    script_block="console.log('Loaded from custom action');",
).execute_query()
```


### [Event Receivers](eventreceivers/)

Attach custom logic (remote endpoints) to list events — item added, updated, deleted, and more.

```python
# List event receivers on a list
target_list = ctx.web.lists.get_by_title("Documents")
receivers = target_list.event_receivers.get().execute_query()
for r in receivers:
    print(f"  {r.properties.get('ReceiverName', '')}  (ID: {r.properties.get('ReceiverId', '')})")
```


### [Hub Sites](hubsites/)

Manage hub sites — register, associate, enumerate, and set as the intranet landing page.

```python
# List all hub sites
hub_sites = ctx.hub_sites.get().execute_query()
for hub in hub_sites:
    print(f"  {hub.title}  ({hub.site_url})")
```


### [Property Bag](propertybag/)

Store and retrieve custom key-value pairs on a web (site) using the property bag.

```python
web = ctx.web.get().execute_query()
web.set_property("AllProperties", {"Custom_Config": "value"}).update().execute_query()
```


### [Site Designs](sitedesigns/)

**Site designs** bundle one or more **site scripts** into a packaged template that can be applied to new or existing sites.

```python
from office365.sharepoint.sitedesigns.utility import SiteDesignUtility

# List all site designs
designs = SiteDesignUtility.get_site_designs(ctx).execute_query()
for d in designs.value:
    print(f"  {d.Title}  (ID: {d.Id})")

# Apply a design to a site
SiteDesignUtility.apply_site_design(ctx, design_id, site_url).execute_query()
```


### [Site Scripts](sitescripts/)

Create, inspect, and manage SharePoint site scripts — JSON-based provisioning recipes that automate site configuration (themes, lists, settings, etc.).

```python
# List existing site scripts
from office365.sharepoint.sitescripts.utility import SiteScriptUtility

result = SiteScriptUtility.get_site_scripts(ctx).execute_query()
for s in result.value:
    print(f"  {s.Title}  (ID: {s.Id})")

# Create a script that applies a custom theme
site_script = {
    "$schema": "schema.json",
    "actions": [{"verb": "applyTheme", "themeName": "Contoso Theme"}],
    "bindata": {},
    "version": 1,
}
created = SiteScriptUtility.create_site_script(
    ctx, "Theme Script", "Applies Contoso theme", site_script
).execute_query()
print(f"Created: {created.value.Title} (ID: {created.value.Id})")
```


### [Teams (via API)](teams/)

List Microsoft Teams and channels that the current user has access to.

```python
import json
result = ctx.group_site_manager.get_current_user_joined_teams().execute_query()
data = json.loads(result.value)
for team in data["value"]:
    print(f"  {team['displayName']}  (ID: {team['id']})")
```


### [User Profile](userprofile/)

Interact with SharePoint user profiles via the **User Profile Service**: view profile properties, manage followers, explore social features, and access OneDrive URLs.

```python
# Get current user's profile properties
props = ctx.people_manager.get_properties_for(ctx.web.current_user).execute_query()
print(f"Display name: {props.display_name}")
print(f"Department: {props.department}")
print(f"Skills: {props.skills}")

# Get trending tags (note: the API takes the context)
tags = ctx.people_manager.get_trending_tags(ctx).execute_query()
for tag in tags.items:
    print(f"  #{tag.name}  ({tag.count})")
```


---

## [Search](search/)

Use the SharePoint search REST API to find sites, documents, people, and list items across the tenant.

```python
# Search for documents
result = ctx.search.post_query("IsDocument:1", row_limit=10).execute_query()
rows = result.value.PrimaryQueryResult.RelevantResults.Table.Rows
for row in rows:
    print(f"  {row.Cells['Path']}")
```

---

## [Taxonomy](taxonomy/)

SharePoint's managed metadata system for consistent tagging across sites using hierarchical term stores, term groups, term sets, and terms.

```python
from office365.sharepoint.taxonomy.service import TaxonomyService


# Access the term store
tax_service = TaxonomyService(ctx)
store = tax_service.term_stores.get().execute_query()
print(f"Term Store: {store.name}  (default language: {store.default_language})")

# List term groups
for group in store.groups:
    print(f"  Group: {group.name}")
```

---

## [Permissions](permissions/)

Manage who can access what at the site, list, folder, or file level.

```python
from office365.sharepoint.sharing.role_type import RoleType


# Get effective permissions on a list
target_list = ctx.web.default_document_library()
result = target_list.get_user_effective_permissions(ctx.web.current_user).execute_query()
for level in result.value.permission_levels:
    print(f"Permission: {level}")

# Grant a user Contributor access
target_list.add_role_assignment("user@contoso.com", RoleType.Contributor).execute_query()
```

---

## [Sharing](sharing/)

Share files, folders, and sites with specific people, the whole organization, or anonymous users via sharing links and direct permission grants.

```python
# Create an anonymous view link for a file
from office365.sharepoint.sharing.links.kind import SharingLinkKind

file = ctx.web.get_file_by_server_relative_url("Shared Documents/report.docx")
result = file.share_link(SharingLinkKind.AnonymousView).execute_query()
print(f"Share link: {result.value.sharingLinkInfo.Url}")
```

---
