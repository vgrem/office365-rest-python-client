"""
Remove a user from a SharePoint site group.

Requires Site Owner.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, user_principal, username


def main():
    parser = argparse.ArgumentParser(description="Remove a user from a site group")
    parser.add_argument("--group", default="Team Site Members", help="group name")
    parser.add_argument("--user", default=user_principal, help="user login/UPN")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    group = ctx.web.site_groups.get_by_name(args.group)
    group.users.remove_by_login_name(args.user).execute_query()
    print(f"User removed from '{args.group}': {args.user}")


if __name__ == "__main__":
    main()
