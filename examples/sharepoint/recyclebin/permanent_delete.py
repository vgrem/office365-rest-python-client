"""
Permanently delete recycle bin items from the first or second stage.

Permanent deletion is irreversible — items cannot be recovered.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Permanently delete recycle bin items")
    parser.add_argument("--stage", type=int, choices=[0, 1], default=0, help="Recycle bin stage (0=first, 1=second)")
    parser.add_argument("--item-id", help="Recycle bin item id to delete")
    parser.add_argument("--all", action="store_true", help="Delete all items in the stage")
    args = parser.parse_args()

    if not args.item_id and not args.all:
        raise SystemExit("Provide --item-id or --all")
    if args.item_id and args.all:
        raise SystemExit("Use either --item-id or --all, not both")

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    if args.item_id:
        ctx.web.recycle_bin.delete_by_ids([args.item_id]).execute_query()
        print(f"Permanently deleted item {args.item_id}")
        return

    if args.stage == 1:
        ctx.web.recycle_bin.delete_all_second_stage_items().execute_query()
        print("All second-stage items permanently deleted")
    else:
        ctx.web.recycle_bin.delete_all().execute_query()
        print("All first-stage items permanently deleted")


if __name__ == "__main__":
    main()
