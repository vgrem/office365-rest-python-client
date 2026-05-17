"""
Disables SSL certificate verification for SharePoint requests.

⚠️ WARNING: This should only be used for testing with self-signed
certificates. Never disable SSL verification in production.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

import ssl

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_site_url

print(ssl.OPENSSL_VERSION)


def disable_ssl(request):
    print("Disabling certificate verification...")
    request.verify = False  # Disable certificate verification


ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)
ctx.pending_request().beforeExecute += disable_ssl
web = ctx.web.get().execute_query()
print(web.url)
