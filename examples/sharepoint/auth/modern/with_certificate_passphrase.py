"""
Connect to SharePoint using Azure AD app-only with an encrypted certificate.

Prerequisites:
    - An app registered in Azure AD with a certificate credential
    - Certificate private key is encrypted with a passphrase

To create an encrypted self-signed certificate:
    openssl req -x509 -newkey rsa:2048 -keyout selfsignkey.pem -out selfsigncert.pem -days 365

See https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread
"""

import os

from office365.sharepoint.client_context import ClientContext
from tests import test_cert_thumbprint, test_client_id, test_site_url, test_tenant

cert_credentials = {
    "tenant": test_tenant,
    "client_id": test_client_id,
    "thumbprint": test_cert_thumbprint,
    "cert_path": "{0}/../selfsignkeyenc.pem".format(os.path.dirname(__file__)),
    "passphrase": "Password",
}
ctx = ClientContext(test_site_url).with_client_certificate(**cert_credentials)
current_web = ctx.web.get().execute_query()
print("{0}".format(current_web.url))
