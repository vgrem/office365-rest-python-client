"""
Recycle a list item — move it to the recycle bin.

The ``recycle`` operation returns the id of the new recycle bin item.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Send a list item to the recycle bin")
    parser.add_argument("--list-title", default="Documents", help="List containing the item")
    parser.add_argument("--item-id", type=int, required=True, help="Item id to recycle")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    item = ctx.web.lists.get_by_title(args.list_title).items.get_by_id(args.item_id)
    result = item.recycle().execute_query()
    print(f"Recycled item {args.item_id}; recycle bin id: {result.value}")


if __name__ == "__main__":
    main()
