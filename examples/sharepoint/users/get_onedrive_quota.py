"""
Show the OneDrive quota maximum for a user.

Requires read access to user profiles.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Show a user's OneDrive quota maximum")
    parser.add_argument("--user", default=None, help="account name (default: the authenticated user)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    account = args.user or username
    result = ctx.people_manager.get_user_onedrive_quota_max(account).execute_query()
    print(f"OneDrive quota max for {account}: {result.value}")


if __name__ == "__main__":
    main()
