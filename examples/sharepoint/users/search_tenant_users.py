"""
Search for users across the whole tenant.

Uses an admin context (tenant admin site + certificate auth).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, tenant


def main():
    parser = argparse.ArgumentParser(description="Search tenant users")
    parser.add_argument("--query", required=True, help="search term")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    result = ctx.search_user(args.query).execute_query()
    print(f"Users matching '{args.query}':")
    for login, info in result.value.items():
        print(f"  {login}  {info}")


if __name__ == "__main__":
    main()
