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

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Connect to SharePoint using app-only with a certificate")
    parser.add_argument("--thumbprint", default="thumbprint", help="certificate thumbprint")
    parser.add_argument("--cert-path", default="./cert.pem", help="path to the PEM certificate")
    parser.add_argument("--passphrase", default="password", help="private key passphrase")
    args = parser.parse_args()

    # Variant 1: PEM file with passphrase
    ctx = ClientContext(site_url).with_client_certificate(
        tenant=tenant,
        client_id=client_id,
        thumbprint=args.thumbprint,
        cert_path=args.cert_path,
        passphrase=args.passphrase,
    )
    web = ctx.web.get().execute_query()
    print(web.title)

    # Variant 2: Private key as string (no passphrase)
    # ctx = ClientContext(site_url).with_client_certificate(
    #     tenant=tenant,
    #     client_id=client_id,
    #     thumbprint="thumbprint",
    #     private_key="""-----BEGIN PRIVATE KEY-----
    # MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+gq...
    # -----END PRIVATE KEY-----""",
    # )

    # Variant 3: Custom permission scopes
    # from office365.azure_env import AzureEnvironment
    # ctx = ClientContext(site_url, environment=AzureEnvironment.Global).with_client_certificate(
    #     tenant=tenant,
    #     client_id=client_id,
    #     thumbprint="thumbprint",
    #     cert_path="./cert.pem",
    #     scopes=["https://contoso.sharepoint.com/Sites.Read.All"],
    # )


if __name__ == "__main__":
    main()
