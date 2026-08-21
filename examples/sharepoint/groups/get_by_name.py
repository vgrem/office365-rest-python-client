"""
Retrieve a SharePoint site group by name.

Requires read access to the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Get a site group by name")
    parser.add_argument("--group", default="Team Site Members", help="group name")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    g = ctx.web.site_groups.get_by_name(args.group).execute_query()
    members = g.users.get().execute_query()
    print(f"Name:    {g.title}")
    print(f"ID:      {g.id}")
    print(f"Owner:   {g.owner_title}")
    print(f"Members: {len(members)}")


if __name__ == "__main__":
    main()
