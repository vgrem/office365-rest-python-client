"""
Enumerate content types on the site or on a specific list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="List content types")
    parser.add_argument("--list-title", help="Scope to a list (default: site content types)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    if args.list_title:
        cts = ctx.web.lists.get_by_title(args.list_title).content_types.get().execute_query()
        print(f"Content types on '{args.list_title}':")
    else:
        cts = ctx.web.content_types.get().execute_query()
        print("Site content types:")

    for ct in cts:
        print(f"  {ct.name}  (ID: {ct.id})")
    print(f"Total: {len(cts)} content types")


if __name__ == "__main__":
    main()
