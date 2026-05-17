"""
Token acquisition using a client certificate (X.509) via a custom callback.

Demonstrates how to acquire a token by using certificate credentials.

Loads a private key from a PEM file and uses msal.ConfidentialClientApplication
to authenticate with the Microsoft identity platform.

https://learn.microsoft.com/en-us/graph/auth
https://learn.microsoft.com/en-us/azure/active-directory/develop/msal-authentication-flows#certificates
"""

from typing import Dict, cast

from office365.graph_client import GraphClient
from tests import test_cert_path, test_cert_thumbprint, test_client_id, test_tenant_name


def acquire_token() -> Dict[str, str]:
    with open(test_cert_path, "r", encoding="utf-8") as f:
        private_key = f.read()

    authority_url = f"https://login.microsoftonline.com/{test_tenant_name}"
    credentials = {"thumbprint": test_cert_thumbprint, "private_key": private_key}
    import msal

    app = msal.ConfidentialClientApplication(
        test_client_id,
        authority=authority_url,
        client_credential=credentials,
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return cast(Dict[str, str], result)


client = GraphClient(acquire_token)
drives = client.drives.get().top(10).execute_query()
for drive in drives:
    print(drive.web_url)
