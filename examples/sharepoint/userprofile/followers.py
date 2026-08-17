"""
List the followers of a user, or the people a user is following.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="List followers / people followed")
    parser.add_argument("--user", help="Account name of the user (default: current user)")
    parser.add_argument("--direction", choices=["followers", "following"], default="followers", help="Direction")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    if args.user:
        target = ctx.web.ensure_user(args.user).execute_query()
        if target.login_name is None:
            raise SystemExit(f"User '{args.user}' could not be resolved")
        account_name = target.login_name
    else:
        me = ctx.web.current_user
        account_name = me.login_name
        if account_name is None:
            raise SystemExit("Current user login name is not available")

    if args.direction == "followers":
        people = ctx.people_manager.get_followers_for(account_name).execute_query()
    else:
        people = ctx.people_manager.get_people_followed_by(account_name).execute_query()

    print(f"{'Followers' if args.direction == 'followers' else 'Following'} of {account_name} ({len(people)}):")
    for person in people:
        print(f"  {person.display_name}  ({person.email})")


if __name__ == "__main__":
    main()
