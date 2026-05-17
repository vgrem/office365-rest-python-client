"""
Connect to SharePoint using a custom MSAL token acquisition callback.

⚠️ NOTE: Using Azure AD app-only with client credentials against
SharePoint v1 API will return 401. Use certificate auth instead.
"""

from office365.runtime.auth.token_response import TokenResponse
from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_team_site_url, test_tenant


def acquire_token():
    authority = "https://login.microsoftonline.com/{0}".format(test_tenant)
    import msal

    app = msal.ConfidentialClientApplication(
        authority=authority,
        client_id=test_client_id,
        client_credential=test_client_secret,
    )
    token_json = app.acquire_token_for_client(scopes=["https://mediadev8.sharepoint.com/.default"])
    return TokenResponse.from_json(token_json)


ctx = ClientContext(test_team_site_url).with_access_token(acquire_token)
target_web = ctx.web.get().execute_query()
print(target_web.url)
