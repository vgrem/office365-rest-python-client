"""
Connect to SharePoint using Azure AD app-only with a certificate.

Supports three variants:
  1. PEM file with passphrase
  2. PEM file without passphrase (private key as string)
  3. Custom permission scopes

Prerequisites:
    - An app registered in Azure AD with a certificate credential
    - Upload the certificate public key to the app registration
    - Grant the app appropriate SharePoint permissions

https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_site_url, test_tenant

# Variant 1: PEM file with passphrase
ctx = ClientContext(test_site_url).with_client_certificate(
    tenant=test_tenant,
    client_id=test_client_id,
    thumbprint="thumbprint",
    cert_path="./cert.pem",
    passphrase="password",
)
web = ctx.web.get().execute_query()
print(web.title)

# Variant 2: Private key as string (no passphrase)
# ctx = ClientContext(test_site_url).with_client_certificate(
#     tenant=test_tenant,
#     client_id=test_client_id,
#     thumbprint="thumbprint",
#     private_key="""-----BEGIN PRIVATE KEY-----
# MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+gq...
# -----END PRIVATE KEY-----""",
# )

# Variant 3: Custom permission scopes
# from office365.azure_env import AzureEnvironment
# ctx = ClientContext(test_site_url, environment=AzureEnvironment.Global).with_client_certificate(
#     tenant=test_tenant,
#     client_id=test_client_id,
#     thumbprint="thumbprint",
#     cert_path="./cert.pem",
#     scopes=["https://contoso.sharepoint.com/Sites.Read.All"],
# )
