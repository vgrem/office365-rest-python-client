"""
Add a custom action (toolbar button) to a SharePoint list.

Requires Site Owner on the target list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Add a toolbar button custom action to a list")
    parser.add_argument("--list-title", default="Documents", help="target list")
    parser.add_argument("--title", default="Open in App", help="action title")
    parser.add_argument("--url", default="https://example.com/open?id={ItemId}", help="action URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    action = target_list.user_custom_actions.add(
        title=args.title,
        location="EditControlBlock",
        url=args.url,
    ).execute_query()
    print(f"List action added: {action.properties.get('Id')}")


if __name__ == "__main__":
    main()
