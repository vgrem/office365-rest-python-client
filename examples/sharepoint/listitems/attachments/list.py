"""Demonstrates how to list attachments of a list item"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List list item attachments")
    parser.add_argument("--list-title", default="Company Tasks", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    source_list = ctx.web.lists.get_by_title(args.list_title)
    items = source_list.items.select(["Id"]).expand(["AttachmentFiles"]).get().execute_query()
    for item in items:
        for attachment_file in item.attachment_files:
            print(attachment_file)


if __name__ == "__main__":
    main()
