"""
Token acquisition via the legacy ADAL library (username/password).

Note: ADAL for Python is no longer receiving new feature improvements. Its successor, MSAL for Python,
is now generally available. Prefer the MSAL-based examples (with_user_creds.py) instead.

https://learn.microsoft.com/en-us/graph/auth
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def acquire_token():
    import adal  # pylint: disable=E0401

    authority_url = f"https://login.microsoftonline.com/{test_tenant}"
    auth_ctx = adal.AuthenticationContext(authority_url)
    token = auth_ctx.acquire_token_with_username_password(
        "https://graph.microsoft.com",
        test_username,
        test_password,
        test_client_id,
    )
    return token


client = GraphClient(acquire_token)
me = client.me.get().execute_query()
print(me.display_name)
