"""
Connect to SharePoint using Azure AD app-only with a certificate (private key string).

Loads the PEM private key and passes its content directly via the ``private_key``
argument instead of a file path.

Prerequisites:
    - An app registered in Azure AD with a certificate credential
    - Upload the certificate public key to the app registration
    - Grant the app appropriate SharePoint permissions

https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Connect to SharePoint app-only with a certificate (private key)")
    parser.add_argument("--thumbprint", default=cert_thumbprint, help="certificate thumbprint")
    parser.add_argument("--cert-path", default=cert_path, help="path to the PEM private key file to load")
    args = parser.parse_args()

    with open(args.cert_path, "r", encoding="utf-8") as f:
        private_key = f.read()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant=tenant,
        client_id=client_id,
        thumbprint=args.thumbprint,
        private_key=private_key,
    )
    web = ctx.web.get().execute_query()
    print(web.title)


if __name__ == "__main__":
    main()
