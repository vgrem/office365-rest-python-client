"""
Follow or unfollow a user (toggles the current state).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Follow or unfollow a user")
    parser.add_argument("--user", required=True, help="Account name of the user to follow/unfollow")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    user = ctx.web.ensure_user(args.user).execute_query()
    if user.login_name is None:
        raise SystemExit(f"User '{args.user}' could not be resolved")

    is_following = ctx.people_manager.am_i_following(user.login_name).execute_query()
    if is_following.value:
        ctx.people_manager.stop_following(user.login_name).execute_query()
        print(f"Unfollowed: {user.login_name}")
    else:
        ctx.people_manager.follow(user.login_name).execute_query()
        print(f"Following: {user.login_name}")


if __name__ == "__main__":
    main()
