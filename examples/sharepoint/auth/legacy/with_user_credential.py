"""
Connect to SharePoint using user credentials via legacy SAML auth.

⚠️ DEPRECATED: This uses the legacy SAML-based auth flow which is
being phased out by Microsoft. Use with_username_and_password instead
(MSAL ROPC OAuth 2.0). See modern/with_username_and_password.py.

See https://learn.microsoft.com/en-us/microsoft-365/enterprise/modern-auth-for-office-2013-and-2016
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import password, team_site_url, username


def main():
    argparse.ArgumentParser(description="Connect to SharePoint with legacy SAML user credentials").parse_args()

    ctx = ClientContext(team_site_url).with_user_credentials(username, password)
    web = ctx.web.get().execute_query()
    print(web.url)


if __name__ == "__main__":
    main()
