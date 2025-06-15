
# About
Microsoft 365 & Microsoft Graph library for Python

# Usage

1. [Installation](#Installation)
2. [Working with SharePoint API](#Working-with-SharePoint-API) 
3. [Working with Outlook API](#Working-with-Outlook-API) 
4. [Working with OneDrive and SharePoint API v2 APIs](#working-with-onedrive-and-sharepoint-v2-apis)
5. [Working with Teams API](#Working-with-Microsoft-Teams-API)
6. [Working with OneNote API](#Working-with-Microsoft-OneNote-API)
7. [Working with Planner API](#Working-with-Microsoft-Planner-API)  

## Status
[![Downloads](https://pepy.tech/badge/office365-rest-python-client/month)](https://pepy.tech/project/office365-rest-python-client)
[![PyPI](https://img.shields.io/pypi/v/office365-rest-python-client.svg)](https://pypi.python.org/pypi/office365-rest-python-client)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/office365-rest-python-client.svg)](https://pypi.python.org/pypi/office365-rest-python-client/)
[![Build Status](https://travis-ci.com/vgrem/office365-rest-python-client.svg?branch=master)](https://travis-ci.com/vgrem/office365-rest-python-client)


> **📌 Python Requirement**: This package requires Python 3.6 or newer.

# Installation

Use pip:

```
# For Python 3.6+ (current version)
pip install office365-rest-python-client

# For Python 2.7 (legacy)
pip install "office365-rest-python-client<3.0.0"
```

### Note 
>
>Alternatively the _latest_ version could be directly installed via GitHub:
>```
>pip install git+https://github.com/vgrem/office365-rest-python-client.git
>```

# Authentication
For the following examples, relevant credentials can be found in the Azure Portal.

Steps to access:
1. Login to the home page of the Azure Portal
2. Navigate to "Azure Active Directory" using the three bars in the top right corner of the portal
3. Select "App registrations" in the navigation panel on the left
4. Search for and select your relevant application
5. In the application's "Overview" page, the client id can be found under "Application (client) id"
6. In the application's "Certificates & Secrets" page, the client secret can be found under the "Value" of the "Client Secrets." If there is no client secret yet, create one here.


# Working with SharePoint API

   The `ClientContext` client provides the support for a legacy SharePoint REST and OneDrive for Business REST APIs, 
   the list of supported versions: 
   -   [SharePoint 2013 REST API](https://msdn.microsoft.com/en-us/library/office/jj860569.aspx) and above 
   -   [SharePoint Online REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service)
   -   OneDrive for Business REST API

### Authentication

   The following auth flows are supported:

#### 1. Using a SharePoint App-Only principal (client credentials flow)

   This auth method is compatible with SharePoint on-premises and still relevant 
   model in both SharePoint on-premises as SharePoint Online, 
   the following methods are available: 

   - `ClientContext.with_credentials(client_credentials)` 
   - `ClientContext.with_client_credentials(client_id, client_secret)`
  
   Usage:
   ``` 
   client_credentials = ClientCredential('{client_id}','{client_secret}')
   ctx = ClientContext('{url}').with_credentials(client_credentials)
   ```
  
   Documentation:
   - [Granting access using SharePoint App-Only](https://docs.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs)  
   - [wiki](https://github.com/vgrem/office365-rest-python-client/wiki/How-to-connect-to-SharePoint-Online-and-and-SharePoint-2013-2016-2019-on-premises--with-app-principal)
  
   Example: [connect_with_app_principal.py](examples/sharepoint/auth/with_app_only.py)
  
#### 2. Using username and password 

   Usage:
   ``` 
   user_credentials = UserCredential('{username}','{password}')
   ctx = ClientContext('{url}').with_credentials(user_credentials)
   ```
  
   Example: [connect_with_user_credential.py](examples/sharepoint/auth/with_user_credential.py)
  
#### 3. Using an Azure AD application (certificate credentials flow) 

  Documentation: 
   - [Granting access via Azure AD App-Only](https://docs.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread)  
   - [wiki](https://github.com/vgrem/office365-rest-python-client/wiki/How-to-connect-to-SharePoint-Online-with-certificate-credentials) 
  
  Example: [with_certificate.py](examples/sharepoint/auth/with_certificate.py)

#### 4. Interactive

   to login interactively i.e. via a local browser

   Prerequisite: 
   
   > In Azure Portal, configure the Redirect URI of your
   "Mobile and Desktop application" as ``http://localhost``.

  Example: [connect_interactive.py](examples/sharepoint/auth/with_interactive.py)

  Usage:
```python
from office365.sharepoint.client_context import ClientContext
ctx = ClientContext("{site-url}").with_interactive("{tenant-name-or-id}", "{client-id}")
me = ctx.web.current_user.get().execute_query()
print(me.login_name)
```

### Examples
 
There are **two approaches** available to perform API queries:

1. `ClientContext class` - where you target SharePoint resources such as `Web`, `ListItem` and etc (recommended)
 
```python
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
site_url = "https://{your-tenant-prefix}.sharepoint.com"
ctx = ClientContext(site_url).with_credentials(UserCredential("{username}", "{password}"))
web = ctx.web
ctx.load(web)
ctx.execute_query()
print("Web title: {0}".format(web.properties['Title']))
```
or alternatively via method chaining (a.k.a Fluent Interface): 

```python
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
site_url = "https://{your-tenant-prefix}.sharepoint.com"
ctx = ClientContext(site_url).with_credentials(UserCredential("{username}", "{password}"))
web = ctx.web.get().execute_query()
print("Web title: {0}".format(web.properties['Title']))
```


2. `SharePointRequest class` - where you construct REST queries (and no model is involved)

   The example demonstrates how to read `Web` properties:
   
```python
import json
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.request import SharePointRequest
site_url = "https://{your-tenant-prefix}.sharepoint.com"
request = SharePointRequest(site_url).with_credentials(UserCredential("{username}", "{password}"))
response = request.execute_request("web")
json = json.loads(response.content)
web_title = json['d']['Title']
print("Web title: {0}".format(web_title))
```
  
For SharePoint-specific examples, see:  
📌 **[SharePoint examples guide](examples/sharepoint/README.md)**  


### Support for Azure environments

  To enable authentication to specific Azure environment endpoints, add the `environment` parameter when calling the 
  `ClientContext class` with `.with_user_credentials`, `.with_client_credentials`, or `.with_credentials`

   Example:
   ```python
   from office365.azure_env import AzureEnvironment
   from office365.sharepoint.client_context import ClientContext
   from office365.runtime.auth.client_credential import ClientCredential
   client_credentials = ClientCredential('{client_id}','{client_secret}')
   ctx = ClientContext('{site-url}', environment=AzureEnvironment.USGovernmentHigh).with_credentials(client_credentials)
   ```

# Working with Outlook API

The list of supported APIs:
-   [Outlook Contacts REST API](https://msdn.microsoft.com/en-us/office/office365/api/contacts-rest-operations)
-   [Outlook Calendar REST API](https://msdn.microsoft.com/en-us/office/office365/api/calendar-rest-operations)
-   [Outlook Mail REST API](https://msdn.microsoft.com/en-us/office/office365/api/mail-rest-operations)


Since Outlook REST APIs are available in both Microsoft Graph and the Outlook API endpoint, 
the following clients are available:

- `GraphClient` which targets Outlook API `v2.0` version (*preferable* nowadays, refer [transition to Microsoft Graph-based Outlook REST API](https://docs.microsoft.com/en-us/outlook/rest/compare-graph-outlook) for a details)   
~~- `OutlookClient` which targets Outlook API `v1.0` version (not recommended for usage since `v1.0` version is being deprecated.)~~


### Authentication

[The Microsoft Authentication Library (MSAL) for Python](https://pypi.org/project/msal/) which comes as a dependency 
is used as a default library to obtain tokens to call Microsoft Graph API. 

Using [Microsoft Authentication Library (MSAL) for Python](https://pypi.org/project/msal/)

> Note: access token is getting acquired via [Client Credential flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)
> in the provided examples. Other forms of token acquisition can be found here: https://msal-python.readthedocs.io/en/latest/

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant_name_or_id}').with_client_secret(
    client_id='{client_id}', 
    client_secret='{client_secret}'
)
```
Example: [with_client_secret](examples/auth/with_client_secret.py)

But in terms of Microsoft Graph API authentication, another OAuth spec compliant libraries 
such as [adal](https://github.com/AzureAD/azure-activedirectory-library-for-python) 
are supported as well.   

Using [ADAL Python](https://adal-python.readthedocs.io/en/latest/#)

Usage

```python
import adal
from office365.graph_client import GraphClient

def acquire_token_func():
    authority_url = 'https://login.microsoftonline.com/{tenant_id_or_name}'
    auth_ctx = adal.AuthenticationContext(authority_url)
    token = auth_ctx.acquire_token_with_client_credentials(
        "https://graph.microsoft.com",
        "{client_id}",
        "{client_secret}")
    return token

client = GraphClient(acquire_token_func)

```

#### Example

The example demonstrates how to send an email via [Microsoft Graph endpoint](https://docs.microsoft.com/en-us/graph/api/user-sendmail?view=graph-rest-1.0&tabs=http).

> Note: access token is getting acquired  via [Client Credential flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant='{tenant_name_or_id}').with_username_and_password(
    '{client_id}', '{username}', '{password}'
)

client.me.send_mail(
    subject="Meet for lunch?",
    body="The new cafeteria is open.",
    to_recipients=["fannyd@contoso.onmicrosoft.com"]
).execute_query()

```


Additional examples & scenarios:

-  [download a message](examples/outlook/messages/download.py) 
-  [list messages](examples/outlook/messages/list_all.py)
-  [move messages to a different folder](examples/outlook/messages/move.py)
-  [search messages](examples/outlook/messages/search.py)   
-  [send messages](examples/outlook/messages/send.py)
-  [send messages with attachments](examples/outlook/messages/send_with_attachment.py) 
-  [enable sending emails on behalf of another user in your organization](https://learn.microsoft.com/en-us/microsoft-365/solutions/allow-members-to-send-as-or-send-on-behalf-of-group)

Refer to [examples section](examples/outlook) for other scenarios


# Working with OneDrive and SharePoint v2 APIs

#### Documentation 

[OneDrive Graph API reference](https://docs.microsoft.com/en-us/graph/api/resources/onedrive?view=graph-rest-1.0)

#### Authentication

[The Microsoft Authentication Library (MSAL) for Python](https://pypi.org/project/msal/) which comes as a dependency 
is used to obtain token

```python
import msal

def acquire_token_func():
    """
    Acquire token via MSAL
    """
    authority_url = 'https://login.microsoftonline.com/{tenant_id_or_name}'
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id='{client_id}',
        client_credential='{client_secret}'
    )
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token
``` 


#### Examples 

##### Example: list available drives

The example demonstrates how to enumerate and print drive's url 
which corresponds to [`list available drives` endpoint](https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/drive_list?view=odsp-graph-online)

> Note: access token is getting acquired  via [Client Credential flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)

```python
from office365.graph_client import GraphClient

tenant_name = "contoso.onmicrosoft.com"
client = GraphClient(tenant=tenant_name)
drives = client.drives.get().execute_query()
for drive in drives:
    print("Drive url: {0}".format(drive.web_url))
```


##### Example: download the contents of a DriveItem(folder facet)

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant="contoso.onmicrosoft.com")
# retrieve drive properties 
drive = client.users["{user_id_or_principal_name}"].drive.get().execute_query()
# download files from OneDrive into local folder 
with tempfile.TemporaryDirectory() as path:
    download_files(drive.root, path)
```

where

```python
def download_files(remote_folder, local_path):
    drive_items = remote_folder.children.get().execute_query()
    for drive_item in drive_items:
        if drive_item.file is not None:  # is file?
            # download file content
            with open(os.path.join(local_path, drive_item.name), 'wb') as local_file:
                drive_item.download(local_file).execute_query()
```

Additional examples:

-  [create list column](examples/onedrive/columns/create_text.py) 
-  [download file](examples/onedrive/files/download.py)
-  [export files](examples/onedrive/files/export.py)
-  [upload folder](examples/onedrive/folders/upload.py)   
-  [list drives](examples/onedrive/drives/list.py)
-  [list files](examples/onedrive/folders/list_files.py)

Refer to [OneDrive examples section](examples/onedrive) for more examples.


# Working with Microsoft Teams API

#### Authentication

[The Microsoft Authentication Library (MSAL) for Python](https://pypi.org/project/msal/) which comes as a dependency 
is used to obtain token  

#### Examples 

##### Example: create a new team under a group

The example demonstrates how create a new team under a group 
which corresponds to [`Create team` endpoint](https://docs.microsoft.com/en-us/graph/api/team-put-teams?view=graph-rest-1.0&tabs=http)

```python
from office365.graph_client import GraphClient
client = GraphClient(acquire_token_func)
new_team = client.groups["{group-id}"].add_team().execute_query_retry()
```

Additional examples:

-  [create a team](examples/teams/create_team.py) 
-  [create team from group](examples/teams/create_from_group.py)
-  [list all teams](examples/teams/list_all.py)
-  [list my teams](examples/teams/list_my_teams.py)   
-  [send messages](examples/teams/send_message.py)
  
Refer to [examples section](examples/teams) for other scenarios

# Working with Microsoft Onenote API

The library supports OneNote API in terms of calls to a user's OneNote notebooks, sections, and pages in a personal or organization account

Example: Create a new page

```python
from office365.graph_client import GraphClient
client = GraphClient(tenant='{tenant_name_or_id}').with_username_and_password(
    '{client_id}', '{username}', '{password}'
)

files = {}
with open("./MyPage.html", 'rb') as f, \
    open("./MyImage.png", 'rb') as img_f, \
    open("./MyDoc.pdf", 'rb') as pdf_f:
    files["imageBlock1"] = img_f
    files["fileBlock1"] = pdf_f
    page = client.me.onenote.pages.add(presentation_file=f, attachment_files=files).execute_query()
```

# Working with Microsoft Planner API

The example demonstrates how to create a new planner task
which corresponds to [`Create plannerTask` endpoint](https://docs.microsoft.com/en-us/graph/api/planner-post-tasks?view=graph-rest-1.0):

```python
from office365.graph_client import GraphClient

client = GraphClient(acquire_token_func)
task = client.planner.tasks.add(title="New task", planId="--plan id goes here--").execute_query()
```

# Third Party Libraries and Dependencies
The following libraries will be installed when you install the client library:
* [requests](https://github.com/kennethreitz/requests)
* [Microsoft Authentication Library (MSAL) for Python](https://pypi.org/project/msal/)


# ThanksTo

Powerful Python IDE [`Pycharm`](https://www.jetbrains.com/pycharm) from [`Jetbrains`](https://jb.gg/OpenSourceSupport).

[<img src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.svg">](https://jb.gg/OpenSourceSupport)

