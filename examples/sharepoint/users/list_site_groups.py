"""
List the SharePoint groups on the current site along with their users.

Requires read access to the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List site groups and members")
    parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    groups = ctx.web.site_groups.expand(["Users"]).get().execute_query()
    print(f"Site groups ({len(groups)}):")
    for group in groups:
        members = ", ".join(u.login_name for u in group.users) if len(group.users) else "-"
        print(f"  {group.login_name}:  {members}")


if __name__ == "__main__":
    main()
