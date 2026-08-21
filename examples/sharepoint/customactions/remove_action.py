"""
Remove a custom action by ID (defaults to the first site action).

Requires Site Owner.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Remove a custom action")
    parser.add_argument("--action-id", default=None, help="custom action ID (default: first site action)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    if args.action_id:
        action_id = args.action_id
    else:
        actions = ctx.web.user_custom_actions.get().execute_query()
        if not actions:
            print("No custom actions found.")
            return
        action_id = actions[0].properties.get("Id")
        if not action_id:
            print("No custom action ID available.")
            return

    ctx.web.user_custom_actions[action_id].delete_object().execute_query()
    print(f"Removed action ID: {action_id}")


if __name__ == "__main__":
    main()
