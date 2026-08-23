"""
Subscribe to list change notifications via a SharePoint webhook.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks
"""

import argparse
from datetime import datetime, timedelta, timezone

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Subscribe to list change notifications")
    parser.add_argument("--list-title", default="Documents", help="list to subscribe to")
    parser.add_argument("--notification-url", required=True, help="your webhook endpoint URL")
    parser.add_argument("--expiration", default=None, help="ISO expiration datetime (default: now + 180 days)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    expiration = (
        datetime.fromisoformat(args.expiration) if args.expiration else datetime.now(timezone.utc) + timedelta(days=180)
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    subscription = target_list.subscriptions.add(args.notification_url, expiration).execute_query()
    print(f"Subscription created: {subscription.id}")
    print(f"Notification URL: {subscription.notification_url}")
    print(f"Expires: {subscription.expiration_datetime}")


if __name__ == "__main__":
    main()
