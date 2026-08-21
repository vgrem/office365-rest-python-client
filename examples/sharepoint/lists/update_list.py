"""
Update a list's properties (title, description).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Update a list's properties")
    parser.add_argument("--list-title", default="Documents", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(tenant, client_id, username, password)
    target_list = ctx.web.lists.get_by_title(args.list_title)
    target_list.set_property("Title", "Updated Documents").update().execute_query()
    print("List updated")


if __name__ == "__main__":
    main()
