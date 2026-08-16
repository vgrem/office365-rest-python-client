"""
Move recycle bin items to the second-stage recycle bin.

Second-stage items are not automatically purged and are harder to recover,
so this is the "deeper delete" step of the recycle bin lifecycle.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Move recycle bin items to the second stage")
    parser.add_argument("--item-id", help="Recycle bin item id to move")
    parser.add_argument("--all", action="store_true", help="Move all first-stage items")
    args = parser.parse_args()

    if args.all and args.item_id:
        raise SystemExit("Use either --item-id or --all, not both")

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    if args.all:
        ctx.web.recycle_bin.move_all_to_second_stage().execute_query()
        print("All first-stage items moved to the second-stage recycle bin")
        return

    if not args.item_id:
        raise SystemExit("Provide --item-id or --all")
    item = ctx.web.recycle_bin.get_by_id(args.item_id)
    ctx.load(item).execute_query()
    name = item.title or item.leaf_name or args.item_id
    item.move_to_second_stage().execute_query()
    print(f"Moved to second stage: {name}")


if __name__ == "__main__":
    main()
