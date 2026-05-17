"""
Connect to SharePoint using Azure AD app-only authentication with a certificate.

Prerequisites:
    - An app registered in Azure AD with a certificate credential
    - Upload the certificate public key to the app registration
    - Grant the app appropriate SharePoint permissions

See https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_cert_thumbprint, test_client_id, test_site_url, test_tenant

cert_credentials = {
    "tenant": test_tenant,
    "client_id": test_client_id,
    "thumbprint": test_cert_thumbprint,
    "cert_path": "./selfsigncert.pem",
}
ctx = ClientContext(test_site_url).with_client_certificate(**cert_credentials)
current_web = ctx.web.get().execute_query()
print("{0}".format(current_web.url))
