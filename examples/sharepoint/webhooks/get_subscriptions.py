"""
List all webhook subscriptions on a SharePoint list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List webhook subscriptions on a list")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    parser.add_argument("--list-title", default="Documents", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    subscriptions = target_list.subscriptions.get().execute_query()
    for sub in subscriptions:
        print(f"ID: {sub.id}")
        print(f"  Notification URL: {sub.notification_url}")
        print(f"  Expires: {sub.expiration_datetime}")
        print(f"  App ID: {sub.application_id}")


if __name__ == "__main__":
    main()
