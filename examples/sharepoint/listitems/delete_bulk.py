"""
Delete many list items in a single OData $batch request.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Bulk-delete list items via $batch")
    parser.add_argument("--list-title", default="Documents", help="list title")
    parser.add_argument("--title-prefix", default="Bulk item", help="only items with this title prefix are deleted")
    parser.add_argument("--batch-size", type=int, default=100, help="operations per batch request")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    items = ctx.web.lists.get_by_title(args.list_title).items.get().execute_query()

    deleted = 0
    for item in items:
        title = item.properties.get("Title") or ""
        if title.startswith(args.title_prefix):
            item.delete_object()
            deleted += 1
    ctx.execute_batch(args.batch_size)
    print(f"{deleted} items queued for deletion")


if __name__ == "__main__":
    main()
