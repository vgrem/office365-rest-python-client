"""
Create a new SharePoint site group (removed after the demo unless --keep).

Requires Site Owner.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create a site group")
    parser.add_argument("--name", default="Project Contributors", help="group name")
    parser.add_argument("--description", default="Contributors to project sites", help="group description")
    parser.add_argument("--keep", action="store_true", help="keep the group (default: delete after demo)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    group = ctx.web.site_groups.add(args.name, args.description).execute_query()
    print(f"Group created: {group.title}  (ID: {group.id})")

    if not args.keep:
        group.delete_object().execute_query()
        print("  (group removed after demo)")


if __name__ == "__main__":
    main()
