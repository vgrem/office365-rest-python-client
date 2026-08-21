"""
Add a user to a SharePoint site group.

Requires Site Owner.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, user_principal, username


def main():
    parser = argparse.ArgumentParser(description="Add a user to a site group")
    parser.add_argument("--group", default="Team Site Members", help="group name")
    parser.add_argument("--user", default=user_principal, help="user login/UPN")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    group = ctx.web.site_groups.get_by_name(args.group)
    user = group.users.add_user(args.user).execute_query()
    print(f"User added to '{args.group}': {user.title}")


if __name__ == "__main__":
    main()
