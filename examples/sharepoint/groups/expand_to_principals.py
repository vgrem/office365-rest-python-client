"""
Expand the associated Members group into principal information objects.

Requires read access to the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Expand the Members group to principals")
    parser.add_argument("--max", type=int, default=100, help="maximum number of principals (default 100)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = ctx.web.associated_member_group.expand_to_principals(args.max).execute_query()
    print(f"Members group principals ({len(result.value)}):")
    for principal_info in result.value:
        print(f"  {principal_info}")


if __name__ == "__main__":
    main()
