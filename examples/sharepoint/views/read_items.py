"""
Read items from the default view or a custom view of a list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Read items from a list view")
    parser.add_argument("--list-title", default="Documents", help="List or library title")
    parser.add_argument("--view", help="Custom view title (default: the list's default view)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    view = target_list.views.get_by_title(args.view) if args.view else target_list.default_view
    items = view.get_items().execute_query()
    print(f"View items ({len(items)}):")
    for item in items:
        print(f"  {item.properties}")


if __name__ == "__main__":
    main()
