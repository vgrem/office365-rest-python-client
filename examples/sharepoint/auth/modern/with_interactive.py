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

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, site_url, tenant


def main():
    argparse.ArgumentParser(description="Connect to SharePoint using interactive browser-based login").parse_args()

    ctx = ClientContext(site_url).with_interactive(tenant, client_id)
    me = ctx.web.current_user.get().execute_query()
    print(me)
    web = ctx.web.get().execute_query()
    print(web)


if __name__ == "__main__":
    main()
