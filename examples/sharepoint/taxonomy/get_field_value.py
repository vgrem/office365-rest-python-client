"""
Demonstrates how to get a taxonomy (managed metadata) field value from a list item.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Get a taxonomy field value from a list item")
    parser.add_argument("--list-title", default="Requests", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    items = ctx.web.lists.get_by_title(args.list_title).items.get().execute_query()
    if not items:
        sys.exit("No list items were found.")

    single = items[0].properties.get("Country") or {}
    multi = items[0].properties.get("Countries") or []

    if isinstance(single, dict):
        print(f"Single value TermGuid: {single.get('TermGuid')}")
    else:
        print(f"Single value: {single}")

    if isinstance(multi, list):
        print("Multi value TermGuids:", [v.get("TermGuid") for v in multi if isinstance(v, dict)])
    else:
        print(f"Multi value: {multi}")


if __name__ == "__main__":
    main()
