"""Gets the OneDrive (default document library) URL for a user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username


def main():
    parser = argparse.ArgumentParser(description="Resolve a user's OneDrive URL")
    parser.add_argument("--user", default=None, help="account name (default: current user)")
    args = parser.parse_args()

    ctx = ClientContext(test_site_url).with_username_and_password(
        tenant=test_tenant, client_id=test_client_id, username=test_username, password=test_password
    )

    if args.user:
        target = ctx.web.ensure_user(args.user).execute_query()
        assert target.login_name is not None
        result = ctx.people_manager.get_default_document_library(target).execute_query()
        print(f"OneDrive URL for {args.user}: {result.value}")
    else:
        me = ctx.web.current_user
        result = ctx.people_manager.get_default_document_library(me).execute_query()
        print(f"OneDrive URL: {result.value}")


if __name__ == "__main__":
    main()
