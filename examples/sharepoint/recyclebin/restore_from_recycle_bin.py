"""
Restore an item (or all items) from the site recycle bin.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Restore recycle bin items")
    parser.add_argument("--item-id", help="Recycle bin item id to restore (default: first item)")
    parser.add_argument("--all", action="store_true", help="Restore all items")
    args = parser.parse_args()

    if args.all and args.item_id:
        raise SystemExit("Use either --item-id or --all, not both")

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    if args.all:
        ctx.web.recycle_bin.restore_all().execute_query()
        print("All recycle bin items restored")
        return

    if args.item_id:
        item = ctx.web.recycle_bin.get_by_id(args.item_id)
        ctx.load(item).execute_query()
    else:
        items = ctx.web.recycle_bin.get().execute_query()
        if not len(items):
            raise SystemExit("Recycle bin is empty")
        item = items[0]
    name = item.title or item.leaf_name or args.item_id
    item.restore().execute_query()
    print(f"Restored: {name}")


if __name__ == "__main__":
    main()
