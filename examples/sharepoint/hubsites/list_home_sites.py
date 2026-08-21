"""
List all home sites configured for the tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/hubsites
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="Lists all home sites").parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = Tenant(ctx).get_home_sites().execute_query()
    for hs in result.value:
        print(f"  {hs.Title}  ({hs.Url})")


if __name__ == "__main__":
    main()
