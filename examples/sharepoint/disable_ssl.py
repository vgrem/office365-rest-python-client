"""
Disables SSL certificate verification for SharePoint requests.

⚠️ WARNING: Only use this for testing with self-signed certificates.
Never disable SSL verification in production.

Recommended: disable SSL at the transport level by passing a
pre-configured ``requests.Session`` to ``RequestsTransport``.
This ensures the setting applies to ALL requests, including
internal ones (form digest).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

import requests
from office365.runtime.transport.requests_transport import RequestsTransport
from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_site_url

session = requests.Session()
session.verify = False

ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)
ctx.pending_request().transport = RequestsTransport(session)

web = ctx.web.get().execute_query()
print(web.url)
