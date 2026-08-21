"""
List all event receivers on a SharePoint list or web.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List all event receivers on a list or web")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    parser.add_argument("--list-title", default="Documents", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )

    # List-scoped event receivers
    target_list = ctx.web.lists.get_by_title(args.list_title)
    receivers = target_list.event_receivers.get().execute_query()
    print(f"=== Event receivers on '{args.list_title}' ({len(receivers)}) ===")
    for r in receivers:
        print(
            f"  {r.properties.get('ReceiverName', '')}  "
            f"(EventType: {r.properties.get('EventType', '')}, "
            f"ReceiverId: {r.properties.get('ReceiverId', '')})"
        )


if __name__ == "__main__":
    main()
