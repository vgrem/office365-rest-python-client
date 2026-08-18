"""
Connect with a custom token callback.

Useful when the access token is acquired by your own code (e.g. a secrets
vault, managed identity, or a custom identity provider). The callback must
return a dict with an ``access_token`` key.

https://learn.microsoft.com/en-us/graph/auth
"""

import msal
from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def acquire_token() -> dict:
    """Acquire a client-credentials token yourself (e.g. from a vault)."""
    app = msal.ConfidentialClientApplication(
        client_id, client_credential=client_secret, authority=f"https://login.microsoftonline.com/{tenant}"
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if not result or "access_token" not in result:
        raise RuntimeError(f"Token acquisition failed: {result}")
    return result


client = GraphClient(tenant=tenant, token_callback=acquire_token)
org = client.organization.get().execute_query()
for o in org:
    print(f"Organization: {o.properties.get('displayName')}")
