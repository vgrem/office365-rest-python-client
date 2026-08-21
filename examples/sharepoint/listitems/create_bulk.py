"""
Create many list items in a single OData $batch request.

Each ``add_item`` is queued, then ``execute_batch`` submits them in one
batch (up to ``--batch-size`` operations per request).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Bulk-create list items via $batch")
    parser.add_argument("--list-title", default="Documents", help="list title")
    parser.add_argument("--count", type=int, default=100, help="number of items to create")
    parser.add_argument("--batch-size", type=int, default=100, help="operations per batch request")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    for i in range(args.count):
        target_list.add_item({"Title": f"Bulk item {i + 1}"})

    added = {"count": 0}

    def _progress(return_types) -> None:
        added["count"] += len([t for t in return_types if isinstance(t, ListItem)])
        print(f"{added['count']} items added")

    ctx.execute_batch(args.batch_size, success_callback=_progress)
    print(f"Done: {added['count']} items created in bulk.")


if __name__ == "__main__":
    main()
