"""
Extend or update the expiration date of a webhook subscription.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks
"""

import argparse
from datetime import datetime, timedelta

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Extend the expiration date of a webhook subscription")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    parser.add_argument("--list-title", default="Documents", help="list title")
    parser.add_argument("--subscription-id", default=None, help="subscription id (default: first subscription)")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)
    subscriptions = target_list.subscriptions.get().execute_query()
    if args.subscription_id:
        subscription = next((s for s in subscriptions if s.id == args.subscription_id), None)
        if subscription is None:
            raise ValueError(f"Subscription {args.subscription_id} not found")
    else:
        subscription = subscriptions[0]
    new_expiry = datetime.utcnow() + timedelta(days=180)
    subscription.expiration_datetime = new_expiry
    subscription.update().execute_query()
    print(f"Subscription {subscription.id} updated, expires: {subscription.expiration_datetime}")


if __name__ == "__main__":
    main()
