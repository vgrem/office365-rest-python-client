"""
Connect to SharePoint using ACS App-Only principal (client credentials).

⚠️ DEPRECATED: Azure Access Control Service (ACS) is being retired.
ACS stopped working for new tenants on Nov 1, 2024, and will be fully
retired on April 2, 2026. Use Azure AD certificate auth instead.

This method is still relevant for SharePoint on-premises.

See https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    argparse.ArgumentParser(description="Connect to SharePoint with client credentials").parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_web = ctx.web.get().execute_query()
    print(target_web.url)


if __name__ == "__main__":
    main()
