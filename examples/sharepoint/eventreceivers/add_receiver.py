"""
Add a remote event receiver to a SharePoint list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Add a remote event receiver to a list")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    parser.add_argument("--list-title", default="Documents", help="list title")
    parser.add_argument("--receiver-name", default="RemoteItemAdded", help="event receiver name")
    parser.add_argument(
        "--receiver-url", default="https://your-app.azurewebsites.net/webhook", help="receiver endpoint URL"
    )
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)

    receiver = target_list.event_receivers.add(
        receiver_name=args.receiver_name,
        receiver_url=args.receiver_url,
    ).execute_query()
    print(f"Event receiver added: {receiver.properties.get('ReceiverId')}")


if __name__ == "__main__":
    main()
