"""Demonstrates how to list activated features on a site.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="List activated features on a site")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    features = ctx.site.features.get().execute_query()
    for f in features:
        print(f"  {f.display_name or 'N/A'}  (ID: {f.definition_id})")
    print(f"Total: {len(features)} activated features")


if __name__ == "__main__":
    main()
