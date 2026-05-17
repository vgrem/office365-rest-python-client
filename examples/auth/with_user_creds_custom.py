"""
Username/Password (Resource Owner Password Credentials) flow via a custom callback.

Uses msal.PublicClientApplication.acquire_token_by_username_password directly
instead of the built-in with_username_and_password method.

https://learn.microsoft.com/en-us/graph/auth
https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc
"""

import msal
from office365.graph_client import GraphClient
from tests import test_client_id, test_tenant, test_user_credentials


def acquire_token():
    authority_url = f"https://login.microsoftonline.com/{test_tenant}"
    app = msal.PublicClientApplication(authority=authority_url, client_id=test_client_id)

    result = app.acquire_token_by_username_password(
        username=test_user_credentials.userName,
        password=test_user_credentials.password,
        scopes=["https://graph.microsoft.com/.default"],
    )
    return result


client = GraphClient(acquire_token)
me = client.me.get().execute_query()
print(me.user_principal_name)
