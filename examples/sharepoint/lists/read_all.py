"""Demonstrates how to retrieve all list items from a large list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.collection import ListItemCollection
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def print_progress(items: ListItemCollection) -> None:
    print(f"Items read: {len(items)}")


def main():
    parser = argparse.ArgumentParser(description="Retrieve all list items from a large list")
    parser.add_argument("--list-title", default="Contacts_Large", help="target list title")
    parser.add_argument("--page-size", type=int, default=1000, help="items per page")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    large_list = ctx.web.lists.get_by_title(args.list_title)
    all_items = large_list.items.get_all(args.page_size, print_progress).execute_query()
    print(f"Total items count: {len(all_items)}")


if __name__ == "__main__":
    main()
