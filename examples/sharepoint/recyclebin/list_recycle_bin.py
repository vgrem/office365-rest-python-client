"""
List items in the site recycle bin (first or second stage).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="List recycle bin items")
    parser.add_argument("--stage", type=int, choices=[0, 1], default=0, help="Recycle bin stage (0=first, 1=second)")
    parser.add_argument("--limit", type=int, default=100, help="Maximum items to return")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    items = ctx.web.get_recycle_bin_items(row_limit=args.limit, item_state=args.stage).execute_query()
    stage = "second" if args.stage else "first"
    print(f"Recycle bin ({stage} stage) — {len(items)} items:\n")
    for item in items:
        name = item.title or item.leaf_name or "(unnamed)"
        print(f"  {name:40s}  deleted: {item.deleted_date_local_formatted or '?'}")
        print(f"    By: {item.deleted_by_name or '?'}  Size: {item.size or 0} bytes")


if __name__ == "__main__":
    main()
