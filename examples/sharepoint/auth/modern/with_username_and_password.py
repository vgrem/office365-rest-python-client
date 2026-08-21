"""
Connect to SharePoint using username and password via MSAL ROPC flow.

This is the modern replacement for the legacy SAML-based user authentication.
Uses the OAuth 2.0 Resource Owner Password Credentials grant.

Prerequisites:
    - An app registered in Azure AD
    - Grant the app appropriate SharePoint permissions
    - The app must support public client flows (allow public client in manifest)

See https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Connect to SharePoint with username and password via MSAL ROPC").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    web = ctx.web.get().execute_query()
    print(web.url)


if __name__ == "__main__":
    main()
