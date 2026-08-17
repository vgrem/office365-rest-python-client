"""
Check whether the current user is following a specific user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Check if following a user")
    parser.add_argument("--user", required=True, help="Account name of the user to check")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    user = ctx.web.ensure_user(args.user).execute_query()
    if user.login_name is None:
        raise SystemExit(f"User '{args.user}' could not be resolved")

    result = ctx.people_manager.am_i_following(user.login_name).execute_query()
    print(f"Following {user.login_name}: {result.value}")


if __name__ == "__main__":
    main()
