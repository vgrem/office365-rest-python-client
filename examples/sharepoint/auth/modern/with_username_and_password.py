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

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
web = ctx.web.get().execute_query()
print(web.url)
