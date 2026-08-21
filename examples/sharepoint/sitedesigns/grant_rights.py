"""
Grant or revoke access rights for principals on a site design.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Grant site design rights to a principal")
    parser.add_argument("--design-id", required=True, help="site design id")
    parser.add_argument("--principal", required=True, help="principal to grant rights to (e.g. user@contoso.com)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    designs = SiteScriptUtility.get_site_designs(ctx).execute_query()
    target = next((d for d in designs.value if str(d.Id) == args.design_id), None)
    if target is None:
        sys.exit(f"Site design not found: {args.design_id}")

    SiteScriptUtility.grant_site_design_rights(
        ctx, str(target.Id), [args.principal], 1  # 1 = View
    ).execute_query()
    print(f"Rights granted on '{target.Title}' to {args.principal}")

    principals = SiteScriptUtility.get_site_design_rights(ctx, str(target.Id)).execute_query()
    print("Current principals:")
    for p in principals:
        print(f"  {p.properties.get('PrincipalName', '')}")


if __name__ == "__main__":
    main()
