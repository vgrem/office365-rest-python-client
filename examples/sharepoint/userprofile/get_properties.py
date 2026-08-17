"""Gets a readable summary of user profile properties.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

SUMMARY_KEYS = ["PreferredName", "Department", "JobTitle", "Office", "Manager", "AboutMe", "PictureURL"]
ABOUT_ME_LEN = 120


def main():
    parser = argparse.ArgumentParser(description="Read a user's profile properties")
    parser.add_argument("--user", default=None, help="account name to read (default: current user)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    if args.user:
        target = ctx.web.ensure_user(args.user).execute_query()
        assert target.login_name is not None
        profile = ctx.people_manager.get_properties_for(target.login_name).execute_query()
    else:
        me = ctx.web.current_user
        profile = ctx.people_manager.get_properties_for(me).execute_query()

    props = profile.user_profile_properties or {}
    for key in SUMMARY_KEYS:
        value = props.get(key, "")
        if key == "AboutMe" and isinstance(value, str) and len(value) > ABOUT_ME_LEN:
            value = value[:ABOUT_ME_LEN] + "..."
        print(f"  {key:14s}: {value or '?'}")


if __name__ == "__main__":
    main()
