"""
Set the owner of a SharePoint site group.

Requires Site Owner.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, user_principal, username


def main():
    parser = argparse.ArgumentParser(description="Set a site group owner")
    parser.add_argument("--group", default="Project Contributors", help="group name")
    parser.add_argument("--owner", default=user_principal, help="new owner login/UPN")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    group = ctx.web.site_groups.get_by_name(args.group)
    user = ctx.web.ensure_user(args.owner).execute_query()
    group.set_user_as_owner(user).execute_query()
    print(f"Owner of '{args.group}' set to: {args.owner}")


if __name__ == "__main__":
    main()
