"""
Ensure a user exists on the current site, adding them if necessary.

Requires Site Owner on the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Add / ensure a user on the site")
    parser.add_argument("--user", required=True, help="user login/UPN")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    user = ctx.web.ensure_user(args.user).execute_query()
    print(f"✓ User ensured on site: {user.title or user.login_name}  ({user.user_principal_name})")


if __name__ == "__main__":
    main()
