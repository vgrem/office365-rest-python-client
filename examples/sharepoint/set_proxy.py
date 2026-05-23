"""
Demonstrates how to configure a proxy for all SharePoint REST API requests.

Best practice: set proxy at the transport level by passing a pre-configured
``requests.Session`` to ``RequestsTransport``.  This ensures the proxy
applies to ALL requests, including internal ones (form digest).

For MSAL authentication requests to login.microsoftonline.com, set the
``HTTPS_PROXY`` environment variable instead — MSAL reads it automatically.

Usage:
    export HTTPS_PROXY="http://proxy:8080"
    python set_proxy.py

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

import requests
from office365.runtime.transport.requests_transport import RequestsTransport
from office365.sharepoint.client_context import ClientContext

session = requests.Session()
session.proxies = {
    "http": "http://proxy:8080",
    "https": "http://proxy:8080",
}

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)
ctx.pending_request().transport = RequestsTransport(session)

web = ctx.web.get().execute_query()
print(f"Connected to: {web.url}")
