"""
List all custom actions on a site (web) or list.

Requires read access.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List custom actions")
    parser.add_argument("--list-title", default=None, help="also list actions on this list (default: site only)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    actions = ctx.web.user_custom_actions.get().execute_query()
    print(f"=== Site actions ({len(actions)}) ===")
    for a in actions:
        print(f"  {a.properties.get('Title', '')}  (ID: {a.properties.get('Id', '')})")

    if args.list_title:
        target_list = ctx.web.lists.get_by_title(args.list_title)
        list_actions = target_list.user_custom_actions.get().execute_query()
        print(f"=== List actions on '{args.list_title}' ({len(list_actions)}) ===")
        for a in list_actions:
            print(f"  {a.properties.get('Title', '')}  (ID: {a.properties.get('Id', '')})")


if __name__ == "__main__":
    main()
