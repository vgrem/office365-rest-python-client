"""
List all SharePoint site groups.

Requires read access to the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="List all site groups").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    groups = ctx.web.site_groups.get().execute_query()
    for g in groups:
        print(f"  {g.title}  (ID: {g.id})")
    print(f"Total: {len(groups)} groups")


if __name__ == "__main__":
    main()
