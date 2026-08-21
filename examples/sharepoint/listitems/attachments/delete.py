"""
Deletes attachments from a List
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Delete attachments from all list items")
    parser.add_argument("--list-title", default="Company Tasks", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    tasks_list = ctx.web.lists.get_by_title(args.list_title)
    task_items = tasks_list.items.get().execute_query()
    for task_item in task_items:
        task_item.attachment_files.delete_all().execute_query()
        print("Attachments have been deleted for list item {0}".format(task_item.id))


if __name__ == "__main__":
    main()
