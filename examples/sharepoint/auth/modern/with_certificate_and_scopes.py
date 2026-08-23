"""
Connect to SharePoint using Azure AD app-only with a certificate and custom scopes.

By default the client requests the site's default permission scope; pass explicit
``scopes`` to control which resource scopes are requested.

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
    parser = argparse.ArgumentParser(description="Connect to SharePoint app-only with a certificate and custom scopes")
    parser.add_argument("--thumbprint", default=cert_thumbprint, help="certificate thumbprint")
    parser.add_argument("--cert-path", default=cert_path, help="path to the PEM private key file")
    parser.add_argument("--scopes", default=[f"{site_url}.Read.All"], nargs="+", help="permission scopes to request")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant=tenant,
        client_id=client_id,
        thumbprint=args.thumbprint,
        cert_path=args.cert_path,
        scopes=args.scopes,
    )
    web = ctx.web.get().execute_query()
    print(web.title)


if __name__ == "__main__":
    main()
