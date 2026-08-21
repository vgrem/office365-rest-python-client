"""
Generates a site script from an existing site.

Site scripts can be exported from an existing site and reused
to apply the same configuration to other sites.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Generate a site script from an existing site")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    parser.add_argument("--list-title", default="Shared Documents", help="list to include in the script")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    result = ctx.web.get_site_script(included_lists=[args.list_title]).execute_query()
    print(result.value.JSON)


if __name__ == "__main__":
    main()
