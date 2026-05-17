
# About
Microsoft 365 & Microsoft Graph library for Python

## Status
[![Downloads](https://pepy.tech/badge/office365-rest-python-client/month)](https://pepy.tech/project/office365-rest-python-client)
[![PyPI](https://img.shields.io/pypi/v/office365-rest-python-client.svg)](https://pypi.python.org/pypi/office365-rest-python-client)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/office365-rest-python-client.svg)](https://pypi.python.org/pypi/office365-rest-python-client/)

> **📌 Python Requirement**: Python 3.8 or newer.

# Installation

```
pip install office365-rest-python-client
```

Or the latest version from GitHub:

```
pip install git+https://github.com/vgrem/office365-rest-python-client.git
```

---

# Authentication

The library provides two clients: **`ClientContext`** for SharePoint REST API and **`GraphClient`** for Microsoft Graph API.

## ClientContext — SharePoint

### App-Only (client credentials)

Compatible with SharePoint on-premises and Online.

```python
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
ctx = ClientContext('{site_url}').with_credentials(ClientCredential('{client_id}', '{client_secret}'))
```

[Docs](https://docs.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs) | [Example](examples/sharepoint/auth/with_app_only.py)

### Username & password

```python
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
ctx = ClientContext('{site_url}').with_credentials(UserCredential('{username}', '{password}'))
```

[Example](examples/sharepoint/auth/with_user_credential.py)

### Certificate credentials

```python
ctx = ClientContext('{site_url}').with_client_certificate(tenant, client_id, thumbprint, cert_path)
```

[Docs](https://docs.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread) | [Example](examples/sharepoint/auth/with_certificate.py)

### Interactive

```python
from office365.sharepoint.client_context import ClientContext
ctx = ClientContext('{site_url}').with_interactive('{tenant}', '{client_id}')
```

> Prerequisite: configure Redirect URI as `http://localhost` in Azure Portal.

[Example](examples/sharepoint/auth/with_interactive.py)

## GraphClient — Microsoft Graph

### Client secret

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}').with_client_secret(client_id='{client_id}', client_secret='{client_secret}')
```

[Example](examples/auth/with_client_secret.py)

### Certificate

```python
client = GraphClient(tenant='{tenant}').with_client_certificate(client_id, thumbprint, cert_path)
```

### Username & password

```python
client = GraphClient(tenant='{tenant}').with_username_and_password('{client_id}', '{username}', '{password}')
```

### Custom token acquisition

Any OAuth2-compliant library (MSAL, ADAL, etc.):

```python
def acquire_token():
    # your token acquisition logic, e.g. via msal
    return token

client = GraphClient(acquire_token)
```

---

# ClientContext — SharePoint API

## Quick start

```python
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

site_url = "https://{tenant}.sharepoint.com"
ctx = ClientContext(site_url).with_credentials(UserCredential("{username}", "{password}"))
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

More [Outlook examples](examples/outlook/).

## OneDrive

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}')
drives = client.drives.get().execute_query()
for drive in drives:
    print(f"Drive url: {drive.web_url}")
```

[Download files](examples/onedrive/files/download.py) | [Upload files](examples/onedrive/folders/upload.py) | [List drives](examples/onedrive/drives/list.py)

More [OneDrive examples](examples/onedrive/).

## Teams

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant}')
new_team = client.groups["{group_id}"].add_team().execute_query()
```

[Create a team](examples/teams/create_team.py) | [List teams](examples/teams/list_all.py) | [Send messages](examples/teams/send_message.py)

More [Teams examples](examples/teams/).

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
