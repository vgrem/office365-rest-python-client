"""
Remove a webhook subscription from a SharePoint list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Remove a webhook subscription from a list")
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
    subscription.delete_object().execute_query()
    print(f"Subscription {subscription.id} deleted")

    # Alternative — remove by ID directly
    # target_list.subscriptions.remove("subscription-id-here").execute_query()


if __name__ == "__main__":
    main()
