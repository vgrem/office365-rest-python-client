"""
List the users that have access to the current SharePoint site.

Requires read access to the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List site users")
    parser.add_argument("--top", type=int, default=100, help="maximum number of users (default 100)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    users = ctx.web.site_users.select(["LoginName", "Title", "Email"]).top(args.top).get().execute_query()
    print(f"Site users ({len(users)}):")
    for user in users:
        print(f"  {user.login_name}  {user.title or ''}  {user.email or ''}")


if __name__ == "__main__":
    main()
