"""
Connect to SharePoint using user credentials via legacy SAML auth.

⚠️ DEPRECATED: This uses the legacy SAML-based auth flow which is
being phased out by Microsoft. Use with_username_and_password instead
(MSAL ROPC OAuth 2.0). See modern/with_username_and_password.py.

See https://learn.microsoft.com/en-us/microsoft-365/enterprise/modern-auth-for-office-2013-and-2016
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_password, test_team_site_url, test_username

ctx = ClientContext(test_team_site_url).with_user_credentials(test_username, test_password)
web = ctx.web.get().execute_query()
print(web.url)
