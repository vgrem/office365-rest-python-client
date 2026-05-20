# office365-rest-python-client

[![Downloads](https://pepy.tech/badge/office365-rest-python-client/month)](https://pepy.tech/project/office365-rest-python-client)
[![PyPI](https://img.shields.io/pypi/v/office365-rest-python-client.svg)](https://pypi.python.org/pypi/office365-rest-python-client)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/office365-rest-python-client.svg)](https://pypi.python.org/pypi/office365-rest-python-client/)

**Python client library for Microsoft 365 and Microsoft Graph APIs.**

Covers SharePoint REST API v1, Microsoft Graph (Outlook, OneDrive, Teams, OneNote, Planner, and more), and supports all modern Azure AD authentication flows.

> **Python 3.8+ required.**

---

## Table of Contents

- [Installation](#installation)
- [Which client do I need?](#which-client-do-i-need)
- [Authentication](#authentication)
  - [ClientContext — SharePoint](#clientcontext--sharepoint-auth)
  - [GraphClient — Microsoft Graph](#graphclient--microsoft-graph-auth)
  - [Azure Environments (national clouds)](#azure-environments)
- [SharePoint — ClientContext](#sharepoint--clientcontext)
- [Microsoft Graph — GraphClient](#microsoft-graph--graphclient)
- [Dependencies](#dependencies)

---

## Installation

```bash
pip install office365-rest-python-client
```

With [uv](https://github.com/astral-sh/uv):

```bash
uv pip install office365-rest-python-client
```

Latest from GitHub (includes unreleased changes):

```bash
pip install git+https://github.com/vgrem/office365-rest-python-client.git
```

---

## Which client do I need?

| | `ClientContext` | `GraphClient` |
|---|---|---|
| **Target API** | SharePoint REST API v1 | Microsoft Graph API |
| **Use for** | SharePoint lists, files, folders, search, site admin, permissions | Outlook, OneDrive, Teams, OneNote, Planner, Users, Groups |
| **SharePoint via Graph?** | — | Partial — use `ClientContext` for full SharePoint fidelity |
| **Docs** | [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service) | [Microsoft Graph](https://learn.microsoft.com/en-us/graph/overview) |

---

## Authentication

> ⚠️ **ACS Retirement:** Azure Access Control Service (ACS) app-only auth is fully retired as of April 2026. `UserCredential` (SAML/IDCRL) is retired as of May 1, 2026. Both have been removed from the library. Migrate to Azure AD auth. [Learn more](https://aka.ms/retirement/acs/support)

---

### ClientContext — SharePoint Auth

#### App-only: Certificate (recommended for automation)

No user interaction. Ideal for scripts, pipelines, and services.

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("{site_url}").with_client_certificate(
    tenant="{tenant}",           # e.g. contoso.onmicrosoft.com
    client_id="{client_id}",
    thumbprint="{thumbprint}",
    cert_path="/path/to/cert.pem"
)
```

[Setup guide](https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread) | [Example](examples/sharepoint/auth/modern/with_certificate.py)

#### App-only: Client secret

```python
ctx = ClientContext("{site_url}").with_client_secret(
    tenant="{tenant}",
    client_id="{client_id}",
    client_secret="{client_secret}"
)
```

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow) | [Example](examples/sharepoint/auth/modern/with_client_secret.py)

#### User auth: Username & password (MSAL ROPC)

Non-interactive user auth. Requires no MFA on the account.

```python
ctx = ClientContext("{site_url}").with_username_and_password(
    tenant="{tenant}",
    client_id="{client_id}",
    username="{username}",
    password="{password}"
)
```

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc) | [Example](examples/sharepoint/auth/modern/with_username_and_password.py)

#### User auth: Interactive (MFA-compatible)

Opens a browser. Works with MFA and Conditional Access.

```python
ctx = ClientContext("{site_url}").with_interactive(
    tenant="{tenant}",
    client_id="{client_id}"
)
```

> Prerequisite: add `http://localhost` as a Redirect URI in your Azure app registration.

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/msal-authentication-flows#interactive-and-non-interactive-authentication) | [Example](examples/sharepoint/auth/modern/with_interactive.py)

#### User auth: Device code

Authenticate on another device via a displayed code. Useful for headless environments.

```python
ctx = ClientContext("{site_url}").with_device_flow(
    tenant="{tenant}",
    client_id="{client_id}"
)
```

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code) | [Example](examples/sharepoint/auth/modern/with_device_flow.py)

#### On-premise: NTLM

For SharePoint Server (2016, 2019, Subscription Edition). Requires `pip install office365-rest-python-client[ntlm]`.

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("http://sharepoint.company.com/sites/project", allow_ntlm=True).with_user_credentials(
    username="DOMAIN\\username",
    password="password"
)
```

[Example](examples/sharepoint/auth/legacy/with_ntlm.py)

---

### GraphClient — Microsoft Graph Auth

#### Client secret

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="{tenant}").with_client_secret(
    client_id="{client_id}",
    client_secret="{client_secret}"
)
```

[Docs](https://learn.microsoft.com/en-us/graph/auth-v2-service) | [Example](examples/auth/with_client_secret.py)

#### Certificate

```python
client = GraphClient(tenant="{tenant}").with_client_certificate(
    client_id="{client_id}",
    thumbprint="{thumbprint}",
    private_key="{private_key}"
)
```

[Docs](https://learn.microsoft.com/en-us/graph/auth-v2-service) | [Example](examples/auth/with_certificate.py)

#### Interactive (MFA-compatible)

```python
client = GraphClient(tenant="{tenant}").with_token_interactive(
    client_id="{client_id}"
)
```

#### Username & password (MSAL ROPC)

```python
client = GraphClient(tenant="{tenant}").with_username_and_password(
    client_id="{client_id}",
    username="{username}",
    password="{password}"
)
```

#### Custom token acquisition

Bring your own MSAL or any OAuth 2.0-compliant token provider:

```python
import msal

def acquire_token():
    app = msal.ConfidentialClientApplication(
        client_id, authority=f"https://login.microsoftonline.com/{tenant}",
        client_credential=client_secret
    )
    return app.acquire_token_for_client(["https://graph.microsoft.com/.default"])

client = GraphClient(acquire_token)
```

---

### Azure Environments

For national and sovereign clouds, pass the `environment` parameter:

```python
from office365.azure_env import AzureEnvironment
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("{site_url}", environment=AzureEnvironment.USGovernmentHigh)\
    .with_client_certificate(...)
```

| Environment | Constant |
|---|---|
| Global (default) | `AzureEnvironment.Global` |
| US Government GCC | `AzureEnvironment.USGovernment` |
| US Government GCC High | `AzureEnvironment.USGovernmentHigh` |
| US Government DoD | `AzureEnvironment.USGovernmentDoD` |
| China (21Vianet) | `AzureEnvironment.China` |
| Germany (legacy) | `AzureEnvironment.Germany` |

---

## SharePoint — ClientContext

### Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("{site_url}").with_client_certificate(
    tenant="{tenant}", client_id="{client_id}",
    thumbprint="{thumbprint}", cert_path="./cert.pem"
)
web = ctx.web.get().execute_query()
print(f"Site title: {web.title}")
```

### Lists & Items

```python
# Get all items (handles 5000+ row threshold automatically)
items = ctx.web.lists.get_by_title("Orders").items.get_all().execute_query()
for item in items:
    print(item.properties["Title"])

# Create item
target_list = ctx.web.lists.get_by_title("Tasks")
item = target_list.add_item({"Title": "New task", "Status": "Active"}).execute_query()

# Bulk create — auto-batches in chunks of 100
for row in data:
    target_list.add_item({"Title": row["name"]})
ctx.execute_batch()

# Filter, select, expand
items = ctx.web.lists.get_by_title("Projects")\
    .items\
    .filter("Status eq 'Active'")\
    .select(["Title", "Author/Title"])\
    .expand(["Author"])\
    .get_all().execute_query()
```

[All list examples](examples/sharepoint/lists/)

### Files & Folders

```python
# Upload file
with open("report.pdf", "rb") as f:
    folder = ctx.web.get_folder_by_server_relative_url("/sites/mysite/Shared Documents")
    file = folder.upload_file("report.pdf", f).execute_query()

# Download file
with open("report.pdf", "wb") as f:
    ctx.web.get_file_by_server_relative_path("/sites/mysite/Shared Documents/report.pdf")\
        .download(f).execute_query()

# Large file upload (chunked)
folder.files.create_upload_session(
    local_path, chunk_size=10*1024*1024,
    chunk_uploaded=lambda offset: print(f"{offset} bytes uploaded")
).execute_query()

# Download folder as zip
with open("archive.zip", "wb") as f:
    folder.download_folder(f).execute_query()

# Create nested folders
base = ctx.web.get_folder_by_server_relative_url("/sites/mysite/Shared Documents")
sub = base.add("Projects").execute_query()
sub.add("2025").execute_query()
```

[All file examples](examples/sharepoint/files/) | [All folder examples](examples/sharepoint/folders/)

### Search

```python
from office365.sharepoint.search.request import SearchRequest
from office365.sharepoint.search.service import SearchService

search = SearchService(ctx)
request = SearchRequest("IsDocument:1", RowLimit=50, StartRow=0)
result = search.post_query(request).execute_query()

rows = result.value.PrimaryQueryResult.RelevantResults.Table.Rows
for row in rows:
    print(row)
```

[All search examples](examples/sharepoint/search/)

### Permissions

```python
from office365.sharepoint.roles.type import RoleType

# Break inheritance and grant access to a user
role_def = ctx.web.role_definitions.get_by_type(RoleType.Reader)
user = ctx.web.ensure_user("i:0#.f|membership|user@company.com")
item = ctx.web.lists.get_by_title("Confidential").items.get_by_id(1)
item.break_role_inheritance(copy_role_assignments=False)
item.add_role_assignment(user, role_def)
ctx.execute_query()
```

[Permissions examples](examples/sharepoint/permissions/)

### Site Administration (Tenant)

```python
from office365.sharepoint.tenant.administration.tenant import Tenant

tenant = Tenant(ctx)

# List all sites
sites = tenant.get_site_properties_from_sharepoint_by_filters().execute_query()
for site in sites:
    print(site.url)

# Create a site
tenant.create_site({"Url": "https://tenant.sharepoint.com/sites/newsite", "Title": "New Site"}).execute_query()
```

[All tenant/admin examples](examples/sharepoint/tenant/)

---

## Microsoft Graph — GraphClient

### Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="{tenant}").with_client_secret(
    client_id="{client_id}", client_secret="{client_secret}"
)
me = client.me.get().execute_query()
print(f"Signed in as: {me.user_principal_name}")
```

### Outlook — Mail & Calendar

```python
# Send email
client.me.send_mail(
    subject="Hello",
    body="Message body",
    to_recipients=["user@company.com"]
).execute_query()

# List messages
messages = client.me.messages.top(10).get().execute_query()
for msg in messages:
    print(msg.subject)

# Create calendar event
from office365.outlook.calendar.events.event import Event
event = client.me.calendar.events.add(
    subject="Team standup",
    start="2025-06-01T09:00:00",
    end="2025-06-01T09:30:00"
).execute_query()
```

[All Outlook examples](examples/outlook/)

### OneDrive

```python
# List drives
drives = client.drives.get().execute_query()

# Upload file to OneDrive
with open("report.xlsx", "rb") as f:
    client.me.drive.root.upload("report.xlsx", f).execute_query()

# Download file
with open("report.xlsx", "wb") as local_file:
    client.me.drive.root.get_by_path("Documents/report.xlsx")\
        .download(local_file).execute_query()
```

[All OneDrive examples](examples/onedrive/)

### Teams

```python
# List all teams
teams = client.groups.get().execute_query()

# Send channel message
client.teams["{team_id}"].channels["{channel_id}"]\
    .messages.add(body="Hello team!").execute_query()

# Create a team
new_team = client.groups["{group_id}"].add_team().execute_query()
```

[All Teams examples](examples/teams/)

### OneNote

```python
# Create a page
with open("MyPage.html", "rb") as f:
    page = client.me.onenote.pages.add(presentation_file=f).execute_query()
```

[All OneNote examples](examples/onenote/)

### Planner

```python
# Create a task
task = client.planner.tasks.add(
    title="Review PR",
    planId="{plan_id}"
).execute_query()
```

[All Planner examples](examples/planner/)

### Users & Groups

```python
# List users
users = client.users.top(100).get().execute_query()

# Create group
group = client.groups.add(
    display_name="Engineering",
    mail_nickname="engineering",
    mail_enabled=False,
    security_enabled=True
).execute_query()
```

[All user examples](examples/directory/)

---

## Dependencies

Installed automatically:

| Package | Purpose |
|---|---|
| [requests](https://github.com/psf/requests) | HTTP transport |
| [msal](https://github.com/AzureAD/microsoft-authentication-library-for-python) | Azure AD authentication |

Optional:

```bash
pip install office365-rest-python-client[pandas]   # to_dataframe() on collections
```

---

## Contributing

PRs welcome. See [issues](https://github.com/vgrem/office365-rest-python-client/issues) for things to work on.

## Links

- [PyPI](https://pypi.org/project/office365-rest-python-client/)
- [Changelog](CHANGELOG.md)
- [SharePoint REST API docs](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service)
- [Microsoft Graph docs](https://learn.microsoft.com/en-us/graph/overview)
- [MSAL for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python)
