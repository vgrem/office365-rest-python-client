"""
Migrate from legacy SAML auth to Azure AD certificate auth.

Microsoft retired SAML/WS-Federation for SharePoint Online in May 2026
(MC1184649). The old with_user_credentials() method no longer works
for SharePoint Online.

This example covers the migration path to Azure AD app-only with a
certificate, which is the recommended replacement.

Prerequisites:
    - An app registered in Azure AD (or update an existing one)
    - openssl (for certificate generation)
    - Admin consent for SharePoint API permissions

See https://learn.microsoft.com/en-us/sharepoint/dev/security/saml-auth-retirement
See https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread
"""

# ===========================================================================
# Step 1 -- Generate a self-signed certificate (run in terminal)
# ===========================================================================
#
#   # Create private key and self-signed certificate (365-day validity)
#   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#     -keyout private_key.pem -out cert.pem \
#     -subj "/CN=SharePointApp"
#
#   # Extract thumbprint (needed below)
#   openssl x509 -in cert.pem -fingerprint -noout \
#     | sed 's/.*=//' | sed 's/://g'
#
#   # Alternatively, convert an existing PFX from Azure:
#   openssl pkcs12 -in myapp.pfx -nocerts -nodes \
#     | openssl pkcs8 -topk8 -nocrypt -out private_key.pem
#   openssl pkcs12 -in myapp.pfx -nokeys -out cert.pem

# ===========================================================================
# Step 2 -- Register / update an app in Azure AD
# ===========================================================================
#
#   Option A -- Create a new app registration:
#     1. Go to https://entra.microsoft.com/ -> App registrations -> New registration
#     2. Name: e.g. "SharePoint Python Client"
#     3. Supported account types: "Accounts in this organizational directory only"
#     4. Do not set a redirect URI (this is app-only)
#     5. Click Register and note the Application (client) ID and Directory (tenant) ID
#
#   Option B -- Update an existing app:
#     1. Same app works -- just add a certificate credential under "Certificates & secrets"
#     2. No need to create a new app registration

# ===========================================================================
# Step 3 -- Grant SharePoint API permissions
# ===========================================================================
#
#   IMPORTANT: Grant SharePoint permissions, not Microsoft Graph permissions.
#   ClientContext uses the SharePoint REST API, which requires SharePoint
#   resource permissions.
#
#     1. In your app registration -> "API permissions"
#     2. Click "Add a permission" -> "APIs my organization uses"
#     3. Search for and select "SharePoint"
#     4. Select "Application permissions"
#     5. Choose at minimum: Sites.Read.All or Sites.FullControl.All
#     6. Click "Add permissions"
#     7. Click "Grant admin consent for [tenant]" and confirm
#
#   Verify that "SharePoint" (not "Microsoft Graph") appears among configured
#   permissions.

# ===========================================================================
# Step 4 -- Upload the certificate to the app registration
# ===========================================================================
#
#     1. In your app registration -> "Certificates & secrets"
#     2. Click "Upload certificate"
#     3. Select the cert.pem file from Step 1
#     4. Click "Add"
#     5. Copy the Thumbprint value (hex string, no colons)

# ===========================================================================
# Step 5 -- Connect and verify
# ===========================================================================

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_site_url, test_tenant

site_url = test_site_url
tenant = test_tenant
client_id = test_client_id
thumbprint = "AABBCCDDEEFF00112233445566778899AABBCCDD"

ctx = ClientContext(site_url).with_client_certificate(
    tenant=tenant,
    client_id=client_id,
    thumbprint=thumbprint,
    cert_path="./private_key.pem",
)

web = ctx.web.get().execute_query()
print("Connected to: {0}".format(web.url))
print("Site title: {0}".format(web.title))

# ===========================================================================
# What changed from the old SAML approach
# ===========================================================================
#
#   OLD (retired -- do not use):
#     ctx = ClientContext(url).with_user_credentials(username, password)
#
#   NEW (recommended):
#     ctx = ClientContext(url).with_client_certificate(
#         tenant, client_id, thumbprint, cert_path
#     )
#
#   Benefits of certificate auth over SAML:
#     - No username/password to rotate
#     - No MFA or conditional access issues (app-only)
#     - Aligned with Microsoft's long-term auth strategy
#     - Works with Sovereign clouds (GCC High, 21Vianet, etc.)

# ===========================================================================
# Alternative: MSAL ROPC (requires delegated user context)
# ===========================================================================
#
#   If your code needs user-specific (delegated) access rather than app-only:
#
#     from office365.sharepoint.client_context import ClientContext
#     from tests import test_client_id, test_site_url, test_tenant, test_username
#
#     ctx = ClientContext(site_url).with_username_and_password(
#         tenant=test_tenant,
#         client_id=test_client_id,
#         username=test_username,
#         password="***",
#     )
#
#   Limitations of ROPC flow:
#     - Does not support MFA
#     - May be blocked by conditional access policies
#     - Tenant must allow public client flows in the app manifest
#     - Microsoft recommends certificate or interactive flows instead
#
#   See https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc
