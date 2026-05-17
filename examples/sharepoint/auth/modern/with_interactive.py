"""
Connect to SharePoint using interactive browser-based login.

Useful when multi-factor authentication (MFA) is required or
when user consent for additional permissions is needed.

Prerequisites:
    - In Azure Portal, configure the Redirect URI of your
      "Mobile and Desktop application" as ``http://localhost``.

See https://learn.microsoft.com/en-us/azure/active-directory/develop/
msal-authentication-flows#interactive-and-non-interactive-authentication
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_interactive(test_tenant, test_client_id)
me = ctx.web.current_user.get().execute_query()
print(me)
web = ctx.web.get().execute_query()
print(web)
