"""
List all role definitions (permission levels) available on a site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="List role definitions on a site")
    parser.add_argument("--order", action="store_true", help="sort by the built-in Order")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    roles = ctx.web.role_definitions.get().execute_query()
    if args.order:
        roles = sorted(roles, key=lambda r: r.properties.get("Order", 0))

    for role in roles:
        print(f"  {role.name}  (ID: {role.id}, Order: {role.properties.get('Order')})")
    print(f"Total: {len(roles)} role definitions")


if __name__ == "__main__":
    main()
