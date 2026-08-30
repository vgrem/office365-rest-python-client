"""Assigns a Document ID to a site.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Assign a Document ID prefix to the site")
    parser.add_argument("--site-url", default=team_site_url, help="target site URL")
    parser.add_argument("--prefix", default="DOCID", help="document ID prefix (default: DOCID)")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    ctx.web.assign_document_id(args.prefix).execute_query()
    print(f"Document IDs assigned with prefix '{args.prefix}'")


if __name__ == "__main__":
    main()
