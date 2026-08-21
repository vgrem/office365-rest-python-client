"""
Remove an event receiver by ID.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Remove an event receiver by ID")
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
    receivers = target_list.event_receivers.get().execute_query()
    if receivers:
        target = receivers[0]
        receiver_id = target.properties.get("ReceiverId")
        if receiver_id:
            receiver = target_list.event_receivers.get_by_id(receiver_id)
            receiver.delete_object().execute_query()
            print(f"Removed event receiver: {receiver_id}")


if __name__ == "__main__":
    main()
