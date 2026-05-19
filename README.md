
# About
Microsoft 365 & Microsoft Graph library for Python

## Status
[![Downloads](https://pepy.tech/badge/office365-rest-python-client/month)](https://pepy.tech/project/office365-rest-python-client)
[![PyPI](https://img.shields.io/pypi/v/office365-rest-python-client.svg)](https://pypi.python.org/pypi/office365-rest-python-client)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/office365-rest-python-client.svg)](https://pypi.python.org/pypi/office365-rest-python-client/)

> **📌 Python Requirement**: Python 3.8 or newer.

# Installation

```bash
pip install office365-rest-python-client
```

Or with uv:

```bash
uv pip install office365-rest-python-client
```

The latest version from GitHub can be installed directly:

```
pip install git+https://github.com/vgrem/office365-rest-python-client.git
```

# Quick Start

## SharePoint REST API

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://{tenant}.sharepoint.com").with_client_certificate(
    tenant="{tenant}", client_id="{client_id}",
    thumbprint="{thumbprint}", cert_path="./cert.pem",
)
web = ctx.web.get().execute_query()
print(f"Web: {web.title}")
```

## Microsoft Graph API

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="{tenant}").with_client_secret(
    client_id="{client_id}", client_secret="{client_secret}",
)
me = client.me.get().execute_query()
print(f"User: {me.user_principal_name}")
```

---

# Supported APIs

| Client | Capabilities |
|---|---|
| **ClientContext** (SharePoint REST) | Sites, Webs, Lists, ListItems, Files, Folders, Fields, ContentTypes, Permissions, Taxonomy, Search, Tenant Administration, User Profiles |
| **GraphClient** (Microsoft Graph) | Users, Groups, Directory, Outlook (Mail/Calendar/Contacts), OneDrive, Teams, Planner, OneNote, Security, Reports, Booking, Tasks, Intune, Presence, Online Meetings |

---

# Authentication

The library provides two clients: **`ClientContext`** for SharePoint REST API and **`GraphClient`** for Microsoft Graph API.

> **📌 ACS Retirement Notice**: Azure Access Control Service (ACS) for SharePoint
> is being retired. ACS stopped working for **new tenants** on November 1, 2024,
> and will be **fully retired on April 2, 2026**. Use Azure AD-based authentication instead.
> [Learn more](https://aka.ms/retirement/acs/support)

## ClientContext - SharePoint

### Azure AD App-Only (certificate) - RECOMMENDED

```python
ctx = ClientContext('{site_url}').with_client_certificate(tenant, client_id, thumbprint, cert_path)
```

[Docs](https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread) | [Example](examples/sharepoint/auth/modern/with_certificate.py)

### Username & password (MSAL ROPC) - RECOMMENDED for user auth

Uses the OAuth 2.0 Resource Owner Password Credentials grant via MSAL.

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext('{site_url}').with_username_and_password(
    tenant='{tenant}', client_id='{client_id}',
    username='{username}', password='{password}'
)
```

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc) | [Example](examples/sharepoint/auth/modern/with_username_and_password.py)

### Interactive

Opens a browser for user login.

```python
from office365.sharepoint.client_context import ClientContext
ctx = ClientContext('{site_url}').with_interactive('{tenant}', '{client_id}')
```

> Prerequisite: configure Redirect URI as `http://localhost` in Azure Portal.

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/msal-authentication-flows#interactive-and-non-interactive-authentication) | [Example](examples/sharepoint/auth/modern/with_interactive.py)

### Device code

User authenticates on another device via a displayed code.

```python
ctx = ClientContext('{site_url}').with_device_flow('{tenant}', '{client_id}')
```

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code) | [Example](examples/sharepoint/auth/modern/with_device_flow.py)

### Legacy - SAML User Auth ⚠️

> **Deprecated**: `with_user_credentials` uses the legacy SAML-based auth flow
> which is being phased out by Microsoft. Use `with_username_and_password`
> (MSAL ROPC OAuth 2.0) instead.

```python
from office365.sharepoint.client_context import ClientContext
ctx = ClientContext('{site_url}').with_user_credentials('{username}', '{password}')
```

Replaced by:

```python
ctx.with_username_and_password(tenant='{tenant}', client_id='{client_id}', username='{username}', password='{password}')
```

[Docs](https://learn.microsoft.com/en-us/microsoft-365/enterprise/modern-auth-for-office-2013-and-2016)

### Legacy - ACS App-Only ⚠️

> **Deprecated**: Azure ACS is being retired. Use Azure AD certificate auth instead.

```python
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
ctx = ClientContext('{site_url}').with_credentials(ClientCredential('{client_id}', '{client_secret}'))
```

[Docs](https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs) | [Example](examples/sharepoint/auth/legacy/with_app_only.py)

---

## GraphClient - Microsoft Graph

### Client secret

Uses the OAuth 2.0 Client Credentials grant via MSAL.

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}').with_client_secret(client_id='{client_id}', client_secret='{client_secret}')
```

[Docs](https://learn.microsoft.com/en-us/graph/auth-v2-service) | [Example](examples/auth/with_client_secret.py)

### Certificate

```python
client = GraphClient(tenant='{tenant}').with_client_certificate(client_id, thumbprint, private_key)
```

[Docs](https://learn.microsoft.com/en-us/graph/auth-v2-service) | [Example](examples/auth/with_client_secret.py)

### Interactive

Opens a browser for user login.

```python
client = GraphClient(tenant='{tenant}').with_token_interactive(client_id='{client_id}')
```

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/msal-authentication-flows#interactive-and-non-interactive-authentication)

### Username & password (MSAL ROPC)

```python
client = GraphClient(tenant='{tenant}').with_username_and_password('{client_id}', '{username}', '{password}')
```

[Docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc)

### Custom token acquisition

Any OAuth2-compliant library (MSAL, ADAL, etc.):

```python
def acquire_token():
    # your token acquisition logic
    return token

client = GraphClient(acquire_token)
```

---

# ClientContext - SharePoint API

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

site_url = "https://{tenant}.sharepoint.com"
ctx = ClientContext(site_url).with_username_and_password(
    tenant="{tenant}", client_id="{client_id}",
    username="{username}", password="{password}",
)
web = ctx.web.get().execute_query()
print(f"Web title: {web.title}")
```

## Azure environments

Add the `environment` parameter for non-global clouds:

```python
from office365.azure_env import AzureEnvironment
ctx = ClientContext('{site_url}', environment=AzureEnvironment.USGovernmentHigh).with_credentials(...)
```

## Examples

For a comprehensive list, see the [SharePoint examples guide](examples/sharepoint/README.md).

---

# GraphClient — Microsoft Graph API

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant='{tenant}').with_client_secret(client_id='{client_id}', client_secret='{client_secret}')
me = client.me.get().execute_query()
print(f"User: {me.user_principal_name}")
```

## Outlook

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}').with_client_secret(client_id='{client_id}', client_secret='{client_secret}')
client.me.send_mail(
    subject="Meet for lunch?",
    body="The new cafeteria is open.",
    to_recipients=["user@contoso.onmicrosoft.com"]
).execute_query()
```

[Send email](examples/outlook/messages/send.py) | [List messages](examples/outlook/messages/list_all.py) | [Download](examples/outlook/messages/download.py) | [Search](examples/outlook/messages/search.py)

More [Outlook examples](examples/outlook/README.md).

## OneDrive

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}')
drives = client.drives.get().execute_query()
for drive in drives:
    print(f"Drive url: {drive.web_url}")
```

[Download files](examples/onedrive/files/download.py) | [Upload files](examples/onedrive/folders/upload.py) | [List drives](examples/onedrive/drives/list.py)

More [OneDrive examples](examples/onedrive/README.md).

## Teams

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}')
new_team = client.groups["{group_id}"].add_team().execute_query()
```

[Create a team](examples/teams/create_team.py) | [List teams](examples/teams/list_all.py) | [Send messages](examples/teams/send_message.py)

More [Teams examples](examples/teams/README.md).

## OneNote

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}')
with open("./MyPage.html", 'rb') as f:
    page = client.me.onenote.pages.add(presentation_file=f).execute_query()
```

## Planner

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}')
task = client.planner.tasks.add(title="New task", planId="--plan-id--").execute_query()
```

---

# Third Party Libraries

The following libraries will be installed when you install the client library:

- [requests](https://github.com/kennethreitz/requests)
- [Microsoft Authentication Library (MSAL) for Python](https://pypi.org/project/msal/)
