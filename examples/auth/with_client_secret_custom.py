"""
Token acquisition via client secret using a custom callback.

The following options are supported:
   - Use the built-in GraphClient(tenant=tenant).with_client_secret(client_id, client_secret) method
   - Or provide a custom callback to the GraphClient constructor as demonstrated below

https://learn.microsoft.com/en-us/graph/auth
https://learn.microsoft.com/en-us/entra/identity-platform/msal-authentication-flows#client-credentials
"""

from typing import Dict, cast

import msal
from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def acquire_token() -> Dict[str, str]:
    authority_url = f"https://login.microsoftonline.com/{test_tenant}"
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id=test_client_id,
        client_credential=test_client_secret,
    )
    return cast(Dict[str, str], app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"]))


client = GraphClient(acquire_token)
root_site = client.sites.root.get().execute_query()
print(root_site.web_url)
